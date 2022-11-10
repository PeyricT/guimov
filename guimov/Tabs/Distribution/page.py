from .elements import *


layout = html.Div(
    className="guimov_tabs_layout",
    children=[
        html.Div(
            className="guimov_container",                   # first container
            children=[
                html.Div(
                    className="guimov_parameters",
                    children=[
                        mod_dropdown_di,
                        tooltip_mod_dropdown_di,
                        obs1_cat_di,
                        tooltip_obs1_cat_di,
                        obs2_cat_di,
                        tooltip_obs2_cat_di,
                    ]
                ),
                html.Div(
                    className="guimov_graphics",
                    children=[
                        sankey_plot_di,
                    ]
                )
            ]
        ),
    ],
)
