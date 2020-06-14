import abc

from utilities.read_ini_file import ReadIniFile
from utilities.save_to_file import SavePdToFile

from static_files.standard_variable_names import GLOBALS, OUTPUT_PATH


class BaseClassAnalytic(object):
    def __init__(self):
        self.read_ini_file_obj = ReadIniFile()
        self.save_file = SavePdToFile(self.read_ini_file_obj.get_str(GLOBALS, OUTPUT_PATH))

    @abc.abstractmethod
    def run(self, *args):
        raise NotImplementedError("method not implemented")
