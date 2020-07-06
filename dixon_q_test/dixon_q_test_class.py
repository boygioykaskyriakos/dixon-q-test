import pandas as pd

from copy import copy

from base_class.base_class_analytic import BaseClassAnalytic
from static_files.standard_variable_names import DATA_TYPE, NODE, VALUES, VALUE, KEY, \
    OUTLIER_NO, SUBSET, SUBSET_SIZE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT, TOTAL_PANICS, \
    HIGHER_RANGE_NUMBER, LOWER_RANGE_NUMBER, EXCEPTION
from static_files.dixon_formulas import r0, r10, r11, r21, r22, generic_formula_dixon_q_test


class FindOutlierDixon(BaseClassAnalytic):
    OUTPUT_COLUMNS = [OUTLIER_NO, SUBSET_SIZE, SUBSET, NODE, DATA_TYPE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]
    OUTPUT_COLUMNS_METRICS = [SUBSET_SIZE, OUTLIER_NO]
    OUTPUT_COLUMNS_METRICS_CRITICAL = [SUBSET_SIZE, TOTAL_PANICS]

    def __init__(self, grouped_data: pd.DataFrame):
        BaseClassAnalytic.__init__(self)

        self.grouped_data = grouped_data
        self.static_n = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "static_n")
        self.static_n_maximum = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "static_n_maximum")
        self.critical_value = self.read_ini_file_obj.get_int("DIXON_Q_TEST_SUBSET_VARIABLES", "critical_value")

    @staticmethod
    def dixon_q_test_algo(numbers: pd.Series, comparator: float) -> bool:
        """
        Dixon q test method reflects the exact dixon q test algorithm

        :param numbers: list : the subset to examine if it contains outliers
        :param comparator: float: the value to compare for outliers according the dixon-q-test algorithm
        :return: bool: True or False
        """

        # initialize local variables
        numbers = copy(numbers).sort_values().to_list()
        len_numbers = len(numbers)

        q_lower = 0
        q_upper = 0

        if len_numbers < r0[HIGHER_RANGE_NUMBER]:
            raise ValueError(r0[EXCEPTION])
        # r10
        elif r10[LOWER_RANGE_NUMBER] <= len_numbers <= r10[HIGHER_RANGE_NUMBER]:
            r = r10
        # r11
        elif r11[LOWER_RANGE_NUMBER] <= len_numbers <= r11[HIGHER_RANGE_NUMBER]:
            r = r11
        # r21
        elif r21[LOWER_RANGE_NUMBER] <= len_numbers <= r21[HIGHER_RANGE_NUMBER]:
            r = r21
        else:   # r22[LOWER_RANGE_NUMBER] <= len_numbers
            r = r22

        upper_numerator, upper_denominator, lower_numerator, lower_denominator = \
            generic_formula_dixon_q_test(r, numbers)

        # apply dixon q test algorithm logic
        if lower_denominator > 0:
            q_lower = lower_numerator / lower_denominator

        if upper_denominator > 0:
            q_upper = upper_numerator / upper_denominator

        if q_lower > comparator or q_upper > comparator:
            return True
        else:
            return False

    @staticmethod
    def find_comparator(numbers: list, confidence: tuple) -> float:
        get_number = len(numbers) - 3

        return confidence[get_number]

    def print_to_console(self, row: dict, confidence_lvl: dict) -> None:
        msg = "********** OUTLIER No " + str(row[OUTLIER_NO]) + " *******************" + "\n"
        msg += "NODE: " + row[NODE] + ", DATA TYPE [" + row[DATA_TYPE] + "]\n"
        msg += "INDEX[" + row[INDEX_FIRST_ELEMENT] + ", " + row[INDEX_LAST_ELEMENT] + "] = "
        msg += row[SUBSET] + " " + "\n"
        msg += confidence_lvl[KEY].upper() + ", SUBSET SIZE: " + row[SUBSET_SIZE] + "\n"

        self.logger.info(msg)

    @staticmethod
    def results_to_dict(
            static_n: int, whole_set: pd.DataFrame, temp_data: pd.Series, i: int) -> dict:

        temp_dic_res = {
            SUBSET_SIZE: str(static_n),
            SUBSET: str(temp_data.tolist()),
            NODE: str(whole_set[NODE].values[0]).replace("\t", ""),
            DATA_TYPE: whole_set[DATA_TYPE].values[0],
            INDEX_FIRST_ELEMENT: str(i+static_n),
            INDEX_LAST_ELEMENT: str(i + 2*static_n - 1),

        }

        return temp_dic_res

    def get_appropriate_subset(
            self, static_n: int, grp: pd.DataFrame, confidence: dict, result: list) -> list:

        test_set = grp[VALUES]

        # list comprehension with UDF optimized on pd.DataFrame
        # read it like: for i in range if condition is true then print
        result += [
            self.results_to_dict(static_n, grp, test_set[i+static_n:i + 2*static_n].sort_values(), i)
            for i in range(len(test_set)-2*static_n + 1)
            if self.dixon_q_test_algo(
                test_set[i+static_n:i + 2*static_n],
                self.find_comparator(test_set[i+static_n:i+2*static_n], confidence[VALUE])
            ) is True
        ]

        return result

    def format_metrics_critical(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.groupby(
            [SUBSET_SIZE, NODE, INDEX_FIRST_ELEMENT, INDEX_LAST_ELEMENT]
        ).count().reset_index()

        df = df[df[OUTLIER_NO] > self.critical_value]
        df = df.groupby(SUBSET_SIZE)[OUTLIER_NO].sum().reset_index()
        df[OUTLIER_NO] = df[OUTLIER_NO] / 2
        df[OUTLIER_NO] = df[OUTLIER_NO].astype(int)
        df = df.rename(columns={OUTLIER_NO: TOTAL_PANICS})

        return df

    def run(self, confidence_level: dict) -> None:
        """
        The main method of the class that saves to file the outliers according the dixon-q-test algorithm

        :param confidence_level: dict: as key contains the title of the confidence
        and as values contains the dixon-q-test comparator values
        :return: None
        """

        # initialize local variables
        static_n = copy(self.static_n)
        final_result = []
        df = pd.DataFrame(columns=self.OUTPUT_COLUMNS)
        df_metrics = pd.DataFrame(columns=self.OUTPUT_COLUMNS_METRICS)
        df_metrics_critical = pd.DataFrame(columns=self.OUTPUT_COLUMNS_METRICS_CRITICAL)

        # apply logic main loop
        while static_n <= self.static_n_maximum:
            self.grouped_data.apply(
                lambda grp: self.get_appropriate_subset(static_n, grp, confidence_level, final_result)
            )
            static_n += 1

        # create results
        if len(final_result) > 0:
            for idx, row in enumerate(final_result):
                row[OUTLIER_NO] = idx+1

            if self.print_debug:
                for row in final_result:
                    self.print_to_console(row, confidence_level)

            df = pd.DataFrame(final_result)
            df_metrics = df.groupby([SUBSET_SIZE]).count().reset_index()
            df_metrics_critical = self.format_metrics_critical(df)

        # save results to files
        self.save_file.run(df[self.OUTPUT_COLUMNS], confidence_level[KEY] + "_metrics_details")
        self.save_file.run(df_metrics[self.OUTPUT_COLUMNS_METRICS], confidence_level[KEY] + "_metrics_summary")
        self.save_file.run(
            df_metrics_critical[self.OUTPUT_COLUMNS_METRICS_CRITICAL], confidence_level[KEY] + "_metrics_critical"
        )

