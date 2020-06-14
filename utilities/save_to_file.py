import pandas as pd


class SavePdToFile:
    def __init__(self, output_path):
        self.output_path = output_path

    def run(self, df: pd.DataFrame, title=""):
        if title != "":
            title = "_".join([title])

        full_output_path = "\\".join([self.output_path, self.__class__.__name__ + title + ".csv"])
        df.to_csv(full_output_path, index=False)
        print(full_output_path + " file saved successfully")

        return None
