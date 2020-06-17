import pandas as pd
import inspect

from utilities.log_module import Logger


class SavePdToFile:
    def __init__(self, output_path):
        self.output_path = output_path
        self.logger = Logger()

    def run(self, df: pd.DataFrame, title=""):
        class_function_name = []
        stack = inspect.stack()

        for row in stack:
            if "self" in row[0].f_locals.keys():
                if row[0].f_locals["self"].__class__.__name__ == self.__class__.__name__:
                    pass
                else:
                    class_function_name = row[0].f_locals["self"].__class__.__name__ + "_"
                    break

        if title != "":
            title = "_".join([title])

        full_output_path = "\\".join([self.output_path, class_function_name + title + ".csv"])
        # lower columns
        df.columns = df.columns.str.lower()
        df.to_csv(full_output_path, index=False)

        self.logger.info(full_output_path + " file saved successfully")

        return None
