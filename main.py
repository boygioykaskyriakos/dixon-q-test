from static_files.dixon_q_test_confidence_data import STATIC_Q95, STATIC_Q90, STATIC_Q99
from utilities.read_csv_to_pd_dataframe import ReadCSVToDataFrame
from static_files.standard_variable_names import NODE, DATA_TYPE
from dixon_q_test.dixon_q_test_class import FindOutlierDixon

if __name__ == "__main__":
    df_data = ReadCSVToDataFrame(field_name="DATA_SET_INFO", file_path="full_file_path", delimiter="delimiter").run()
    df_data_grouped = df_data.groupby([NODE, DATA_TYPE])

    find_outliers_dixon = FindOutlierDixon(grouped_data=df_data_grouped)

    # results for q90
    find_outliers_dixon.run(STATIC_Q90)

    # results for q95
    find_outliers_dixon.run(STATIC_Q95)

    # results for q99
    find_outliers_dixon.run(STATIC_Q99)
