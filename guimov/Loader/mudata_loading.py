import muon as mu


def mudata_load(path):
    """
    Laod mudata datasets, send dict according feature_types
    :param path:
    :return dict(type: anndata):
    """
    mudata = mu.read_h5mu(path)

    # contrairement à Anndata, Mudata n'as pas d'attribut _uns
    mudata._uns = mudata.uns

    ret = {'muon': mudata}

    for adata in mudata.mod.values():
        if 'feature_types' not in adata.var.columns:
            raise TypeError('`feature_types` is required in .var')

        if (adata.var['feature_types'] == 'Peaks').all():
            ret['atac'] = adata

        elif (adata.var['feature_types'] == 'Gene Expression').all():
            ret['rna'] = adata

        else:
            if (adata.var['feature_types'] == adata.var['feature_types'][0]).all():
                raise TypeError(f'{adata} contain {adata.var["feature_types"][0]} feature_types which is not supported.')

            else:
                raise TypeError(f'multiples feature_types in {adata} AnnData files is not supported.'
                                f'Please use Muon package instead')

    return ret
