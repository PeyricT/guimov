import dash
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import time as t
import numpy as np
import plotly.graph_objects as go
from dash import dcc
import scanpy as sc
from PIL import Image

from guimov._utils import tools as tl


@tl.app.callback(Output('umap_em', 'figure'),
                  Input('embedding_dropdown_em', 'value'),
                  Input('factor_dropdown_em', 'value'),
                  Input('pct_cells_em', 'value'),
                  Input('pct_obs_em', 'value'),
                  Input('points_size_em', 'value'),
                  Input('gene_name_em', 'value'),
                  Input('use_3d_em', 'value'),
                  Input('pct_alpha_em', 'value'),
                  State('session', 'data'),
                  State('mod_dropdown_em', 'value'),)
def update_umap(embed, factor, pct_cells, pct_obs, psize, genes, use_3d, opacity, session, mod):
    if embed is None or (factor is None and (genes is None or genes == [])) or\
            session is None or session.get('code') is None or mod is None:
        raise PreventUpdate

    dataset = tl.datasets.get(session['code'])
    if dataset is None:
        raise PreventUpdate

    # slice data only if a subset data is asked
    if pct_cells < 1:
        data = dataset[mod][np.random.choice([True, False], dataset[mod].shape[0], p=[pct_cells, 1-pct_cells])]
    else:
        data = dataset[mod]

    # if genes are provide, they have the priorities
    if genes:
        color = data[:, genes].X.toarray().transpose().sum(axis=0)
    else:
        color = data.obs[factor]

    # change the color min and max according quantile
    if ((factor is not None and factor in session['obs'][mod]['n_obs_numerical']) or genes) and pct_obs != [0, 1]:
        p_low = np.quantile(color, pct_obs[0])
        p_high = np.quantile(color, pct_obs[1])
        color = [
            p_low if c < p_low else p_high if c > p_high else c for c in color
        ]
        # data = data[data.obs[factor].gt(p_low) & data.obs[factor].lt(p_high)]    # surpime les valeurs extremes

    test = pd.DataFrame([], columns=['index', 'X', 'Y', 'color'], index=data.obs_names)
    test['index'] = data.obs_names

    if embed == "spatial":
        data_name = next(iter(data.uns['spatial'].keys()))
        scale_factor = data.uns['spatial'][data_name]['scalefactors']['tissue_hires_scalef']
        max_height = int(data.uns['spatial'][data_name]['images']['hires'].shape[0])

        test['Y'] = max_height - data.obsm[embed][:, 1]*scale_factor
        test['X'] = data.obsm[embed][:, 0]*scale_factor

        min_x = test['X'].min()
        max_x = test['X'].max()
        min_y = test['Y'].min()
        max_y = test['Y'].max()

    else:
        test['Y'] = data.obsm[embed][:, 1]
        test['X'] = data.obsm[embed][:, 0]

    test['color'] = color

    # use 3d plot if possible and asked
    if data.obsm[embed].shape[1] > 2 and use_3d:
        fig = px.scatter_3d(
            x=data.obsm[embed][:, 0], y=data.obsm[embed][:, 1], z=data.obsm[embed][:, 2], color=color, opacity=opacity,
        )
    else:
        fig = px.scatter(
            test, x='X', y='Y', color='color', custom_data=['index'], opacity=opacity,
        )
    fig.update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)
    fig.update_traces(marker_size=psize)

    if embed == "spatial":

        rgb_8bits_array = (data.uns['spatial'][data_name]['images']['hires']*255).astype('uint8')
        img = Image.fromarray(rgb_8bits_array, 'RGB')
        width, height = img.size

        x_margin = (max_x - min_x) * 0.05
        y_margin = (max_y - min_y) * 0.05
        fig.update_layout(
            xaxis=dict(range=[min_x-x_margin, max_x+x_margin], showgrid=False),
            yaxis=dict(range=[min_y-y_margin, max_y+y_margin], showgrid=False, scaleanchor="x", scaleratio=1,),
        )

        fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=height,
                sizex=width,
                sizey=height,
                sizing="stretch",
                opacity=1,
                layer="below")
        )

    tl.users_timer[session['id']]['last_update'] = round(t.time() * 1000)

    return fig


