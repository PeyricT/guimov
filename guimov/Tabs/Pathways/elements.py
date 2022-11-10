import dash_bootstrap_components as dbc
from dash import dcc, dash_table, html

GeneDiffs_title = html.H1('Pathways')

loading_pa = dcc.Loading(
    id="loading_pa",
    className="guimov_loading",
    children=html.Div(
        id="loading_div_pa",
        children=None,
    ),
    type="circle",
)

mod_dropdown_pa = dcc.Dropdown(
    id="mod_dropdown_pa",
    placeholder="omics data",
    className="guimov_dropdown",
)

tooltip_mod_dropdown_pa = dbc.Tooltip(
    "Feature type",
    target="mod_dropdown_pa",
    placement="right",
    className="guimov_tooltip",
)

gene_name_pa = dcc.Dropdown(
    id='gene_name_pa',
    multi=True,
    clearable=True,
    placeholder="Select genes",
    className="guimov_dropdown",
)

tooltip_gene_name_pa = dbc.Tooltip(
    "Select Genes to add in pathways, write first letter to see suggestion",
    target="gene_name_pa",
    placement="right",
    className="guimov_tooltip",
)

pathway_name_pa = dcc.Input(
    id="pathway_name_pa",
    placeholder="Name of pathway",
    debounce=False,
    className="guimov_imput",
 )

tooltip_pathway_name_pa = dbc.Tooltip(
    "Enter name of pathways",
    target="pathway_name_pa",
    placement="right",
    className="guimov_tooltip",
)

texte_area_pa = dcc.Textarea(
    id='texte_area_pa',
    placeholder='add list of genes',
    className="guimov_imput",
)

tooltip_texte_area_pa = dbc.Tooltip(
    "Write or copy/paste genes, split with comma without spaces.",
    target="texte_area_pa",
    placement="right",
    className="guimov_tooltip",
)

input_file_pa = dcc.Upload(
    id='input_file_pa',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    # Allow multiple files to be uploaded
    multiple=False,
    className="guimov_input_file",
)

tooltip_input_file_pa = dbc.Tooltip(
    "Get genes from first columns of csv or excel files",
    target="input_file_pa",
    placement="right",
    className="guimov_tooltip",
)

button_run_pa = html.Button(
    id='button_run_pa',
    children='Run pathway',
    className="guimov_button",
)

tooltip_button_run_pa = dbc.Tooltip(
    "Run the pathways, the results is store as numerical metadata in dataset",
    target="button_run_pa",
    placement="right",
    className="guimov_tooltip",
)

label_error_pa = html.Div(
    id="label_error_pa",
    children=""
)

update_from_pa = html.Div(
    id="update_from_pa",
    hidden=True,
)

table_pa = dash_table.DataTable(
    id='table_pa',
    columns=[
        {"name": i, "id": i, "deletable": False, "selectable": True}
        for i in ['Gene', 'Found in dataset']
    ],
    editable=False,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    row_deletable=False,
    page_action="native",
    page_current=0,
    page_size=10,
    style_as_list_view=True,

    # je sais... J'ai explicitement dit plusieurs fois qu'il ne fallait pas faire ça.
    # Mais des fois on fait pas ce qu'on veut.
    style_cell={'text-align': 'center'},
)

alert_pa = dbc.Alert(
    "Hello! I am an auto-dismissing alert!",
    id="alert_pa",
    is_open=False,
    duration=7000,
    className="guimov_info",
)
