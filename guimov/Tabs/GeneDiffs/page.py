from .elements import *


layout = html.Div(
    className="guimov_layout_qc",
    children=[
        # tab_title,
        html.Div(
            className="guimov_parameters_1_qc",
            children=[
                mod_dropdown_gd,
                tooltip_mod_dropdown_gd,
                rank_test_gd,
                tooltip_rank_test_gd,
                clusters_gd,
                tooltip_clusters_gd,
                nb_genes_gd,
                tooltip_nb_genes_gd,
                export_all_gd,
                tooltip_export_all_gd,
            ]
        ),
        html.Div(
            className="guimov_graphics_1_qc",
            children=[
                table_gd,
            ]
        ),
        html.Div(
            className="guimov_parameters_2_qc",
            children=[
                loading_gd,
            ],
        ),
        html.Div(
            className="guimov_graphics_2_qc",
            children=[
                heatmap_gd,
            ]
        )
    ],
)
