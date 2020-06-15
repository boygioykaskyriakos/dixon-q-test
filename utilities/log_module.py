import logging
import os

from utilities.read_ini_file import ReadIniFile
from static_files.standard_variable_names import GLOBALS, OUTPUT_PATH, LOG_FILE_NAME


class Logger:
    read_ini_file_obj = ReadIniFile()
    file_folder_path = read_ini_file_obj.get_str(GLOBALS, OUTPUT_PATH)

    if not os.path.exists(file_folder_path):
        os.makedirs(file_folder_path)

    filename_output = "\\".join([file_folder_path, LOG_FILE_NAME + ".log"])

    # set up logging to file
    logging.basicConfig(
        filename=filename_output,
        filemode="w",
        level=logging.INFO,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - \n %(message)s',
        datefmt='%H:%M:%S'
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-8s %(asctime)s \n %(message)s ')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)

    @classmethod
    def set_formatter(cls, formatter):
        cls.console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(cls.console)
        cls.logger = logging.getLogger(__name__)

    @classmethod
    def check_for_new_line(cls, content):
        if "\n" not in content:
            formatter = logging.Formatter('%(levelname)-8s %(asctime)s  %(message)s ')
        else:
            formatter = logging.Formatter('%(levelname)-8s %(asctime)s \n %(message)s ')

        cls.set_formatter(formatter)

    @classmethod
    def info(cls, content):
        cls.check_for_new_line(content)
        cls.logger.info(content)

