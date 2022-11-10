import dash_bootstrap_components as dbc
from dash import html
from dash import dcc


tab_title = html.H2('Overview')

alert_ov = dbc.Alert(
    "Hello! I am an auto-dismissing alert!",
    id="alert_ov",
    is_open=False,
    duration=7000,
    className="guimov_info",
)

input_code_ov = dcc.Input(
    id="input_code_ov",
    type="password",
    placeholder="input code to acces your data",
    debounce=True,
    className="guimov_input",
 )

tooltip_ov = dbc.Tooltip(
    "Each dataset has a unique code, which is given by the bioinformatic team",
    target="input_code_ov",
    placement="right",
    className="guimov_tooltip",
)

loading_ov = dcc.Loading(
    id="loading_ov",
    className="guimov_loading",
    children=html.Div(
        id="loading_div_ov",
        children=None,
    ),
    type="circle",
)

label_filename_ov = html.Div(
    children=[
        html.P(
            'Filename  ',
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_filename_ov',
            className='guimov_info_caract_ov',
        )

    ],
    className="guimov_label_ov",
)

label_featuretypes_ov = html.Div(
    children=[
        html.P(
            'Feature types  ',
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_featuretypes_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_genebycell_ov = html.Div(
    children=[
        html.P(
            'Genes by Cells matrix  ',
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_genebycell_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_embeddings_ov = html.Div(
    children=[
        html.P(
            'Number of Embeddings  ',
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_embeddings_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_observations_num_ov = html.Div(
    children=[
        html.P(
            "Number of cell's numerical Observations  ",
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_observations_num_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_observations_cat_ov = html.Div(
    children=[
        html.P(
            "Number of cell's categorical Observations  ",
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_observations_cat_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_variables_num_ov = html.Div(
    children=[
        html.P(
            "Number of gene's numerical Observations  ",
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_variables_num_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_variables_cat_ov = html.Div(
    children=[
        html.P(
            "Number of gene's categorical Observations  ",
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id='label_variables_cat_ov',
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)

label_ranktest_ov = html.Div(
    children=[
        html.P(
            "Number of rank tests  ",
            className="guimov_title_caract_ov",
        ),
        html.P(
            children=None,
            id="label_ranktest_ov",
            className='guimov_info_caract_ov',
        )
    ],
    className="guimov_label_ov",
)
