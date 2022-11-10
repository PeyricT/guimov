from dash import dcc, html
import dash_bootstrap_components as dbc
from guimov._utils import tools as tl, plot_sankey


sankey_plot_di = dcc.Graph(
    id='sankey_plot_di',
    figure=plot_sankey(
        tl.iris, source="species", target="size"
    ).update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color),
)

mod_dropdown_di = dcc.Dropdown(
    id="mod_dropdown_di",
    placeholder="omics data",
    className="guimov_dropdown",
)

tooltip_mod_dropdown_di = dbc.Tooltip(
    "Features type",
    target="mod_dropdown_di",
    placement="right",
    className="guimov_tooltip",
)

obs1_cat_di = dcc.Dropdown(
    id="obs1_cat_di",
    placeholder="observation source",
    className="guimov_dropdown",
)

tooltip_obs1_cat_di = dbc.Tooltip(
    "Select the first categorical metadata (clusters, sample, etc)",
    target="obs1_cat_di",
    placement="right",
    className="guimov_tooltip",
)

obs2_cat_di = dcc.Dropdown(
    id="obs2_cat_di",
    placeholder="observation target",
    className="guimov_dropdown",
)

tooltip_obs2_cat_di = dbc.Tooltip(
    "Select the second categorical metadata (clusters, sample, etc)",
    target="obs2_cat_di",
    placement="right",
    className="guimov_tooltip",
)

