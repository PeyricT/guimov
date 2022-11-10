import plotly.graph_objects as go
import plotly.express as px
from threading import Lock
import hashlib as hb
import pandas as pd
import numpy as np
import base64
import dash
import io

from guimov._settings import settings


class Tools:
    """
    Tools contain all variables share in the differents callbacks of GUIMOV.
    When the App is launch the Settings.datasets_path is read to extract metadata about
    the datasets.
    """
    def __init__(self):
        # Dash main object
        self.app = dash.Dash(__name__)
        # Use to set the mod of the interface
        self.single_dataset = False
        # use for default graphs
        self.iris = self.get_default_df()
        # use for figure
        self.background_color = "#FAFAFA"
        # loaded datasets
        self.datasets = {}
        # dict(code: datasets_path), dict(code: [users]), str(datasets_location)
        self.datasets_hash, self.datasets_in_use, self.datasets_path = None, None, None
        # dict for gather user information outside local session
        self.users_timer = {'current_users': 0}
        # lock for acces data in threadin function
        self.lock = Lock()

    def start_app(self, *args, dataset=None, **kwargs):
        if dataset is None:
            self.datasets_hash, self.datasets_in_use, self.datasets_path = self.setup_datasets()
        else:
            self.single_dataset = True
            self.datasets_hash = {'c3937e84165709073627378f2587ce845d5058dcc220e5993ee2501d': dataset.split('/')[-1]}
            self.datasets_in_use = {'c3937e84165709073627378f2587ce845d5058dcc220e5993ee2501d': []}
            self.datasets_path = '/'.join(dataset.split('/')[:-1])+'/'

        # start GUIMOVapp (default port='8050')
        self.app.run_server(*args, debug=False, **kwargs)

    @staticmethod
    def setup_datasets():
        """
        This function load the informations about datasets stored in datasets.txt
        This function load the informations about datasets stored in datasets.txt
        :return dict, dict, str:
        """
        tmp_hash = {}
        data_used = {}

        with open(settings.datasets_path, 'r') as hashf:
            for line in hashf:
                if line.strip() != "":
                    data, hashd = line.strip().split('\t')
                    tmp_hash[hashd] = data
                    data_used[hashd] = []

            tmp_hash['8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762'] = 'pbmc3k.h5ad'
            data_used['8b1c1c1eae6c650485e77efbc336c5bfb84ffe0b0bea65610b721762'] = []

        return tmp_hash, data_used, settings.datasets_path.replace('datasets.txt', '')

    @staticmethod
    def get_default_df():
        """
        Get 'iris' datasets and add some observation for default graph in GUIMOVapp
        :return DataFrame:
        """
        default_df = px.data.iris()  # iris is a pandas DataFrame
        default_df['species'] = default_df['species'].astype('category')
        default_df['size'] = pd.Series(['short' if l < 4 else 'long' for l in default_df['petal_length']]).astype(
            'category')
        return default_df


def plot_sankey(df, source, target):
    """
    Get the observation from a datasets to convert categorical data for Sankey figure
    :param df:
    :param source:
    :param target:
    :return Sankey_plot:
    """
    label = list(df[source].cat.categories)
    label += list(df[target].cat.categories)

    nb1 = len(df[source].cat.categories)
    translate_source = {v: i for i, v in enumerate(df[source].cat.categories)}
    translate_target = {v: i + nb1 for i, v in enumerate(df[target].cat.categories)}

    counts = {}
    splice = df[[source, target]]
    for i in range(df.shape[0]):
        v = tuple(splice.iloc[i])
        counts[v] = counts.get(v, 0) + 1

    node_value = list(counts.values())
    node_source = [translate_source[cl[0]] for cl in counts.keys()]
    node_target = [translate_target[cl[1]] for cl in counts.keys()]

    fig = go.Figure(data=[go.Sankey(
        orientation="v",
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
        ),
        link=dict(
            source=node_source,
            target=node_target,
            value=node_value,
        ))])

    return fig


