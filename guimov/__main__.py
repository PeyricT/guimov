from dash import html, dcc
from guimov._utils import tools
from guimov._main_callbacks import threaded_functions
from guimov.Tabs import *
import logging


def start(*args, **kwargs):
    """Start the interface

    :param str host: IP to access the interface .Default '0.0.0.0'
    :param str port: Port to access the interface. Default '8585'
    :param bool debug: Launch the interface with debug mode. Default False
    :param str dataset: Use for explore only one dataset without providing datasets_path and logs_path
    :param args: Parameters pass to Dash.app.run_server
    :param kwargs: Parameters pass to Dash.app.run_server
    :return:
    """

    # Main layout
    tools.app.layout = html.Div(
        className="guimov_main",
        children=[
            html.Div(
                'GUIMOV app development',
                className='guimov_H1',
            ),
            dcc.Store(id='session', storage_type='session'),
            dcc.Store(id='clusters_temp', storage_type='session'),
            dcc.Interval(
                id='interval-timer',
                interval=60 * 1000,  # in milliseconds
                n_intervals=0
            ),
            dcc.ConfirmDialog(
                id='disconnected',
                message='You have been inactive for more than 45 min !'
                        '\nYou were automatically disconnected, please reload the dataset',
            ),
            dcc.Download(
                id='downlaod_image'
            ),
            dcc.Download(
                id='downlaod_table_csv'
            ),
            dcc.Tabs(
                className="guimov_tabs",
                parent_className="guimov_parent_tabs",
                content_className="guimov_content_tabs",
                value='Overview_tab',
                children=[
                    # Before loading a datasets only Overview layout is accessible
                    # others are disabled with className='guimov_disabled'
                    dcc.Tab(id='Overview_tab', label='Overview', value='Overview_tab',
                            children=layout_ov, ),
                    dcc.Tab(id='QCs_tab', label='QCs', value='QCs_tab',
                            children=layout_qc, className='guimov_disabled', ),
                    dcc.Tab(id='Embedding_tab', label='Embedding', value='Embedding_tab',
                            children=layout_em, className='guimov_disabled'),
                    dcc.Tab(id='Distribution_tab', label='Distribution', value='Distribution_tab',
                            children=layout_di, className='guimov_disabled', ),
                    dcc.Tab(id='GeneDiff_tab', label='Genes Diff', value='GeneDiff_tab',
                            children=layout_gd, className='guimov_disabled', ),
                    dcc.Tab(id='Pathways_tab', label='Pathways', value='Pathways_tab',
                            children=layout_pa, className='guimov_disabled', ),
                    dcc.Tab(id='Clustering_tab', label='Clustering', value='Clustering_tab',
                            children=layout_cl, className='guimov_disabled', ),
                    dcc.Tab(id='Options_tab', label='Options', value='Options_tab',
                            children=layout_op, className='guimov_disabled', ),
                ],
                vertical=True,

                # not working :(
                persistence=True,
                persistence_type='session',
            )
        ]
    )
    # remove log from Flask serveur
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    # start the fonction which check users activities
    threaded_functions()
    tools.start_app(*args, **kwargs)


if __name__ == '__main__':
    start(host='0.0.0.0', port='8050')
