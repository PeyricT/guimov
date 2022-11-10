from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash
import time as t
import datetime
import gc

import threading
from guimov._settings import settings
from guimov._utils import tools as tl


def start_threaded_functions():
    """
    Start checkin users function only the second launch, (debug mode launch code twice)
    :return:
    """
    f = open('../datasets/buffer', 'r')
    if f.read()[0] == '0':
        f.close()
        f2 = open('../datasets/buffer', 'w')
        f2.write('1')
        f2.close()
        write_log('Start user disconection system (1/2)', 'GUIMOV-system', '-1')
    else:
        f3 = open('../datasets/buffer', 'w')
        f3.write('0')
        f3.close()
        write_log('Start user disconection system (2/2)', 'GUIMOV-system', '-1')
        threaded_functions()


def threaded_functions():
    check_disconnection()
    update_datasets()

    threading.Timer(60, threaded_functions).start()


def update_datasets():
    if tl.single_dataset or tl.datasets_hash is None:
        return

    temp = dict()
    in_use = dict()
    with open(settings.datasets_path, 'r') as hashf:
        for line in hashf:
            if line.strip() != "":
                data, hashd = line.strip().split('\t')
                temp[hashd] = data
                in_use[hashd] = []

    temp['8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762'] = 'pbmc3k.h5ad'
    in_use['8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762'] = []

    if temp == tl.datasets_hash:
        return

    for key, item in tl.datasets_hash.items():
        if temp.get(key) is None or temp[key] != item:
            if tl.datasets.get(key) is not None:
                del tl.datasets[key]
            del tl.datasets_in_use[key]
        else:
            in_use[key] = tl.datasets_in_use[key].copy()

    tl.datasets_hash = temp
    tl.datasets_in_use = in_use

    write_log('datasets library has been updated', 'GUIMOV-system', '-1')



def check_disconnection():
    """
    Check the last time a user has send a ping. If 2 pings are missing, the user is consider inactive,
    the session, and if he not used , the dataset will be cleared.
    :return:
    """
    inactive_id = []
    for _id, user in tl.users_timer.items():
        if _id == 'current_users':
            continue
        if user['last_check'] < 0:
            continue

        if t.time()*1000 - user['last_check'] > 120 * 1000:    # en milliseconds
            for code, data_users in tl.datasets_in_use.items():
                if _id in data_users:
                    ind = tl.datasets_in_use[code].index(_id)
                    del tl.datasets_in_use[code][ind]

                    if not tl.datasets_in_use[code]:
                        del tl.datasets[code]  # unload datasets
                        write_log(f'Unloading {tl.datasets_hash[code]}', 'GUIMOV-system', '-1')
                        gc.collect()  # free memory

                    break

            inactive_id.append(_id)

        else:
            pass  # ancien print

    if inactive_id:
        inactive_ip = [tl.users_timer[in_id]['ip'] for in_id in inactive_id]
        messages = ['Leave the interface']*len(inactive_id)
        write_log(messages, inactive_ip, inactive_id)
        for in_id in inactive_id:
            del tl.users_timer[in_id]


@tl.app.callback(
    Output('disconnected', 'displayed'),
    Input('interval-timer', 'n_intervals'),
    State('session', 'data'),
    prevent_initial_call=True,
)
def check_user_activity(_, session):
    """
    Update when a user send a ping, if no figure are update for more than 15min, the user is consider inactive,
    the session, and if he not used , the dataset will be cleared.
    :param _:
    :param session:
    :return:
    """
    if session is None or session.get('code') is None or tl.users_timer[session['id']]['last_update'] < 0:
        raise PreventUpdate

    tl.users_timer[session['id']]['last_check'] = round(t.time()*1000)
    time_from_last_update = t.time() * 1000 - tl.users_timer[session['id']]['last_update']  # en milliseconds

    if time_from_last_update > 45 * 60 * 1000:    # 45min
        tl.users_timer[session['id']]['last_update'] = -1
        tl.users_timer[session['id']]['last_check'] = -1
        write_log('Is an inactive user', session['ip'], session['id'])
        clean_datasets(session['code'], session['id'])

        return True

    return False


def clean_datasets(code: str, _id: int):
    """
    Call when a user is detected inactive, clear dict, and check if datasets is still use,
    if not, the datasets will be cleared.
    :param code:
    :param _id:
    :return:
    """
    if tl.datasets.get(code) is None:
        return

    try:
        ind = tl.datasets_in_use[code].index(_id)
        del tl.datasets_in_use[code][ind]
    except ValueError:
        raise ValueError(f"{_id} not found in the list of current datasets users.\n{tl.datasets_in_use}")

    if not tl.datasets_in_use[code]:
        write_log(f'Unloading {tl.datasets_hash[code]}', 'GUIMOV-system', '-1')
        del tl.datasets[code]  # unload datasets
        gc.collect()  # free memory


@tl.app.callback(
    Output('Embedding_tab', 'className'),
    Output('QCs_tab', 'className'),
    Output('Distribution_tab', 'className'),
    Output('GeneDiff_tab', 'className'),
    Output('Pathways_tab', 'className'),
    Output('Clustering_tab', 'className'),
    Output('Options_tab', 'className'),
    Output('input_code_ov', 'className'),
    State('session', 'data'),
    Input('session', 'modified_timestamp')
)
def update_tab_access(session, _):
    """
    Call when a user load a dataset, according the datasets, tabs will be accessible or not.
    :param session:
    :param _:
    :return:
    """
    if session is None or session.get('code') is None:
        raise PreventUpdate
    input_code_class = 'guimov_input_disable' if tl.single_dataset else 'guimov_input'
    return None, None, None, None, None, None, dash.no_update, input_code_class


def write_log(message, ip, session_id):
    """
    Call to write log and print message.
    :param message:
    :param ip:
    :param session_id:
    :return:
    """

    if tl.single_dataset:
        return

    date = datetime.datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")

    if isinstance(message, str):
        log = f"{date}\t{ip}\t{session_id}\t{message}\n"
        with tl.lock, open(settings.logs_path, 'a') as log_file:
            log_file.write(log)
            print(log, end="")

    elif isinstance(message, list):
        logs = [f"{date}\t{ip[k]}\t{session_id[k]}\t{message[k]}\n" for k in range(len(message))]
        with tl.lock, open(settings.logs_path, 'a') as log_file:
            for log in logs:
                log_file.write(log)
                print(log, end="")
