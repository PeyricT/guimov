Installation
============

GUIMOV has differents way to be installed. According your utilisation you would use
pip, docker or from source for installed it. After the installation look at
`datasets requirements`_ to add your own datasets, then tutorials_ to learn how use GUIMOV.

pip
----------

GUIMOV is available as a package. It is not already on PyPI but you could install it
easily with this code.


>>> pip install git+https://gitlab.com/pfgt/sandbox/GUIMOVapp.git

Using Python
~~~~~~~~~~~~~
then you would be able to use GUIMOV as standar python package. In order to use your own
datasets you can use `guimov.settings`, the sttings must be set before launch the app,
therefore default settings will be used and paths must not be found.

>>> import guimov
>>> guimov.settings.datasets_path = 'Path/to/your/datasets/file'
>>> guimov.settings.logs_path = 'Path/to/your/logs/file'
>>> guimov.start()

If you want explore a single dataset, prefere using the following command

>>> guimov.start(dataset='Path/to/your/dataset')


using Bash
~~~~~~~~~~~

>>> guimov_launch --datasets=Path/to/your/datasets/file --logs=Path/to/your/logs/file

If you want explore a single dataset, prefere using the following command

>>> guimov_launch --singledataset=Path/to/your/dataset


Docker
-----------

Using Docker is the easyest way to install GUIMOV, you only have to download
the docker image_ and load it. With docker you can't move the path to access datasets.
However you can mount your directory inside the container.

>>> docker run -d -p 8050:8050 -v /Users/Username/your_datasets:/app/datasets -v /Users/Username/your_logs:/app/logs guimovapp

From source
-----------

GUIMOV provide an requirements.txt file, in order to quickly install all dependencies.

>>> git clone https://gitlab.com/pfgt/sandbox/GUIMOVapp.git
>>> cd GUIMOVapp
>>> pip install -r requirements.txt

Then you can start the interface with the following command :

>>> python guimov/__main__.py

Here the best way to add your directory is adding them in `datasets` directory.

Servers mode
------------

GUIMOV could be install on server same way as above.

.. _tutorials: ./tutorial.html
.. _`datasets requirements`: ./datasets.html
.. _image: https://www.docker.com/