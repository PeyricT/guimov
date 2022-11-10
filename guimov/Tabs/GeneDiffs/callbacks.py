from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc
import dash

import pandas as pd

from guimov._utils import tools as tl, low_heatmap, full_heatmap


@tl.app.callback(
    Output('table_gd', 'data'),
    Input('rank_test_gd', 'value'),
    Input('clusters_gd', 'value'),
    Input('mod_dropdown_gd', 'value'),
    State('session', 'data'),
)
def update_table(rank_test, cluster, mod, session):
    if session is None or session.get('code') is None or rank_test is None:
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]
    cols = ['names', 'scores', 'logfoldchanges', 'pvals_adj', 'pvals', 'cluster']
    table = pd.DataFrame([], columns=cols)

    if cluster is not None:
        # Only the first 100 genes are displayed
        limit = 100
        # table['names'] = data.uns[markers_exp]['names'][clusters].astype(str)[:limit]
        for col in cols[:-1]:
            table[col] = data.uns[rank_test][col][cluster][:limit]
        table['cluster'] = [cluster]*limit
    else:
        # only the first 30 genes of each clusters are displayed
        limit = 10*3
        for col in cols[:-1]:
            agg_col = []

            for clust in data.uns[rank_test]['names'].dtype.names:
                agg_col += list(data.uns[rank_test][col][clust][:limit])

            if col == 'names':
                table[col] = pd.Series(agg_col).astype(str)
            else:
                table[col] = pd.Series(agg_col).astype(float)

        clusters = []
        for clust in data.uns[rank_test]['names'].dtype.names:
            clusters += [clust]*limit

        table['cluster'] = pd.Series(clusters).astype(str)

    return table.to_dict('records')


@tl.app.callback(
    Output('downlaod_table_csv', 'data'),
    Input('export_all_gd', 'n_clicks'),
    State('rank_test_gd', 'value'),
    State('clusters_gd', 'value'),
    State('mod_dropdown_gd', 'value'),
    State('session', 'data'),
    prevent_initial_call=True,
)
def export_table(_, rank_test, cluster, mod, session):
    if session is None or session.get('code') is None or rank_test is None or mod is None:
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]
    cols = ['names', 'scores', 'logfoldchanges', 'pvals_adj', 'pvals', 'cluster']
    table = pd.DataFrame([], columns=cols)

    if cluster is not None:
        name = f"MarkerGenes_{rank_test}_{cluster}.csv"
        for col in cols[:-1]:
            table[col] = data.uns[rank_test][col][cluster]
        table['cluster'] = [cluster]*data.shape[1]
    else:
        name = f"MarkerGenes_{rank_test}_all.csv"
        for col in cols[:-1]:
            agg_col = []

            for clust in data.uns[rank_test]['names'].dtype.names:
                agg_col += list(data.uns[rank_test][col][clust])

            if col == 'names':
                table[col] = pd.Series(agg_col).astype(str)
            else:
                table[col] = pd.Series(agg_col).astype(float)

        clusters = []
        for clust in data.uns[rank_test]['names'].dtype.names:
            clusters += [clust]*data.shape[1]

        table['cluster'] = pd.Series(clusters).astype(str)

    return dcc.send_data_frame(table.to_csv, name)


@tl.app.callback(
    Output('heatmap_gd', 'figure'),
    Output('loading_div_gd', 'children'),
    Input('rank_test_gd', 'value'),
    Input('nb_genes_gd', 'value'),
    Input('mod_dropdown_gd', 'value'),
    Input('loading_div_gd', 'children'),
    State('session', 'data'),
)
def update_heatmap(rank_test, nb_genes, mod, _load, session):
    if session is None or session.get('code') is None or rank_test is None:
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]
    # on trie les cellules par clusters pour une heatmap plus claire
    clusters = data.uns[rank_test]['params']['groupby']
    if clusters in data.obs:
        fig = full_heatmap(data, rank_test, nb_genes)
    else:
        fig = low_heatmap(data, rank_test, nb_genes)

    fig.update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)

    return fig, ""


@tl.app.callback(
    Output('mod_dropdown_gd', 'options'),
    Output('mod_dropdown_gd', 'value'),
    Input('session', 'modified_timestamp'),
    State('session', 'data'),
)
def update_mod(ts, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if session['reload'] != 'Update':
        raise PreventUpdate

    return [{'label': value, 'value': value} for value in session['infos']['mod']], session['default_mod']


@tl.app.callback(
    Output('rank_test_gd', 'options'),
    Output('rank_test_gd', 'value'),
    Input('session', 'modified_timestamp'),
    Input('mod_dropdown_gd', 'value'),
    State('session', 'data'),
)
def update_rank_genes(ts, mod, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if mod is None:
        return [], None

    ctx = dash.callback_context

    modified_session = False
    for triggered in ctx.triggered:
        modified_session = triggered['prop_id'] == "session.modified_timestamp"

    if modified_session:
        if session['reload'] == 'de':
            return [{'label': value, 'value': value} for value in session['obs'][mod]['rank_test']], dash.no_update
        else:
            raise PreventUpdate

    return [{'label': value, 'value': value} for value in session['obs'][mod]['rank_test']], \
           session['default_values'][mod]['rank_test']


@tl.app.callback(
    Output('clusters_gd', 'options'),
    Output('clusters_gd', 'value'),
    State('session', 'modified_timestamp'),
    Input('rank_test_gd', 'value'),
    Input('mod_dropdown_gd', 'value'),
    State('session', 'data'),
)
def update_rank_genes(ts, rank_test,  mod, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if mod is None or rank_test is None:
        return [], None

    return [
               {'label': value, 'value': value}
               for value in tl.datasets[session['code']][mod].uns[rank_test]['names'].dtype.names
           ], \
           None


