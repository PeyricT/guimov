from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html
import dash

from guimov._utils import tools as tl
from guimov._main_callbacks import clean_datasets, write_log
import time as t
import hashlib as hb

from guimov.Loader import check_hash, get_infos
from flask import request


@tl.app.callback(Output('session', 'data'),
                  Output('alert_ov', 'is_open'),
                  Output('alert_ov', 'children'),
                  Output('alert_ov', 'className'),
                  Output('loading_div_ov', 'children'),
                  State('session', 'data'),
                  Input('input_code_ov', 'value'),
                  Input('update_from_cl', 'children'),
                  Input('update_from_pa', 'children'),
                  Input('update_from_em', 'children'),
                  Input('loading_div_ov', 'children'),
                  # Input('session', 'modified_timestamp'),
                  Input('disconnected', 'submit_n_clicks'),
                  Input('disconnected', 'cancel_n_clicks'),)
def check_code(session, code, cluster_update, pathways_update, de_update, *_):
    """
    Call when user input a code, load dataset if needed, then store code in dcc.Store to be user in
    other functions to acces a unique dataset.
    :param session:
    :param code:
    :param cluster_update:
    :param pathways_update:
    :param de_update:
    :param _:
    :return:
    """
    # get context from callbacks
    ctx = dash.callback_context
    alert_is_open = dash.no_update
    alert_children = dash.no_update
    alert_className = dash.no_update

    if tl.single_dataset:
        if tl.demo:
            code = 'demo'
        else:
            code = 'dataset'

    if code is not None:
        code = hb.sha224(code.encode('utf-8')).hexdigest()

    if session is None:
        # at the beginning of session
        session = {'id': tl.users_timer['current_users'], 'ip': request.remote_addr}
        tl.users_timer['current_users'] += 1
        tl.users_timer[session['id']] = {
            'ip': session['ip'],
            'first_update': round(t.time() * 1000),
            'last_update': -1,
            'last_check': -1,
        }
        write_log('Connexion', session['ip'], session['id'])

    if ctx.triggered[0]["prop_id"] == "disconnected.submit_n_clicks" or \
       ctx.triggered[0]["prop_id"] == "disconnected.cancel_n_clicks":
        # if inactive, disconnected submit or cancel will be send here
        del session['code']
        del session['infos']
        del session['obs']
        session['reload'] = 'Update'
        
    elif ctx.triggered[0]['prop_id'] == 'update_from_pa.children':
        pathway, mod = pathways_update.split(';')
        session['obs'][mod]['n_obs_numerical'].append(pathway)
        session['reload'] = 'pathways'
    
    elif ctx.triggered[0]['prop_id'] == 'update_from_cl.children':
        cluster, mod = cluster_update.split(';')
        session['obs'][mod]['n_obs_categorical'].append(cluster)
        session['reload'] = 'clusters'

    elif ctx.triggered[0]['prop_id'] == 'update_from_em.children':
        de_name, mod = de_update.split(';')
        session['obs'][mod]['rank_test'].append(de_name)
        session['reload'] = 'de'

    if code is not None and check_hash(code):
        session['reload'] = 'Update'

        if session.get('code') is not None and session['code'] != code:
            # if user has already load a dataset
            clean_datasets(session['code'], session['id'])
            del session['code']
            del session['infos']
            del session['obs']

        if session.get('code') is None:
            # load a dataset and get his informations
            write_log(f'Grant acces to {tl.datasets_hash[code]}', session['ip'], session['id'])
            tl.datasets_in_use[code].append(session['id'])
            session['infos'], session['obs'], session['default_mod'], session['default_values'] = get_infos(code)
            session['code'] = code
            tl.users_timer[session['id']]['last_update'] = round(t.time() * 1000)
            tl.users_timer[session['id']]['last_check'] = round(t.time() * 1000)

            alert_is_open = True
            alert_children = f"Dataset {tl.datasets_hash[code]} successfully loaded."
            alert_className = "guimov_info"

        else:
            alert_is_open = True
            alert_children = f"This dataset is already loaded."
            alert_className = "guimov_alert"

    # hash du string vide ''
    elif code != 'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f' and code is not None:
        alert_is_open = True
        alert_children = f"Wrong password, try another one."
        alert_className = "guimov_alert"

    return session, alert_is_open, alert_children, alert_className, None


@tl.app.callback(
              Output('input_code_ov', 'value'),
              Output('label_filename_ov', 'children'),
              Output('label_featuretypes_ov', 'children'),
              Output('label_genebycell_ov', 'children'),
              Output('label_embeddings_ov', 'children'),
              Output('label_observations_cat_ov', 'children'),
              Output('label_variables_cat_ov', 'children'),
              Output('label_observations_num_ov', 'children'),
              Output('label_variables_num_ov', 'children'),
              Output('label_ranktest_ov', 'children'),
              State('session', 'data'),
              Input('session', 'modified_timestamp'))
def update_label_ov(session, _):
    """
    Display informations from newly loaded dataset
    :param session:
    :param _:
    :return:
    """
    if session is None or session.get('code') is None:
        raise PreventUpdate

    label_filename = f"○  {session['infos']['dataset_name']}"
    label_featuretypes = []
    label_genebycell = []
    label_embeddings = []
    label_ranktest = []
    label_observations_cat = []
    label_variables_cat = []
    label_observations_num = []
    label_variables_num = []

    for k in range(len(session['infos']['feature_types'])):
        label_featuretypes.append(f"○  {session['infos']['mod'][k]}: {session['infos']['feature_types'][k]}")
        label_genebycell.append(f"○  {session['infos']['n_genes'][k]} genes by {session['infos']['n_cells'][k]} cells")
        label_embeddings.append(f"○  {session['infos']['n_embeddings'][k]}")
        label_observations_cat.append(f"○  {session['infos']['n_obs_categorical'][k]}")
        label_variables_cat.append(f"○  {session['infos']['n_var_categorical'][k]}")
        label_observations_num.append(f"○  {session['infos']['n_obs_numerical'][k]}")
        label_variables_num.append(f"○  {session['infos']['n_var_numerical'][k]}")
        label_ranktest.append(f"○  {session['infos']['n_rank_test'][k]}")

        label_featuretypes.append(html.Br())
        label_genebycell.append(html.Br())
        label_embeddings.append(html.Br())
        label_observations_cat.append(html.Br())
        label_variables_cat.append(html.Br())
        label_observations_num.append(html.Br())
        label_variables_num.append(html.Br())
        label_ranktest.append(html.Br())

    return "", \
           label_filename, \
           label_featuretypes,\
           label_genebycell,\
           label_embeddings,\
           label_observations_cat,\
           label_variables_cat,\
           label_observations_num,\
           label_variables_num,\
           label_ranktest
