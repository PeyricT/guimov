from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import time as t

from guimov._utils import tools as tl, plot_sankey


@tl.app.callback(
    Output('sankey_plot_di', 'figure'),
    Input('obs1_cat_di', 'value'),
    Input('obs2_cat_di', 'value'),
    State('mod_dropdown_di', 'value'),
    State('session', 'data'),
)
def update_sankey_plot(source, target, mod, session):
    if mod is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if source is None or target is None or source == target:
        raise PreventUpdate

    df = tl.datasets[session['code']][mod].obs
    fig = plot_sankey(df, source, target)
    fig.update_layout(plot_bgcolor=tl.background_color, paper_bgcolor=tl.background_color)

    tl.users_timer[session['id']]['last_update'] = round(t.time() * 1000)

    return fig


@tl.app.callback(
    Output('mod_dropdown_di', 'options'), Output('mod_dropdown_di', 'value'),
    Input('session', 'modified_timestamp'), State('session', 'data')
)
def update_mod(ts, session):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if session['reload'] != 'Update':
        raise PreventUpdate

    return [{'label': value, 'value': value} for value in session['infos']['mod']], session['default_mod']


@tl.app.callback(
    Output('obs1_cat_di', 'options'), Output('obs1_cat_di', 'value'),
    Output('obs2_cat_di', 'options'), Output('obs2_cat_di', 'value'),
    State('session', 'modified_timestamp'), State('session', 'data'),
    Input('mod_dropdown_di', 'value'),
)
def update_parameters(ts, session, mod):
    if ts is None or session is None or session.get('code') is None:
        raise PreventUpdate

    if mod is None:
        return \
            [], None, \
            [], None

    return \
        [{'label': value, 'value': value} for value in session['obs'][mod]['n_obs_categorical']], \
        session['default_values'][mod]['n_obs_categorical'], \
        [{'label': value, 'value': value} for value in session['obs'][mod]['n_obs_categorical']], \
        session['default_values'][mod]['n_obs_categorical_2']
