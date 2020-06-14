import pandas as pd

from base_class.base_class_analytic import BaseClassAnalytic


class ReadCSVToDataFrame(BaseClassAnalytic):
    def __init__(self, field_name: str, file_path: str, delimiter=""):
        BaseClassAnalytic.__init__(self)

        self.file_path = self.read_ini_file_obj.get_str(field_name, file_path)
        try:
            self.delimiter = self.read_ini_file_obj.get_str(field_name, delimiter)
        except Exception as e:
            print(e)
            self.delimiter = ""

    def run(self) -> pd.DataFrame:
        if len(self.delimiter) > 0:
            df = pd.read_csv(self.file_path, delimiter=self.delimiter)
        else:
            df = pd.read_csv(self.file_path)

        return df
