# Import layout from all tabs
from .Embedding.page import layout as layout_em
from .Overview.page import layout as layout_ov
from .QCs.page import layout as layout_qc
from .Distribution.page import layout as layout_di
from .Options.page import layout as layout_op
from .GeneDiffs.page import layout as layout_gd
from .Pathways.page import layout as layout_pa
from .Clustering.page import layout as layout_cl

# Import callbacks from all tabs
from .Embedding.callbacks import (
    update_umap, selected_data, update_mod, update_parameters, update_gene_name, download_em,
)
from .Overview.callbacks import (
    check_code, update_label_ov,
)
from .QCs.callbacks import (
    update_histplot, update_boxplot, update_mod, update_parameters, update_gene_name
)
from .Distribution.callbacks import (
    update_sankey_plot, update_mod, update_parameters
)
from .GeneDiffs.callbacks import (
    update_table, export_table, update_heatmap, update_mod, update_rank_genes, update_rank_genes
)
from .Pathways.callbacks import (
    update_mod, update_gene_name, update_table, run_pathway,
)
from .Clustering.callbacks import (
    update_umap, update_sankey_plot, update_mod, update_parameters, compute_clustering, load_clustering,
)

__all__ = [
    'layout_em',
    'layout_ov',
    'layout_qc',
    'layout_di',
    'layout_op',
    'layout_gd',
    'layout_pa',
    'layout_cl',
    'update_umap', 'selected_data', 'update_mod', 'update_parameters', 'update_gene_name', 'download_em',
    'check_code', 'update_label_ov',
    'update_histplot', 'update_boxplot', 'update_mod', 'update_parameters', 'update_gene_name',
    'update_sankey_plot', 'update_mod', 'update_parameters',
    'update_table', 'export_table', 'update_heatmap', 'update_mod', 'update_rank_genes', 'update_rank_genes',
    'update_mod', 'update_gene_name', 'update_table', 'run_pathway',
    'update_umap', 'update_sankey_plot', 'update_mod', 'update_parameters', 'compute_clustering', 'load_clustering',
]
