Datasets requirements
=====================

GUIMOV use Anndata_ format to read singlecell datasets. It's the great choice for is
standardization in Python algorithms. The interface is mainly use to read Scanpy_ and
Muon_ output.

However few algorithms exist to turn Seurat or SingleCellExperiement data into Anndata. We
recommand to use ower own converter SinglecellConverter_.

Be aware that most of warnings we ask you to be careful about, are mostly cause by
converting Seurat and SinglecellExperiment in Anndata format. Scanpy and Muon algorithms
don't trigger theses warnings.

Anndata format
--------------

GUIMOV is made to get most of the informations in Anndata file automatically. If you respect
Anndata standard The interface will suggest all calculated embeddings
(store as 'X_NameOfReductions' like 'X_pca' or 'X_umap') or all metadata from cells or genes.

Nethertheless it still remain some specific format to store data in Anndata. In order to
acces to all your data, be aware about the following caracteristics require by GUIMOV.

⚠️
    The Anndata format is undergoing a big update. The main matrix `X` will be merged
    with the dictionary containing the other optional matrices `layers`.
    The upgrade will take place over several months or years, but it will be necessary
    to make changes to take it into account.

⚠️
    Some functions as Rank test need log-normalise data without scaling. For the GUIMOV's tools
    we recommand to put the log-normalise matrix in layer 'Normalise' if you want to scale the main matrix.

Dataframe
-----------

Anndata store all the metadata in Dataframe from pandas_. For cells in '.obs' and  for genes
in '.var'.

⚠️
    The Anndata or Mudata file must contain the `feature_types` key in `.var`
    for the given type ('Gene Expression', 'atac', 'prot') to be recognized by
    GUIMOV. Otherwise the program will return an error message.

⚠️
    GUIMOV use the different types of data stored in Observations `obs` and Variables `var`
    specificly. There are 3 types of data, numerical, factors, and strings.
    It is important to check that the resulting data from a clustering is factors.

Rank test
-----------

⚠️
    Marker genes are detected when the object in '.uns' is a dictionary which contains
    the keys 'names', 'pvals', 'scores', 'logfoldchanges' and 'pvals_adj'.
    By default the Scanpy rank test uses this format, however if marker genes
    are imported they must also be in this format. To display the heatmap correctly,
    the group used by the rank test must also be remembered; it is expected in
    `.uns[rank_test_name]['params']['groupby']`. This group must also be present
    under the same name in '.obs'

Others
-----------

⚠️
    A spatial dataset is read like a classical scRNAseq file with 2 differences.
    Firstly, the 'spatial' embeddings must be found in '.obsm'.
    Secondly the high quality image must be stored as a numpy matrix in
    '.uns['spatial'][nomdudataset]['images']['hires']`.
    It is also necessary to have the scale factor in
    `.uns['spatial'][nomdudataset]['scalefactors']['tissue_hires_scalef']`.


.. _Anndata: https://anndata.readthedocs.io/en/latest/
.. _Scanpy: https://scanpy.readthedocs.io/en/stable/
.. _Muon: https://muon.readthedocs.io/en/latest
.. _SinglecellConverter: https://gitlab.com/pfgt/sandbox/singlecellconverter
.. _pandas: https://pandas.pydata.org/docs/index.html

