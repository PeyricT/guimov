from dash import html
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc

from guimov._utils import plot_sankey, tools as tl


tab_title = html.H2('Clustering')

umap_cl = dcc.Graph(
    id='umap_cl',
    figure=px.scatter(
        tl.iris, x="sepal_width", y="sepal_length"
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)
)

sankey_plot_cl = dcc.Graph(
    id='sankey_plot_cl',
    figure=plot_sankey(
        tl.iris, source="species", target="size"
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color),
)

mod_dropdown_cl = dcc.Dropdown(
    id="mod_dropdown_cl",
    placeholder="omique data",
    persistence=True,
    persistence_type='session',
    className="guimov_dropdown",
)

tooltip_mod_dropdown_cl = dbc.Tooltip(
    "Feature type",
    target="mod_dropdown_cl",
    placement="right",
    className="guimov_tooltip",
)

embedding_dropdown_cl = dcc.Dropdown(
    persistence=True,
    persistence_type='session',
    id="embedding_dropdown_cl",
    placeholder="Embeddings",
    className="guimov_dropdown",
)

tooltip_embedding_dropdown_cl = dbc.Tooltip(
    "Select which embeddind to use (coordinates of cells). "
    "Select ‘spatial ’ with a spatial dataset to display the image of sample behind points",
    target="embedding_dropdown_cl",
    placement="right",
    className="guimov_tooltip",
)

res_dropdown_cl = dcc.Dropdown(
    persistence=True,
    persistence_type='session',
    id="res_dropdown_cl",
    placeholder="resolution",
    className="guimov_dropdown",
)

tooltip_res_dropdown_cl = dbc.Tooltip(
    "Clustering use for the first graph and at the top of the second one",
    target="res_dropdown_cl",
    placement="right",
    className="guimov_tooltip",
)

res2_dropdown_cl = dcc.Dropdown(
    persistence=True,
    persistence_type='session',
    id="res2_dropdown_cl",
    placeholder="2eme resolution",
    className="guimov_dropdown",
)

tooltip_res2_dropdown_cl = dbc.Tooltip(
    "Clustering use at the bottom of the second graph",
    target="res2_dropdown_cl",
    placement="right",
    className="guimov_tooltip",
)

pct_cells_cl = dcc.Slider(
    persistence=True,
    persistence_type='session',
    id='pct_cells_cl',
    min=0,
    max=1,
    step=None,
    marks={0.10: '10%', 0.25: '25%', 0.50: '50%', 0.75: '75%', 1: '100%'},
    value=1,
    className="guimov_slider",
)

tooltip_pct_cells_cl = dbc.Tooltip(
    "Percentage of cells to display",
    target="pct_cells_cl",
    placement="right",
    className="guimov_tooltip",
)

points_size_cl = dcc.Slider(
    persistence=True,
    persistence_type='session',
    id='points_size_cl',
    min=1,
    max=10,
    step=1,
    value=5,
    className="guimov_slider",
)

tooltip_points_size_cl = dbc.Tooltip(
    "Size of points in first graph",
    target="points_size_cl",
    placement="right",
    className="guimov_tooltip",
)

input_res_cl = dcc.Input(
    id='input_res_cl',
    type='number',
    min=0.01,
    max=4,
    step=0.01,
    value=1,
    className="guimov_imput",
)

tooltip_input_res_cl = dbc.Tooltip(
    "Select the resolution of clustering",
    target="input_res_cl",
    placement="right",
    className="guimov_tooltip",
)

compute_cl = html.Button(
    id='compute_cl',
    children='Compute clustering',
    className="guimov_button",
)

tooltip_compute_cl = dbc.Tooltip(
    "Calculate clustering with selected resolution to use in dropdowns",
    target="compute_cl",
    placement="right",
    className="guimov_tooltip",
)

save_clustering_cl = html.Button(
    id='save_clustering_cl',
    children='Load clustering in dataset',
    className="guimov_button",
)

tooltip_save_clustering_cl = dbc.Tooltip(
    "Load clustering of the first dropdown in dataset as categorical metada",
    target="save_clustering_cl",
    placement="right",
    className="guimov_tooltip",
)

update_from_cl = html.Div(
    id="update_from_cl",
    hidden=True,
)

loading_cl = dcc.Loading(
    id="loading_cl",
    className="guimov_loading",
    children=html.Div(
        id="loading_div_cl",
        children=None,
    ),
    type="circle",
)

