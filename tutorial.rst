Tutorial
========

GUIMOV provide severals functions divide in tabs. Each tabs focus on a main purpose and offer some tools
or graphs to explore it.


Overview
-----------

Each dataset has a unique code, which is given by the bioinformatic team.
For more safety the server only store the code's hash.

.. image:: img/overview.png

|
|

QCs
------------

.. image:: img/qcs.png

1. Select the feature type you want to explore, it may have multiple features in multi omics datasets, or when several datasets are gather.
2. Show groups, stacked (like the screen) or one behind the other.
3. When a gene is selected (5 and 6 are optional) you can display his expressionon Y axis (1 screen) or on X axis of first plot and Y axis of second plot (2 screen).
4. Select a numerical metadata (real values) to display on graphs (display on second graph if any gene are selected or if gene expression is display on Y axis).
5. Select a gene to explore his expression (write the first letter to show all options of the dropdown).
6. Select a numerical metadata to display when gene expression is display on X axis.
7. When groups are display one behind the other, it can be useful to change the opactiy of all groups.
8. Select a categorical metadata (clusters, sample, etc) to display on both graphs.

|
|

Embedding
------------

.. image:: img/embeddings.png

1. Features type
2. Select which embeddind to use (coordinates of cells). Select ‘spatial ’ with a spatial dataset to display the image of sample behind points.
3. Seletec metadata to explore (change the color of graph)
4. Seletec one or more gene (sum expression)(priority against metadata)
5. When embedding allow it permit to display a 3d graph (which can be move in all directions)
6. Percentage of cells to display (randomly choose). Use it for large datasets (>10’000 cells) or with a small computer.
7. Size of points on the graph
8. Range of color to use when display a numerical metadata
9. Percentage of points opacity, usable only with spatial datasets.
10. Save graph in svg format
11. In order to compute Differential Expression on choosen cells, use the ‘lasso’ tool of plotly to select cells. Then press ‘cells selection 1’, repeat for the second selection. Chose the name of the DE and compute with ‘compute DE’. The resuls can be seen in the Differential Expression tab.

|
|

Distribution
------------

.. image:: img/distribution.png

1. Features type
2. First categorical metadata
3. Second categorical metadata

|
|

Differentially express genes
----------------------------

.. image:: img/ranktest.png

1. Features type
2. Differential Expression already calculated
3. Clusters to explore in table (default all clusters included)
4. Numbers of Genes per clusters in the heatmap
5. Export all genes in csv. (very large file, nbGenes * nbClusters rows)
6. Export the table in csv.

|
|

Clustering
------------

.. image:: img/clusters.png

1. Features type
2. Embedding use for the first graph
3. Clustering use for the first graph and at the top of the second one
4. Clustering use at the bottom of the second graph
5. Percentage of cells to display
6. Size of points in first graph
7. Select the resolution of clustering
8. Calculate clustering with selected resolution to use in 3. and 4.
9. Load 3. clustering in dataset as categorical metada

|
|

Pathways
------------

.. image:: img/pathways.png

1. Features type
2. Select Genes to add in pathways, write first letter to see suggestion
3. Write or copy / paste genes, split with comma without spaces.
4. Enter name of pathways
5. Get genes from first columns of csv or excel files.
6. Run the pathways, the results is store as numerical metadata in dataset.

|
|

Options
------------

Loading ...