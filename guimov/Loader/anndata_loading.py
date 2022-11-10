import anndata as ad


def anndata_load(path, name=None):
    """
    Laod anndata datasets, send dict according feature_types
    :param path:
    :param name:
    :return dict(type: anndata):
    """
    adata = ad.read_h5ad(path)
    if 'feature_types' not in adata.var.columns:
        raise TypeError('`feature_types` is required in .var')

    if (adata.var['feature_types'] == 'Peaks').all():
        _type = 'atac'
        if name:
            _type = _type + '_' + name

    elif (adata.var['feature_types'] == 'Gene Expression').all():
        _type = 'rna'
        if name:
            _type = _type + '_' + name

    else:
        if (adata.var['feature_types'] == adata.var['feature_types'][0]).all():
            raise TypeError(f'{adata} contain {adata.var["feature_types"][0]} feature_types which is not supported.')

        else:
            raise TypeError(f'multiples feature_types in {adata} AnnData files is not supported.'
                            f'Please use Muon package instead')

    return {_type: adata}


def multiple_anndata_load(path, datasets_name):
    ret = {}
    for data_name in datasets_name:
        ret.update(anndata_load(path+data_name, data_name.split('.')[0]))

    return ret
