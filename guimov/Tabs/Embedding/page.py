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
                        mod_dropdown_em,
                        tooltip_mod_dropdown_em,
                        embedding_dropdown_em,
                        tooltip_embedding_dropdown_em,
                        factor_dropdown_em,
                        tooltip_factor_dropdown_em,
                        gene_name_em,
                        tooltip_gene_name_em,
                        use_3d_em,
                        tooltip_use_3d_em,
                        pct_cells_em,
                        tooltip_pct_cells_em,
                        points_size_em,
                        tooltip_points_size_em,
                        pct_obs_em,
                        tooltip_pct_obs_em,
                        pct_alpha_em,
                        tooltip_pct_alpha_em,
                        html.Br(),
                        html.Br(),
                        save_svg_em,
                        tooltip_save_svg_em,
                        loading_em,
                        alert_em,
                        update_from_em,
                    ]
                ),
                html.Div(
                    className="guimov_graphics",
                    children=[
                        umap_em,
                        cells1_selection_em,
                        tooltip_cells1_selection_em,
                        cells2_selection_em,
                        tooltip_cells2_selection_em,
                        de_name_em,
                        compute_de_em,
                        tooltip_compute_de_em,
                    ]
                )
            ]
        ),
    ],
)
