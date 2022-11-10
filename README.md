# GUIMOV

Graphical Uuser Interface for Multi-Omics Visualisation

---

GUIMOV is an open-source Interface for multi-omics visualization providing the commonly used graphics and tools in single
cell RNAseq analyses in an easily installed package. Based on Anndata format, it was made to explore scRNAseq, spatially
resolved single cell and ATAC seq data, and also to refine analyses thanks to useful tools such as change cell
clustering, calculate a score from pathways and compute differentially expressed genes. The use of the Plotly library
allow interactive cells or groups selections, high resolution images and a free exploration of all metadata. GUIMOV is a
web application with secure access to datasets and simple deployment in environment. Distribution of a docker image
ensure no dependencies and portability.  Otherwise, it is available as a python package

Check the Documentation to know how install and use GUIMOV.

## Contents
___

GUIMOV’s interface are structured in tabs, each one dedicated to a part of the analysis, and provide several tools and
graphs with parameters to explore the datasets. The pbmc3k datasets is the datasets used in the Scanpy’s tutorial, we 
will be used to explore the interface.

GUIMOV includes theses graphs :
+ **Overview**: access a dataset a password is required: in order to download and explore pbmc3k enter the password ‘demo’.
This first tabs give some useful information about the datasets
+ **QCs**: second tabs provide stacked barplot and violin plots to explore the metadata of the datasets.
+ **Embeddings**: An embedding is set of coordinates calculated for each cell. Generally, from reduction dimension as 
PCA, embeddings could also be UMAP and Spatial . This tab allows to explore the first axes of PCA and project some
metadata like clusters of genes expression. Moreover, GUIMOV provides a tool to select one or two groups and look for
differential expression using a ranking test.
+ **Distributions**: Distribution tab uses an alluvial plot to compare two categorical metadata
+ **Expressions Expression**: Genes differential expression is computed thanks a ranking test with Scanpy. A table and 
an heatmap are available to explore the differentially expressed genes
+ **Clusterings**: Clustering cells is one of the most complicated tasks of the analysis, as it requires to fit several 
information like the cell type, conditions, samples and more to choose the final resolution
+ **Pathways**: A pathway is defined here as a set of genes that must be explored together. We usually want to know if 
they are differentially expressed between groups of cells in the dataset

##Methods
___
	
### Package
GUIMOV is built on Dash, a Python package. Written on top of the JavaScript libraries Plotly.js and React.js, Dash
creates a customizable application rendered in the web browser. The python code is automatically converted into HTML and
JavaScript. The web page is host by a server ran with an open-source micro framework for web development in Python, 
Flask. In this way the front-end can be set by a CSS file and separated from the back-end developed in Python. 
Dash also provides a set of tools made for interactive visualization compatible with the large data of single cell. Dash
is inherently cross-platform and mobile ready, perfect to deploy in a whole organization. The GUIMOV tools are 
implemented using Scanpy. As Dash and Scanpy are both written in Python, Scanpy’s functions can easily fit with 
the architecture of Dash.

### Inputs data:
Data is stored in the Anndata format, a standard format for single cell data in Python, understood by both Scanpy and 
Dash tools. The data is not modified by the interface, all functions applied to datasets are temporary and their result 
are erased when the user disconnects. In addition, with its interface, GUIMOV also allow users to convert other 
well-known format as Seurat into Anndata, with extension ‘.h5ad’ thanks a built-in converter usable in command line or 
importing GUIMOV in Python.

### Sessions management
Using Dash, asynchronous functions are used to ensure portability and optimize the use of devices. GUIMOV can track 
session from the interface and unload memory if possible. In fact, most of the computing resources are used for the 
creation of graphics from large datasets. This part is handled by the local device. A parameter allows users to reduce 
the numbers of cells to display in graphs to facilitate the use of light devices. The remote device handles the tools 
calculations and the RAM usage to load datasets. In order to save performance, a dataset is only load once. When 2 
sessions want to use the same dataset, they share it and so no more RAM is used. Moreover, as soon as a user close 
the browser (in fact the window or tab of GUIMOV) the memory is freed. Datasets are also unloaded when the interface is 
not used for 45min, to prevent ghost sessions.
