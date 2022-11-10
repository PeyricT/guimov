import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import time as t
import plotly.express as px

from guimov._utils import tools as tl


@tl.app.callback(
    Output('histplot_qc', 'figure'),
    Input('obs_num_qc', 'value'),
    Input('var_gene_qc', 'value'),
    Input('y_num_qc', 'value'),
    Input('use_overlay_qc', 'value'),
    Input('use_gene_Y_qc', 'value'),
    Input('obs_cat_qc', 'value'),
    Input('opacity_qc', 'value'),
    State('mod_dropdown_qc', 'value'),
    State('session', 'data'),
)
def update_histplot(obs_num, var_gene, y_num, use_overlay, use_gene_Y, obs_cat, opacity, mod, session):
    if session is None or session.get('code') is None \
            or mod is None\
            or (var_gene is None and obs_num is None):
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]
    df = pd.DataFrame([], index=data.obs.index)
    color = None
    use_y = False
    xlabel = None
    ylabel = None

    if var_gene and not use_gene_Y:
        xlabel = var_gene
        df[xlabel] = pd.Series(
            data[:, var_gene].X.toarray().transpose().sum(axis=0), index=data.obs.index
        )
    else:
        xlabel = obs_num
        df[xlabel] = data.obs[obs_num]

    if var_gene and use_gene_Y:
        ylabel = var_gene
        use_y = True
        df[ylabel] = pd.Series(
            data[:, var_gene].X.toarray().transpose().sum(axis=0), index=data.obs.index
        )
    elif y_num:
        ylabel = y_num
        use_y = True
        df[ylabel] = data.obs[y_num]

    if obs_cat:
        df[obs_cat] = data.obs[obs_cat]
        color = obs_cat

    if not use_y:
        fig = px.histogram(df, x=xlabel, color=color)
    else:
        fig = px.histogram(df, x=xlabel, y=ylabel, color=color, histfunc='avg')

    fig.update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)

    if use_overlay:
        fig.update_layout(barmode='overlay')
    if color is not None:
        fig.update_traces(opacity=opacity)

    tl.users_timer[session['id']]['last_update'] = round(t.time() * 1000)

    return fig


@tl.app.callback(
    Output('boxplot_qc', 'figure'),
    Input('obs_num_qc', 'value'),
    Input('var_gene_qc', 'value'),
    Input('use_gene_Y_qc', 'value'),
    Input('obs_cat_qc', 'value'),
    State('mod_dropdown_qc', 'value'),
    State('session', 'data'),
)
def update_boxplot(obs_num, var_gene, use_gene_Y, obs_cat, mod, session):
    if session is None \
            or session.get('code') is None \
            or mod is None \
            or (var_gene is None and obs_num is None) \
            or obs_cat is None:
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]
    df = pd.DataFrame(columns=['Y', 'color'], index=data.obs.index)
    ylabel = None
    if var_gene and not use_gene_Y:
        ylabel = var_gene
        df[ylabel] = pd.Series(
            data[:, var_gene].X.toarray().transpose().sum(axis=0), index=data.obs.index
        )
    else:
        ylabel = obs_num
        df[ylabel] = data.obs[obs_num]

    df['color'] = data.obs[obs_cat]

    fig = px.box(df, y=ylabel, color='color', notched=True)

    fig.update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)

    tl.users_timer[session['id']]['last_update'] = round(t.time() * 1000)

    return fig


@tl.app.callback(Output('mod_dropdown_qc', 'options'), Output('mod_dropdown_qc', 'value'),
              Input('session', 'modified_timestamp'), State('session', 'data'))
def update_mod(ts, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if session['reload'] != 'Update':
        raise PreventUpdate

    return [{'label': value, 'value': value} for value in session['infos']['mod']], session['default_mod']


@tl.app.callback(
    Output('obs_num_qc', 'options'), Output('obs_num_qc', 'value'),
    Output('obs_cat_qc', 'options'), Output('obs_cat_qc', 'value'),
    Output('var_gene_qc', 'value'),
    Output('y_num_qc', 'options'),   Output('y_num_qc', 'value'),
    State('session', 'modified_timestamp'), State('session', 'data'),
    Input('mod_dropdown_qc', 'value'),
)
def update_parameters(ts, session, mod):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if mod is None:
        return \
            [], None, \
            [], None, \
            None, \
            [], None,

    return \
        [{'label': value, 'value': value} for value in session['obs'][mod]['n_obs_numerical']], \
        session['default_values'][mod]['n_obs_numerical'], \
        [{'label': value, 'value': value} for value in session['obs'][mod]['n_obs_categorical']], \
        session['default_values'][mod]['n_obs_categorical'], \
        None, \
        [{'label': value, 'value': value} for value in session['obs'][mod]['n_obs_numerical']], None


@tl.app.callback(
    Output('var_gene_qc', 'options'),
    State('session', 'data'),
    Input('var_gene_qc', 'search_value'),
    State('var_gene_qc', 'value'),
    State('mod_dropdown_qc', 'value'),
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
