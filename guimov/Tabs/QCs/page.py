from .elements import *


layout = html.Div(
    className="guimov_layout_qc",
    children=[
        # tab_title,
        html.Div(
            className="guimov_parameters_1_qc",
            children=[
                mod_dropdown_qc,
                tooltip_mod_dropdown_qc,
                use_overlay_qc,
                tooltip_use_overlay_qc,
                use_gene_Y_qc,
                tooltip_use_gene_Y_qc,
                obs_num_qc,
                tooltip_obs_num_qc,
                var_gene_qc,
                tooltip_var_gene_qc,
                y_num_qc,
                tooltip_y_num_qc,
                opacity_qc,
                tooltip_opacity_qc,
            ]
        ),
        html.Div(
            className="guimov_graphics_1_qc",
            children=[
                histplot_qc,
            ]
        ),
        html.Div(
            className="guimov_parameters_2_qc",
            children=[
                obs_cat_qc,
                tooltip_obs_cat_qc,
            ]
        ),
        html.Div(
            className="guimov_graphics_2_qc",
            children=[
                boxplot_qc,
            ]
        )
    ],
)
