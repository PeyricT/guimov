from pandas.api.types import is_string_dtype, is_numeric_dtype, is_categorical_dtype
import numpy as np
from urllib import request
import anndata as ad
from os.path import exists


from .._settings import settings
from .anndata_loading import *
from .mudata_loading import *

from .._utils import tools as tl
from .._main_callbacks import write_log

import scanpy as sc

def check_hash(code):
    """
    Call to check if code provide a datasets. Load datasets if not already loaded.
    :param code:
    :return bool:
    """
    if code == '8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762':
        if not exists(settings.datasets_path+'spatial.h5ad'):
            write_log(f'downloading spatial demo datasets', 'GUIMOV-system', '-1')
            sc.datasets.visium_sge(sample_id="V1_Human_Lymph_Node").write(settings.datasets_path+'spatial.h5ad')
        else:
            write_log(f'loading spatial demo datasets', 'GUIMOV-system', '-1')
        tl.datasets[code] = {'rna': ad.read_h5ad(settings.datasets_path+'spatial.h5ad')}
        tl.datasets[code]['rna'].uns['dataset_name'] = 'pbmc3k'

        return True

    it = tl.datasets_hash.get(code)
    if it is None:
        return False

    extension = it.split(".")[-1]

    if extension == 'h5mu':
        if tl.datasets.get(code) is None:
            write_log(f'Loading {it}', 'GUIMOV-system', '-1')
            tl.datasets[code] = mudata_load(tl.datasets_path+"/"+it)

    elif extension == 'h5ad':
        if tl.datasets.get(code) is None:
            write_log(f'Loading {it}', 'GUIMOV-system', '-1')

            names = it.split(';')
            if len(names) > 1:
                tl.datasets[code] = multiple_anndata_load(tl.datasets_path+"/", names)
            else:
                tl.datasets[code] = anndata_load(tl.datasets_path+"/"+it)

    else:
        raise ValueError(f'Extension file `{extension}` is not handle.')

    if 'dataset_name' not in next(iter(tl.datasets.get(code).values())).uns.keys():
        next(iter(tl.datasets.get(code).values())).uns['dataset_name'] = it

    return True


def get_infos(code):
    """
    Sparse dataset to get informations : The numbers and the list of all observations, varaibles, etc.
     according feature_types
    :param code:
    :return dict(), dict():
    """
    dataset = tl.datasets.get(code)
    if dataset is None:
        raise ValueError('Key not found among the datasets')

    infos = {}
    obs = {}
    default_values = {}
    for mod, value in dataset.items():
        obs[mod] = parse_data(value, infos)
        infos['mod'].append(mod)

        default_values[mod] = {}
        for inf, val in obs[mod].items():
            default_values[mod][inf] = val[0] if val else None
        default_values[mod]['n_obs_categorical_2'] = \
            obs[mod]['n_obs_categorical'][1] if len(obs[mod]['n_obs_categorical']) > 1 else None

    default_mod = infos['mod'][0]
    return infos, obs, default_mod, default_values


def parse_data(data, infos):
    # Overview's information
    if not infos:
        infos['mod'] = []
        infos['dataset_name'] = data.uns['dataset_name']
        infos['feature_types'] = [data.var['feature_types'][0]]
        infos['n_cells'] = [data.shape[0]]
        infos['n_genes'] = [data.shape[1]]
        infos['n_embeddings'] = [len(data.obsm)]
        infos['n_obs_categorical'] = [0]
        infos['n_obs_numerical'] = [0]
        infos['n_var_categorical'] = [0]
        infos['n_var_numerical'] = [0]
        infos['n_rank_test'] = [0]
        infos['raw'] = [0]
        infos['layers'] = [0]

    else:
        infos['feature_types'].append(data.var['feature_types'][0])
        infos['n_cells'].append(data.shape[0])
        infos['n_genes'].append(data.shape[1])
        infos['n_embeddings'].append(len(data.obsm))
        infos['n_obs_categorical'].append(0)
        infos['n_obs_numerical'].append(0)
        infos['n_var_categorical'].append(0)
        infos['n_var_numerical'].append(0)
        infos['n_rank_test'].append(0)
        infos['raw'].append(0)
        infos['layers'].append(0)

    # store useful informations for an easier use later
    observations = {
        'n_obs_categorical': [],
        'n_obs_numerical': [],
        'n_obs_string': [],

        'n_var_categorical': [],
        'n_var_numerical': [],
        'n_var_string': [],

        'rank_test': [],
        'layers': [],

    }

    if isinstance(data, mu.MuData):
        observations['n_embeddings'] = list(set(data.obsm.keys()) - set(data.mod.keys()))
    else:
        observations['n_embeddings'] = list(data.obsm.keys())

    if data.raw is not None:
        infos['raw'][-1] = 1

    if data.layers is not None:
        for layer in data.layers:
            infos['layers'][-1] += 1
            observations['layers'].append(layer)

    # split numerical, categorical, and string data
    for col in data.obs.columns:
        if is_categorical_dtype(data.obs[col].dtype):
            infos['n_obs_categorical'][-1] += 1
            observations['n_obs_categorical'].append(col)

        elif is_numeric_dtype(data.obs[col].dtype):
            infos['n_obs_numerical'][-1] += 1
            observations['n_obs_numerical'].append(col)

        elif is_string_dtype(data.obs[col].dtype):
            observations['n_obs_string'].append(col)

    for col in data.var.columns:
        if is_categorical_dtype(data.var[col].dtype):
            infos['n_var_categorical'][-1] += 1
            observations['n_var_categorical'].append(col)

        elif is_numeric_dtype(data.var[col].dtype):
            infos['n_var_numerical'][-1] += 1
            observations['n_var_numerical'].append(col)

        elif is_string_dtype(data.var[col].dtype):
            observations['n_var_string'].append(col)

    # gather rank test
    # they don't have caracteristic name, or location
    # so we have to check the values inside each key in uns
    for key, items in data.uns.items():
        if isinstance(items, dict):
            if np.array([tab in items.keys() for tab in
                         ['names', 'pvals', 'scores', 'logfoldchanges', 'pvals_adj']]).all():
                observations['rank_test'].append(key)
                infos['n_rank_test'][-1] += 1

    return observations