def full_heatmap(adata, rank_test, nb_genes):
    #
    #   CREATE SUBPLOT
    #

    from plotly.subplots import make_subplots
    fig = make_subplots(rows=10, cols=2, column_widths=[0.04, 0.96], vertical_spacing=0.02, horizontal_spacing=0.01,
                        specs=[
                            [{'rowspan': 9}, {'rowspan': 9}],
                            [None, None, ],
                            [None, None, ],
                            [None, None, ],
                            [None, None, ],
                            [None, None, ],
                            [None, None, ],
                            [None, None, ],
                            [None, None, ],
                            [{'rowspan': 1}, {'rowspan': 1}]
                        ])

    #
    #  HEATMAP
    #

    nb_cells = adata.shape[0]
    pslice = 5000 / nb_cells if nb_cells > 5000 else 0.99

    data = adata[
        np.random.choice([True, False], adata.shape[0], p=[pslice, 1 - pslice])
    ]
    # on trie les cellules par clusters pour une heatmap plus claire
    clusters = data.uns[rank_test]['params']['groupby']
    label = [f"{cl} ({round(k * (1 / pslice))})" for k, cl in
             enumerate(pd.Series.sort_values(data.obs[clusters]).values)]
    cells = pd.Series.sort_values(data.obs[clusters]).index
    sort_data = data[cells]

    genes_label = []
    genes = []
    genes_id = []
    i = 0
    for clust in sort_data.uns[rank_test]['names'].dtype.names:
        for gene in sort_data.uns[rank_test]['names'][clust][:nb_genes]:
            if gene not in genes:
                genes_label.append(gene)
                genes.append(gene)
                genes_id.append(i)
                i += 1
            else:
                ind = genes.index(gene)
                genes_id.append(genes_id[ind])
                while gene in genes_label:
                    gene += ' '
                genes_label.append(gene)

    df = pd.DataFrame([], index=sort_data.obs_names, columns=genes_label)
    array = sort_data[:, genes].X.toarray().transpose()
    for k in range(len(genes_label)):
        df[genes_label[k]] = array[genes_id[k]]

    heatmap = go.Heatmap(
        z=df.to_numpy(),
        x=df.columns,
        y=label,
        showlegend=False,
        type='heatmap',
        colorscale='Viridis')

    #
    #    CREATE LEFT COLOR LABEL BAR
    #

    clusters_col = adata.obs[clusters]
    nbcl = len(adata.obs[clusters].cat.categories)
    len_cl = []
    for cl in clusters_col.cat.categories:
        len_cl.append((clusters_col == cl).sum())

    x = [0, 1]
    y = [0]
    for size in len_cl:
        y.append(y[-1] + size)

    color = go.Heatmap(
        x=x,
        y=-np.sort(-np.array(y)),
        z=[[n] for n in range(len(clusters_col.cat.categories) - 1, -1, -1)],
        text=[[cl_name] for cl_name in list(clusters_col.cat.categories)[::-1]],
        texttemplate="%{text}",
        showscale=False,
        # showticklabels=False,
        colorscale=[[i / 23, px.colors.qualitative.Light24[i]] for i in range(24)],
    )

    #
    #    CREATE BOTTOM LABEL COLOR BAR
    #

    Z = []
    for i in range(nbcl):
        Z += [i] * nb_genes

    Text = []
    for i in range(nbcl):
        tmp = [clusters_col.cat.categories[i] if j == nb_genes // 2 else '' for j in range(nb_genes)]

        Text += tmp

    cl_heatmap = go.Heatmap(
        x=df.columns,
        y=['clusters'],
        z=[Z],
        text=[Text],
        texttemplate="%{text}",
        showscale=False,
        # showticklabels=False,
        colorscale=[[i / 23, px.colors.qualitative.Light24[i]] for i in range(24)]
    )

    #
    #    ADD TRACES
    #

    fig.add_trace(color, row=1, col=1)
    fig.add_trace(heatmap, row=1, col=2)
    fig.add_trace(cl_heatmap, row=10, col=2)
    fig.update_yaxes(title='y', visible=False, showticklabels=False)
    fig.update_xaxes(title='x', visible=False, showticklabels=False, row=1)
    fig.update_xaxes(title='x', visible=False, showticklabels=False, row=1, col=1)
    fig.update_xaxes(tickangle=0, row=10, col=10)

    return fig


def low_heatmap(data, rank_test, nb_genes):

    # in order to be more efficient, we keep only 5000 cells max
    # they are choosen randomly so the results is representative
    nb_cells = data.shape[0]
    pslice = 5000/nb_cells if nb_cells > 5000 else 0.99

    sort_data = data[
        np.random.choice([True, False], data.shape[0], p=[pslice, 1-pslice])
    ]

    # the expression of top gene of each marker is gather in a DataFrame
    # 1 gene can be in top of multiples genes but Dataframe have unique column names
    # so we need to do some trick adding space after gene name
    # we also need to keep the old name of the gene to get his expression
    genes_label = []
    genes = []
    genes_id = []
    i = 0
    for clust in sort_data.uns[rank_test]['names'].dtype.names:
        for gene in sort_data.uns[rank_test]['names'][clust][:nb_genes]:
            if gene not in genes:
                genes_label.append(gene)
                genes.append(gene)
                genes_id.append(i)
                i += 1
            else:
                ind = genes.index(gene)
                genes_id.append(genes_id[ind])
                while gene in genes:
                    gene += ' '
                genes_label.append(gene)

    df = pd.DataFrame([], index=sort_data.obs_names, columns=genes_label)
    array = sort_data[:, genes].X.toarray().transpose()
    for k in range(len(genes_label)):
        df[genes_label[k]] = array[genes_id[k]]

    return px.imshow(df, aspect="auto", labels=dict(y='Clusters'))


def parse_content(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        df = pd.DataFrame()
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')),
                sep=",|;|\t",
                header=0,
                engine='python',
            )
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), header=0, sheet_name=0)

        genes = list(df[df.columns[0]]) if not df.empty else []

    except Exception as e:
        print(e)
        genes = []

    return genes


def hash_password(pwd):
    """Get hash from clear password.

    Gimov don't store clear password but their hashes. There are severals algorithms to caclulate hashes so Gimov \
    provide a function to ensure consistency with the password check inside the interface.

    :param str pwd: password to hash. Integers or floats have to be format to string before hash.
    :return: (str) - password's hash
    """
    if isinstance(pwd, str):
        return hb.sha224(pwd.encode('utf-8')).hexdigest()
    elif isinstance(pwd, int):
        raise ValueError("Password can't be an integer, it's must be a string")
    else:
        raise ValueError("Password must be a string")


tools = Tools()
