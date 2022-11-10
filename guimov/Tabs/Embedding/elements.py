from dash import html
from dash import dcc
import dash_daq as daq
import plotly.express as px
from guimov._utils import tools as tl
import dash_bootstrap_components as dbc

tab_title = html.H2('Embedding')

umap_em = dcc.Graph(
    id='umap_em',
    figure=px.scatter(
        tl.iris, x="sepal_width", y="sepal_length"
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)
)

mod_dropdown_em = dcc.Dropdown(
    id="mod_dropdown_em",
    placeholder="omique data",
    persistence=True,
    persistence_type='session',
    className="guimov_dropdown",
)

tooltip_mod_dropdown_em = dbc.Tooltip(
    "Features type",
    target="mod_dropdown_em",
    placement="right",
    className="guimov_tooltip",
)

embedding_dropdown_em = dcc.Dropdown(
    persistence=True,
    persistence_type='session',
    id="embedding_dropdown_em",
    placeholder="Embeddings",
    className="guimov_dropdown",
)

tooltip_embedding_dropdown_em = dbc.Tooltip(
    "Select which embeddind to use (coordinates of cells). "
    "Select ‘spatial’ with a spatial dataset to display the image of sample behind points.",
    target="embedding_dropdown_em",
    placement="right",
    className="guimov_tooltip",
)

factor_dropdown_em = dcc.Dropdown(
    persistence=True,
    persistence_type='session',
    id="factor_dropdown_em",
    placeholder="Observations",
    className="guimov_dropdown",
)

tooltip_factor_dropdown_em = dbc.Tooltip(
    "Seletec metadata to explore (change the color of graph)",
    target="factor_dropdown_em",
    placement="right",
    className="guimov_tooltip",
)

gene_name_em = dcc.Dropdown(
    persistence=True,
    persistence_type='session',
    id='gene_name_em',
    multi=True,
    clearable=True,
    placeholder="Select gene.s",
    className="guimov_dropdown",
)

tooltip_gene_name_em = dbc.Tooltip(
    "Seletec one or more genes "
    "(write the first letter to show all options of the dropdown, "
    "sum expression of genes, "
    "priority against metadata)",
    target="gene_name_em",
    placement="right",
    className="guimov_tooltip",
)

use_3d_em = daq.ToggleSwitch(
    persistence=True,
    persistence_type='session',
    id="use_3d_em",
    label='Enable 3D plot',
    labelPosition='left',
    value=False,
    className="guimov_toggle",
)

tooltip_use_3d_em = dbc.Tooltip(
    "When embedding allow it permit to display a 3d graph"
    " (which can be move in all directions)",
    target="use_3d_em",
    placement="right",
    className="guimov_tooltip",
)

pct_cells_em = dcc.Slider(
    persistence=True,
    persistence_type='session',
    id='pct_cells_em',
    min=0,
    max=1,
    step=None,
    marks={0.10: '10%', 0.25: '25%', 0.50: '50%', 0.75: '75%', 1: '100%'},
    value=1,
    className="guimov_slider",
)

tooltip_pct_cells_em = dbc.Tooltip(
    "Percentage of cells to display (randomly choose). "
    "Use it for large datasets (>10’000cells) or with a small computer.",
    target="pct_cells_em",
    placement="right",
    className="guimov_tooltip",
)

points_size_em = dcc.Slider(
    persistence=True,
    persistence_type='session',
    id='points_size_em',
    min=1,
    max=10,
    step=1,
    value=5,
    className="guimov_slider",
)

tooltip_points_size_em = dbc.Tooltip(
    "Size of points on the graph",
    target="points_size_em",
    placement="right",
    className="guimov_tooltip",
)

pct_obs_em = dcc.RangeSlider(
    persistence=True,
    persistence_type='session',
    id='pct_obs_em',
    min=0,
    max=1,
    step=0.025,
    marks={
        0: '0%', 0.10: '10%', 0.25: '25%', 0.50: '50%', 0.75: '75%', 0.90: '90%', 1: '100%',
    },
    value=[0, 1],
    className="guimov_slider",
)

tooltip_pct_obs_em = dbc.Tooltip(
    "Range of color to use when display a numerical metadata",
    target="pct_obs_em",
    placement="right",
    className="guimov_tooltip",
)

pct_alpha_em = dcc.Slider(
    id='pct_alpha_em',
    min=0,
    max=1,
    step=0.05,
    marks={
        0: '0%', 0.10: '10%', 0.25: '25%', 0.50: '50%', 0.75: '75%', 0.90: '90%', 1: '100%',
    },
    value=1,
    className="guimov_slider",
)

tooltip_pct_alpha_em = dbc.Tooltip(
    "Percentage of points opacity, usable only with spatial datasets.",
    target="pct_alpha_em",
    placement="right",
    className="guimov_tooltip",
)

save_svg_em = html.Button(
    id='save_svg_em',
    children="save in svg format",
    className="guimov_button",
)

tooltip_save_svg_em = dbc.Tooltip(
    "Save graph in svg format",
    target="save_svg_em",
    placement="right",
    className="guimov_tooltip",
)

cells1_selection_em = html.Button(
    id='cells1_selection_em',
    children='cells selection 1',
    className="guimov_button",
)

tooltip_cells1_selection_em = dbc.Tooltip(
    "Use the ‘lasso’ tool of graph to select cells. Then press ‘cells selection 1’",
    target="cells1_selection_em",
    placement="bottom",
    className="guimov_tooltip",
)

cells2_selection_em = html.Button(
    id='cells2_selection_em',
    children='cells selection 2',
    className="guimov_button",
)

tooltip_cells2_selection_em = dbc.Tooltip(
    "Use the ‘lasso’ tool of graph to select cells. Then press ‘cells selection 2’",
    target="cells2_selection_em",
    placement="bottom",
    className="guimov_tooltip",
)

compute_de_em = html.Button(
    id='compute_de_em',
    children='compute DE',
    className="guimov_button",
)

tooltip_compute_de_em = dbc.Tooltip(
    "Chose the name of the DE and compute with ‘compute DE’. "
    "The resuls can be seen in the Differential Expression tab",
    target="compute_de_em",
    placement="bottom",
    className="guimov_tooltip",
)

de_name_em = dcc.Input(
    id="de_name_em",
    placeholder="Name of DE",
    debounce=False,
    className="guimov_imput",
 )

update_from_em = html.Div(
    id="update_from_em",
    hidden=True,
)

loading_em = dcc.Loading(
    id="loading_em",
    className="guimov_loading",
    children=html.Div(
        id="loading_div_em",
        children=None,
    ),
    type="circle",
)

alert_em = dbc.Alert(
    "Hello! I am an auto-dismissing alert!",
    id="alert_em",
    is_open=False,
    duration=7000,
    className="guimov_info",
)
