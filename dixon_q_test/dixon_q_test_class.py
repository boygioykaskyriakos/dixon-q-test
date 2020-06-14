import pandas as pd

from copy import copy

from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import DATA_TYPE, NODE, VALUES, VALUE, KEY, \
    OUTLIER_NO, SUBSET, SUBSET_SIZE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, CONFIDENCE_LVL


class FindOutlierDixon(BaseClassAnalytic):
    OUTPUT_COLUMNS = [OUTLIER_NO, SUBSET_SIZE, SUBSET, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]

    def __init__(self, grouped_data: pd.DataFrame):
        BaseClassAnalytic.__init__(self)

        self.grouped_data = grouped_data
        self.static_n = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "static_n")
        self.static_n_maximum = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "static_n_maximum")

    @staticmethod
    def get_result(numbers: pd.Series, comparator: float) -> bool:
        numbers = copy(numbers).sort_values().to_list()

        q_lower = 0
        q_upper = 0
        denominator = float(numbers[-1]-numbers[0])

        if denominator > 0:
            q_lower = float(numbers[1] - numbers[0]) / denominator
            q_upper = float(numbers[-1] - numbers[-2]) / denominator

        if q_lower > comparator or q_upper > comparator:
            return True
        else:
            return False

    @staticmethod
    def find_comparator(numbers: list, confidence: tuple) -> float:
        get_number = len(numbers) - 3

        return confidence[get_number]

    @staticmethod
    def print_to_console(row: dict, confidence_lvl: dict) -> None:
        msg = "********** OUTLIER No " + str(self.counter) +" *******************" + "\n"
        msg += "NODE: " + str(whole_set[NODE].values[0]).replace("\t", "") + \
               ", DATA TYPE [" + whole_set[DATA_TYPE].values[0] + "]\n"
        msg += "INDEX[" + str(i) + ", " + str(static_n + i-1) + "] = "
        msg += str(temp_data.tolist()) + " " + "\n"
        msg += str(confidence_lvl).upper() + ", SUBSET SIZE: " + str(static_n) + "\n"

        print(msg)

    @staticmethod
    def results_to_dict(
            static_n: int, whole_set: pd.DataFrame, temp_data: pd.Series, i: int) -> dict:

        temp_dic_res = {
            SUBSET_SIZE: str(static_n),
            SUBSET: str(temp_data.tolist()),
            NODE: str(whole_set[NODE].values[0]).replace("\t", ""),
            DATA_TYPE: whole_set[DATA_TYPE].values[0],
            INDEX_FIRST_ELEMENT: str(i),
            INDEX_LAST_ELEMENT: str(static_n + i - 1),

        }

        return temp_dic_res

    def get_appropriate_subset(
            self, static_n: int, whole_set: pd.DataFrame, confidence: dict, result: list) -> list:

        test_set = whole_set[VALUES]

        # list comprehension with UDF optimized on pd.DataFrame
        # read it like: for i in range if condition is true then print
        result += [
            self.results_to_dict(static_n, whole_set, test_set[i:i + static_n].sort_values(), i)
            for i in range(len(test_set)-static_n)
            if self.get_result(test_set[i:i+static_n],
                               self.find_comparator(test_set[i:i+static_n], confidence[VALUE])) is True
        ]

        return result

    def run(self, confidence_level: dict) -> None:
        static_n = copy(self.static_n)
        final_result = []
        df = pd.DataFrame(columns=self.OUTPUT_COLUMNS)

        while static_n <= self.static_n_maximum:
            self.grouped_data.apply(
                lambda grp: self.get_appropriate_subset(static_n, grp, confidence_level, final_result)
            )

            # increment size
            static_n += 1

        if len(final_result) > 0:
            for idx, row in enumerate(final_result):
                row[OUTLIER_NO] = idx+1

            if self.print_debug:
                for row in final_result:
                    self.print_to_console(row, confidence_level)

            df = pd.DataFrame(final_result)

        self.save_file.run(df[self.OUTPUT_COLUMNS], confidence_level[KEY])
