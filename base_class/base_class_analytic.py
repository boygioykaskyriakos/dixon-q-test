import abc

from utilities.read_ini_file import ReadIniFile
from utilities.save_to_file import SavePdToFile
from utilities.log_module import Logger

from static_files.standard_variable_names import GLOBALS, OUTPUT_PATH, PRINT_DEBUG


class BaseClassAnalytic(object):
    def __init__(self):
        self.read_ini_file_obj = ReadIniFile()
        self.save_file = SavePdToFile(self.read_ini_file_obj.get_str(GLOBALS, OUTPUT_PATH))
        self.print_debug = self.read_ini_file_obj.get_int(GLOBALS, PRINT_DEBUG)
        self.logger = Logger()

    @abc.abstractmethod
    def run(self, *args):
        raise NotImplementedError("method not implemented")
