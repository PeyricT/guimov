from .elements import *


layout = html.Div(
    className="guimov_tabs_layout",
    children=[
        tab_title,
        html.Div(
            className="guimov_container",                   # first container
            children=[
                html.Div(
                    className="guimov_parameters",
                    children=[
                        input_code_ov,
                        alert_ov,
                        loading_ov,
                        tooltip_ov,
                    ]
                ),
                html.Div(
                    className="guimov_overview_labels",
                    children=[
                        label_filename_ov,
                        label_genebycell_ov,
                        label_featuretypes_ov,
                        label_embeddings_ov,
                        label_observations_cat_ov,
                        label_observations_num_ov,
                        label_variables_cat_ov,
                        label_variables_num_ov,
                        label_ranktest_ov,
                    ]
                )
            ]
        ),
    ],
)
