from dash import html
from dash import dcc
import dash_daq as daq
import plotly.express as px
from guimov._utils import tools as tl
import dash_bootstrap_components as dbc

QCs_title = html.H1('QCs')

mod_dropdown_qc = dcc.Dropdown(
    id="mod_dropdown_qc",
    placeholder="omics data",
    className="guimov_dropdown",
)

tooltip_mod_dropdown_qc = dbc.Tooltip(
    "Features type",
    target="mod_dropdown_qc",
    placement="right",
    className="guimov_tooltip",
)


histplot_qc = dcc.Graph(
    id='histplot_qc',
    figure=px.histogram(
        tl.iris, x='sepal_length'
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color),
)

boxplot_qc = dcc.Graph(
    id='boxplot_qc',
    figure=px.box(
        tl.iris, y='sepal_length', x="species"
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color),
)

use_gene_Y_qc = daq.ToggleSwitch(
    id="use_gene_Y_qc",
    label='Gene for X or Y axis',
    labelPosition='left',
    value=False,
    className="guimov_toggle",
)

tooltip_use_gene_Y_qc = dbc.Tooltip(
    "When a gene is selected "
    "you can display his expression on Y axis or on X axis",
    target="use_gene_Y_qc",
    placement="right",
    className="guimov_tooltip",
)

use_overlay_qc = daq.ToggleSwitch(
    id="use_overlay_qc",
    label='display Overlay',
    labelPosition='left',
    value=True,
    className="guimov_toggle",
)

tooltip_use_overlay_qc = dbc.Tooltip(
    "Show groups stacked or one behind the other",
    target="use_overlay_qc",
    placement="right",
    className="guimov_tooltip",
)

obs_num_qc = dcc.Dropdown(
    id="obs_num_qc",
    placeholder="numerical observations",
    className="guimov_dropdown",
)

tooltip_obs_num_qc = dbc.Tooltip(
    "Select a numerical metadata (continues values) to display on graphs "
    "(display on second graph if any gene are selected or if gene expression "
    "is display on Y axis).",
    target="obs_num_qc",
    placement="right",
    className="guimov_tooltip",
)

var_gene_qc = dcc.Dropdown(
    id="var_gene_qc",
    placeholder="Genes expression",
    className="guimov_dropdown",
)

tooltip_var_gene_qc = dbc.Tooltip(
    "Select a gene to explore his expression "
    "(write the first letter to show all options of the dropdown)",
    target="var_gene_qc",
    placement="right",
    className="guimov_tooltip",
)

y_num_qc = dcc.Dropdown(
    id="y_num_qc",
    placeholder="Y axe, default : count",
    className="guimov_dropdown",
)

tooltip_y_num_qc = dbc.Tooltip(
    "Select a numerical metadata to display when gene expression is display on X axis",
    target="y_num_qc",
    placement="right",
    className="guimov_tooltip",
)

opacity_qc = dcc.Slider(
    id='opacity_qc',
    min=0,
    max=1,
    step=0.1,
    marks={0: '0%', 0.50: '50%', 1: '100%'},
    value=1,
    className="guimov_slider",
)

tooltip_opacity_qc = dbc.Tooltip(
    "When groups are display one behind the other, "
    "it can be useful to change the opactiy of all groups.",
    target="opacity_qc",
    placement="right",
    className="guimov_tooltip",
)

obs_cat_qc = dcc.Dropdown(
    id="obs_cat_qc",
    placeholder="categorical observations",
    className="guimov_dropdown",
)

tooltip_obs_cat_qc = dbc.Tooltip(
    "Select a categorical metadata (clusters, sample, etc)"
    " to display on both graphs.",
    target="obs_cat_qc",
    placement="right",
    className="guimov_tooltip",
)
