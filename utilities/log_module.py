import logging
import os
import inspect

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
    file_handler = logging.FileHandler(filename_output, "w")
    file_handler.setLevel(logging.INFO)
    # # set up logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    # # set a format which is simpler for console use
    # formatter = logging.Formatter('%(levelname)-8s %(asctime)s \n %(message)s ')
    # file_handler.setFormatter(formatter)
    # stream_handler.setFormatter(formatter)
    # # add the handler to the root logger
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('').addHandler(stream_handler)
    logger = logging.getLogger("")

    @classmethod
    def get_class_function_name(cls):
        class_function_name = []
        stack = inspect.stack()

        for row in stack:
            if "self" in row[0].f_locals.keys():
                class_function_name.append(".".join([row[0].f_locals["self"].__class__.__name__, row.function]))

        return " in ".join(class_function_name)

    @classmethod
    def set_formatter(cls, content):
        class_function_name = cls.get_class_function_name()

        if "\n" not in content:
            formatter = logging.Formatter('%(levelname)-8s %(asctime)s  ' + class_function_name + '   %(message)s ')
        else:
            formatter = logging.Formatter('%(levelname)-8s %(asctime)s  ' + class_function_name + '   \n %(message)s ')

        cls.file_handler.setFormatter(formatter)
        cls.stream_handler.setFormatter(formatter)

    @classmethod
    def info(cls, content):
        cls.set_formatter(content)
        cls.logger.info(content)

