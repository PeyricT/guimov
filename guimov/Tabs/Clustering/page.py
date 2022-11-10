from .elements import *


layout = html.Div(
    className="guimov_layout_cl",
    children=[
        # tab_title,
        html.Div(
            className="guimov_parameters_1_qc",
            children=[
                mod_dropdown_cl,
                tooltip_mod_dropdown_cl,
                embedding_dropdown_cl,
                tooltip_embedding_dropdown_cl,
                res_dropdown_cl,
                tooltip_res_dropdown_cl,
                res2_dropdown_cl,
                tooltip_res2_dropdown_cl,
                pct_cells_cl,
                tooltip_pct_cells_cl,
                points_size_cl,
                tooltip_points_size_cl,
                update_from_cl,
            ]
        ),
        html.Div(
            className="guimov_graphics_1_qc",
            children=[
                umap_cl,
            ]
        ),
        html.Div(
            className="guimov_parameters_2_qc",
            children=[
                input_res_cl,
                tooltip_input_res_cl,
                compute_cl,
                tooltip_compute_cl,
                save_clustering_cl,
                tooltip_save_clustering_cl,
                loading_cl,
            ]
        ),
        html.Div(
            className="guimov_graphics_2_qc",
            children=[
                sankey_plot_cl,
            ]
        )
    ],
)
