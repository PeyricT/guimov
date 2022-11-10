import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pandas as pd
import scanpy as sc

from guimov._utils import tools as tl, parse_content


@tl.app.callback(
    Output('mod_dropdown_pa', 'options'),
    Output('mod_dropdown_pa', 'value'),
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
    Output('gene_name_pa', 'options'),
    State('session', 'data'),
    Input('gene_name_pa', 'search_value'),
    State('gene_name_pa', 'value'),
    State('mod_dropdown_pa', 'value'),
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

    # Select genes with search in it
    genes_list = [gene for gene in data.var_names if search in gene]

    if current_values:
        genes_list += current_values

    return genes_list


@tl.app.callback(
    Output('table_pa', 'data'),
    Input('gene_name_pa', 'value'),
    Input('texte_area_pa', 'value'),
    Input('input_file_pa', 'contents'),
    State('input_file_pa', 'filename'),
    Input('mod_dropdown_pa', 'value'),
    State('session', 'data'),
)
def update_table(genes_dropdown, gene_text, genes_file_contents, genes_filename, mod, session):
    if session is None or session.get('code') is None \
            or (genes_dropdown is None and genes_file_contents is None and gene_text is None)\
            or mod is None:
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]
    cols = ['Gene', 'Found in dataset']
    table = pd.DataFrame([], columns=cols)

    genes = []
    found = []
    if genes_dropdown:
        genes += genes_dropdown
        found += [True]*len(genes_dropdown)

    if genes_file_contents:
        genes_file = parse_content(genes_file_contents, genes_filename)
        for gene in genes_file:
            genes.append(gene)
            found.append(
                True if gene in data.var_names else False
            )

    if gene_text:
        list_genes = gene_text.strip().split(',')
        for gene in list_genes:
            if gene == '':
                continue
            genes.append(gene)
            found.append(
                True if gene in data.var_names else False
            )

    table['Gene'] = pd.Series(genes)
    table['Found in dataset'] = pd.Series(found)

    return table.to_dict('records')


@tl.app.callback(
    Output('update_from_pa', 'children'),
    Output('loading_div_pa', 'children'),
    Output('alert_pa', 'is_open'),
    Output('alert_pa', 'children'),
    Output('alert_pa', 'className'),
    Input('button_run_pa', 'n_clicks'),
    State('loading_div_ov', 'children'),
    State('pathway_name_pa', 'value'),
    State('table_pa', 'data'),
    State('mod_dropdown_pa', 'value'),
    State('session', 'data'),
)
def run_pathway(_, _loading, pathway_name, gene_table, mod, session):
    if session is None or session.get('code') is None or mod is None:
        raise PreventUpdate

    data = tl.datasets[session['code']][mod]

    if pathway_name is None:
        alert_is_open = True
        alert_children = 'Pathway name is Empty, choose a name for yout pathway'
        alert_className = 'guimov_alert'
        return dash.no_update, dash.no_update, alert_is_open, alert_children, alert_className

    elif pathway_name in data.obs:
        alert_is_open = True
        alert_children = 'Pathway name is already in obs. Choose another name'
        alert_className = 'guimov_alert'
        return dash.no_update, dash.no_update, alert_is_open, alert_children, alert_className

    df = pd.DataFrame.from_records(gene_table)
    df = df[df['Found in dataset']]

    genes = list(df['Gene'])

    if len(genes) < 2:
        alert_is_open = True
        alert_children = 'A pathway need at least 2 valid genes'
        alert_className = 'guimov_alert'
        return dash.no_update, dash.no_update, alert_is_open, alert_children, alert_className

    sc.tl.score_genes(data, genes, use_raw=False, score_name=pathway_name)

    alert_is_open = True
    alert_children = f'Pathways {pathway_name} successfuly computed'
    alert_className = 'guimov_info'

    return f"{pathway_name};{mod}", "",  alert_is_open, alert_children, alert_className
