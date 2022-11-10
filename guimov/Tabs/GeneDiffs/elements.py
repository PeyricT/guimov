from dash import dcc, dash_table, html
import plotly.express as px
import dash_bootstrap_components as dbc
from guimov._utils import tools as tl


GeneDiffs_title = html.H1('Genes Differentiations')

table_gd = dash_table.DataTable(
    id='table_gd',
    columns=[
        {"name": i, "id": i, "deletable": False, "selectable": True}
        for i in ['names', 'scores', 'logfoldchanges', 'pvals_adj', 'pvals', 'cluster']
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
    export_format="csv",
    # je sais... J'ai explicitement dit plusieurs fois qu'il ne fallait pas faire ça.
    # Mais des fois on fait pas ce qu'on veut.
    style_cell={'text-align': 'center'},
)

export_all_gd = html.Button(
    id='export_all_gd',
    children='export all marker genes',
    className="guimov_button",
)

tooltip_export_all_gd = dbc.Tooltip(
    "Export all genes in csv. (very large file, <nbGenes * nbClusters> rows)",
    target="export_all_gd",
    placement="right",
    className="guimov_tooltip",
)

heatmap_gd = dcc.Graph(
    id='heatmap_gd',
    figure=px.box(
        tl.iris, y='sepal_length', x="species"
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color),
)

mod_dropdown_gd = dcc.Dropdown(
    id="mod_dropdown_gd",
    placeholder="omics data",
    className="guimov_dropdown",
)

tooltip_mod_dropdown_gd = dbc.Tooltip(
    "Features type",
    target="mod_dropdown_gd",
    placement="right",
    className="guimov_tooltip",
)

rank_test_gd = dcc.Dropdown(
    id="rank_test_gd",
    placeholder="Ranking test",
    className="guimov_dropdown",
)

tooltip_rank_test_gd = dbc.Tooltip(
    "Differential Expression already calculated",
    target="rank_test_gd",
    placement="right",
    className="guimov_tooltip",
)

clusters_gd = dcc.Dropdown(
    id="clusters_gd",
    placeholder="Clusters, default : All",
    className="guimov_dropdown",
)

tooltip_clusters_gd = dbc.Tooltip(
    "Clusters to explore in table (by default all clusters are included)",
    target="clusters_gd",
    placement="right",
    className="guimov_tooltip",
)

nb_genes_gd = dcc.Slider(
    id='nb_genes_gd',
    min=1,
    max=6,
    step=1,
    value=3,
    className="guimov_slider",
)

tooltip_nb_genes_gd = dbc.Tooltip(
    "Numbers of Genes per clusters in the heatmap",
    target="nb_genes_gd",
    placement="right",
    className="guimov_tooltip",
)

loading_gd = dcc.Loading(
    id="loading_gd",
    className="guimov_loading",
    children=html.Div(
        id="loading_div_gd",
        children=None,
    ),
    type="circle",
)
