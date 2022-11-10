from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
from PIL import Image
import scanpy as sc
import pandas as pd
import numpy as np
import time as t
import dash

from guimov._utils import tools as tl, plot_sankey


@tl.app.callback(Output('umap_cl', 'figure'),
                  Input('embedding_dropdown_cl', 'value'),
                  Input('pct_cells_cl', 'value'),
                  Input('points_size_cl', 'value'),
                  Input('res_dropdown_cl', 'value'),
                  State('session', 'data'),
                  State('mod_dropdown_cl', 'value'),
                  State('clusters_temp', 'data'),)
def update_umap(embed, pct_cells, psize, res, session, mod, clusters):
    if embed is None or session is None or session.get('code') is None or mod is None or res is None:
        raise PreventUpdate

    dataset = tl.datasets.get(session['code'])
    if dataset is None:
        raise PreventUpdate

    # slice data only if a subset data is asked
    if pct_cells < 1:
        slicer = np.random.choice([True, False], dataset[mod].shape[0], p=[pct_cells, 1-pct_cells])
    else:
        slicer = [True]*dataset[mod].shape[0]

    data = dataset[mod][slicer]
    color = pd.Series(clusters[mod][res])[slicer]

    test = pd.DataFrame([], columns=['X', 'Y'])
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
        test['X'] = data.obsm[embed][:, 0]
        test['Y'] = data.obsm[embed][:, 1]

    fig = px.scatter(x=test['X'], y=test['Y'], color=color)
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
    Output('sankey_plot_cl', 'figure'),
    Input('res_dropdown_cl', 'value'),
    Input('res2_dropdown_cl', 'value'),
    State('mod_dropdown_cl', 'value'),
    State('session', 'data'),
    State('clusters_temp', 'data'),
)
def update_sankey_plot(source, target, mod, session, clusters):
    if mod is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if source is None or target is None or source == target:
        raise PreventUpdate

    df = pd.DataFrame([], columns=[source, target])
    df[source] = pd.Series(clusters[mod][source]).astype('category')
    df[target] = pd.Series(clusters[mod][target]).astype('category')

    fig = plot_sankey(df, source, target)
    fig.update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)

    tl.users_timer[session['id']]['last_update'] = round(t.time() * 1000)

    return fig


@tl.app.callback(Output('mod_dropdown_cl', 'options'), Output('mod_dropdown_cl', 'value'),
              Input('session', 'modified_timestamp'), State('session', 'data'))
def update_mod(ts, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if session['reload'] != 'Update':
        raise PreventUpdate

    return [{'label': value, 'value': value} for value in session['infos']['mod']], session['default_mod']


@tl.app.callback(Output('embedding_dropdown_cl', 'options'), Output('embedding_dropdown_cl', 'value'),
                  Output('res_dropdown_cl', 'options'), Output('res_dropdown_cl', 'value'),
                  Output('res2_dropdown_cl', 'options'), Output('res2_dropdown_cl', 'value'),
                  State('session', 'modified_timestamp'),
                  Input('clusters_temp', 'modified_timestamp'),
                  State('session', 'data'),
                  State('clusters_temp', 'data'),
                  Input('mod_dropdown_cl', 'value'))
def update_parameters(ts, ts_clust, session, clusters, mod):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if mod is None:
        return [], None, [], None, [], None

    if clusters is None:
        clusters = {mod: dict()}

    ctx = dash.callback_context

    if ctx.triggered[0]['prop_id'] == 'clusters_temp.modified_timestamp':
        return dash.no_update, dash.no_update,\
               [{'label': value, 'value': value} for value in clusters[mod]], dash.no_update, \
               [{'label': value, 'value': value} for value in clusters[mod]], dash.no_update,
    else:
        return \
            [{'label': value, 'value': value} for value in session['obs'][mod]['n_embeddings']], \
            session['default_values'][mod]['n_embeddings'], \
            [{'label': value, 'value': value} for value in clusters[mod]], None, \
            [{'label': value, 'value': value} for value in clusters[mod]], None,


@tl.app.callback(Output('clusters_temp', 'data'),
                  Output('loading_div_cl', 'children'),
                  Input('compute_cl', 'n_clicks'),
                  State('input_res_cl', 'value'),
                  State('session', 'data'),
                  State('clusters_temp', 'data'),
                  State('mod_dropdown_cl', 'value'),
                  State('loading_div_cl', 'children'),)
def compute_clustering(_, res, session, clusters, mod, _load):
    if session is None or session.get('code') is None or mod is None:
        raise PreventUpdate

    dataset = tl.datasets.get(session['code'])
    if dataset is None:
        raise PreventUpdate

    if clusters is None:
        clusters = {}

    if clusters.get(mod) is None:
        clusters[mod] = {}

    key = f"guimov_clustering_{res}"

    if key not in clusters[mod]:
        sc.tl.leiden(dataset[mod], resolution=res, key_added=key)
        clusters[mod][key] = dataset[mod].obs[key]
        dataset[mod].obs.drop(columns=key)

    return clusters, ""


@tl.app.callback(
    Output('update_from_cl', 'children'),
    Input('save_clustering_cl', 'n_clicks'),
    State('session', 'data'),
    State('clusters_temp', 'data'),
    State('mod_dropdown_cl', 'value'),
    State('res_dropdown_cl', 'value')
)
def load_clustering(_, session, clusters, mod, res):
    if session is None or session.get('code') is None or mod is None or res is None:
        raise PreventUpdate

    dataset = tl.datasets.get(session['code'])
    if dataset is None:
        raise PreventUpdate

    dataset[mod].obs[res] = pd.Series(clusters[mod][res], index=dataset[mod].obs.index).astype('category')

    return f"{res};{mod}"
