import os


class Settings:
    """
    Settings provides properties to set the paths of datasets and logs files.
    """
    def __init__(self):
        self._datasets_path = os.getcwd()+'/datasets/datasets.txt'
        self._logs_path = os.getcwd()+'/logs/log'

    @property
    def datasets_path(self):
        """
        Path of file containing the list of datasets with their hashed password.
        """
        return self._datasets_path

    @datasets_path.setter
    def datasets_path(self, path):
        if os.path.exists(path):
            self._datasets_path = path
        else:
            raise ValueError(f'`{path}` does not exist')

    @property
    def logs_path(self):
        """
        Path of the file where all logs will be saved. The new logs will be added, and does not remove
        the data of the file.
        """
        return self._logs_path

    @logs_path.setter
    def logs_path(self, path):
        if os.path.exists(path):
            self._logs_path = path
        else:
            raise ValueError(f'`{path}` does not exist')


settings = Settings()