@tl.app.callback(
    Output('update_from_em', 'children'),
    Output('cells1_selection_em', 'children'),
    Output('cells2_selection_em', 'children'),
    Output('loading_div_em', 'children'),
    Output('alert_em', 'is_open'),
    Output('alert_em', 'children'),
    Output('alert_em', 'className'),
    Input('cells1_selection_em', 'n_clicks'),
    Input('cells2_selection_em', 'n_clicks'),
    Input('compute_de_em', 'n_clicks'),
    State('loading_div_em', 'children'),
    State('de_name_em', 'value'),
    State('umap_em', 'selectedData'),
    State('session', 'data'),
    State('mod_dropdown_em', 'value'),
)
def selected_data(_sel1, _sel2, _compute, _load, de_name, data, session, mod):
    if data is None or mod is None:
        raise PreventUpdate

    dataset = tl.datasets.get(session['code'])
    if dataset is None:
        raise PreventUpdate

    if de_name in dataset[mod].obs.columns:
        raise PreventUpdate

    alert_is_open = dash.no_update
    alert_children = dash.no_update
    alert_className = dash.no_update

    cells = []
    for point in data['points']:
        cells.append(point['customdata'][0])

    df = dataset[mod].obs
    key = 'guimov_temp_de'

    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'cells1_selection_em.n_clicks':
        if key in df.columns:
            df.drop(columns=key)

        ind = df.index.isin(cells)
        df[key] = pd.Series(['1' if cell else '0' for cell in ind], index=df.index).astype('category')

        return dash.no_update, f"{ind.sum()} cells", dash.no_update, dash.no_update,\
               alert_is_open, alert_children, alert_className

    elif ctx.triggered[0]['prop_id'] == 'cells2_selection_em.n_clicks':
        if key not in df.columns:
            raise PreventUpdate

        ind = df.index.isin(cells)
        df[key] = pd.Series(
            [
                value if not cell else '0' if cell and value == '1' else '2' for cell, value in zip(ind, df[key])
            ], index=df.index
        ).astype('category')

        return dash.no_update, dash.no_update, f"{ind.sum()} cells", dash.no_update,\
               alert_is_open, alert_children, alert_className

    elif ctx.triggered[0]['prop_id'] == 'compute_de_em.n_clicks':
        if key not in df.columns:
            alert_is_open = True
            alert_children = f"Select at least `cells selection 1`"
            alert_className = "guimov_alert"
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, \
                   alert_is_open, alert_children, alert_className

        if de_name is None or de_name == '':
            alert_is_open = True
            alert_children = f"A DE's name is required"
            alert_className = "guimov_alert"
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update,\
                   alert_is_open, alert_children, alert_className

        if len(df[key].cat.categories) == 2:
            groups = ['0', '1']
        else:
            groups = ['1', '2']

        layer = None
        if 'Normalise' in dataset[mod].layers.keys():
            layer = 'Normalise'

        sc.tl.rank_genes_groups(
            dataset[mod], key, groups=groups, key_added="rank_genes_"+de_name, use_raw=False, layer=layer
        )

        key_obs = 'guimov_selected_cells' + de_name
        dataset[mod].obs[key_obs] = dataset[mod].obs.pop(key)
        dataset[mod].uns["rank_genes_"+de_name]['params']['groupby'] = key_obs

        alert_is_open = True
        alert_children = f"DE `{de_name}` successfully computed."
        alert_className = "guimov_info"

    return f"rank_genes_{de_name};{mod}", "cells selection 1", "cells selection 2", "",\
           alert_is_open, alert_children, alert_className


@tl.app.callback(Output('mod_dropdown_em', 'options'), Output('mod_dropdown_em', 'value'),
              Input('session', 'modified_timestamp'), State('session', 'data'))
def update_mod(ts, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    print(session['reload'], session['reload'] != 'Update')

    if session['reload'] != 'Update':
        raise PreventUpdate

    return [{'label': value, 'value': value} for value in session['infos']['mod']], session['default_mod']


@tl.app.callback(Output('embedding_dropdown_em', 'options'), Output('embedding_dropdown_em', 'value'),
              Output('factor_dropdown_em', 'options'), Output('factor_dropdown_em', 'value'),
              Output('gene_name_em', 'value'),
              Input('session', 'modified_timestamp'), State('session', 'data'),
              Input('mod_dropdown_em', 'value'))
def update_parameters(ts, session, mod):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if mod is None:
        return \
            [], None, \
            [], None, None

    cat = session['obs'][mod]['n_obs_categorical'] + session['obs'][mod]['n_obs_numerical']

    ctx = dash.callback_context

    modified_session = False
    for triggered in ctx.triggered:
        modified_session = triggered['prop_id'] == "session.modified_timestamp"

    if modified_session:
        if session['reload'] == 'pathways' or session['reload'] == 'clusters':
            return dash.no_update, dash.no_update, [{'label': value, 'value': value} for value in cat],\
               dash.no_update, dash.no_update
        else:
            raise PreventUpdate

    default_obs = session['default_values'][mod]['n_obs_categorical'] \
        if session['default_values'][mod]['n_obs_categorical'] else session['default_values'][mod]['n_obs_numerical']

    return \
        [{'label': value, 'value': value} for value in session['obs'][mod]['n_embeddings']], \
        session['default_values'][mod]['n_embeddings'], \
        [{'label': value, 'value': value} for value in cat], \
        default_obs, \
        None


@tl.app.callback(
    Output('gene_name_em', 'options'),
    State('session', 'data'),
    Input('gene_name_em', 'search_value'),
    State('gene_name_em', 'value'),
    State('mod_dropdown_em', 'value'),
    )
def update_gene_name(session, search, current_values, mod):
    """
    In order to optimize the request, genes are only display when the first letter is gave.
    (26'000 names are often too expensive for local computer)
    :param session:
    :param search:
    :param current_values:
    :param mod:
    :return:
    """
    if not search or not mod.startswith('rna'):
        raise PreventUpdate

    dataset = tl.datasets.get(session['code'])
    if dataset is None:
        raise PreventUpdate

    data = dataset[mod]

    genes_list = [gene for gene in data.var_names if search in gene]
    if current_values is not None:
        genes_list += current_values

    return genes_list


# TODO : Remove image save here, once it's download.
@tl.app.callback(
    Output('downlaod_image', 'data'),
    Input('save_svg_em', 'n_clicks'),
    State('umap_em', 'figure'),
    State('session', 'data'),
    prevent_initial_call=True,
)
def download_em(_, figure, session):
    """
    Fonction to download figure in high quality, the figure is first save in the server, then send to the user.
    currently in test
    :param _:
    :param figure:
    :param session:
    :return:
    """
    if session is None or figure is None:
        raise PreventUpdate

    figure = go.Figure(figure)
    figure.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', width=1920/2, height=1080/2)
    path = f"assets/images/embedding.pdf"
    figure.write_image(path)
    return dcc.send_file(path, filename="embedding.pdf")
