import logging
import sys

from utilities.read_ini_file import ReadIniFile
from static_files.standard_variable_names import GLOBALS, OUTPUT_PATH, LOG_FILE_NAME


class Logger:
    read_ini_file_obj = ReadIniFile()
    filename_output = "\\".join([read_ini_file_obj.get_str(GLOBALS, OUTPUT_PATH), LOG_FILE_NAME + ".log"])

    # # setup logging to file
    # logging.basicConfig(
    #     filename=filename_output,
    #     filemode="a",
    #     format='%(asctime)s - %(message)s',
    #     level=logging.INFO,
    # )

    # set up logging to file
    logging.basicConfig(
        filename=filename_output,
        level=logging.INFO,
        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - \n %(message)s',
        datefmt='%H:%M:%S'
    )

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(asctime)s \n %(message)s ')
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)

    @classmethod
    def info(cls, content):
        cls.logger.info(content)
