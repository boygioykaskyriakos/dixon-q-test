from static_files.standard_variable_names import LOWER_RANGE_NUMBER, HIGHER_RANGE_NUMBER, UPPER_NUMERATOR, \
    LOWER_NUMERATOR, LOWER_DENOMINATOR, UPPER_DENOMINATOR, EXCEPTION


"""
all formulas of different population of subsets 
"""

r0 = {
    HIGHER_RANGE_NUMBER: 2,
    EXCEPTION: "Change length of numbers"
}

r10 = {
    LOWER_RANGE_NUMBER: 3,
    HIGHER_RANGE_NUMBER: 7,

    # x_n - x_n-1
    UPPER_NUMERATOR: lambda x: float(x[-1] - x[-2]),
    # x_n - x_1
    UPPER_DENOMINATOR: lambda x: float(x[-1] - x[0]),

    # x_2 - x_1
    LOWER_NUMERATOR: lambda x: float(x[1] - x[0]),
    # x_n - x_1
    LOWER_DENOMINATOR: lambda x: float(x[-1] - x[0])
}

r11 = {
    LOWER_RANGE_NUMBER: 8,
    HIGHER_RANGE_NUMBER: 10,

    # x_n - x_n-1
    UPPER_NUMERATOR: lambda x: float(x[-1] - x[-2]),
    # x_n -x_2
    UPPER_DENOMINATOR: lambda x: float(x[-1] - x[1]),

    # x_2 - x_1
    LOWER_NUMERATOR: lambda x: float(x[1] - x[0]),
    # x_n-1 - x_1
    LOWER_DENOMINATOR: lambda x: float(x[-2] - x[0])
}

r21 = {
    LOWER_RANGE_NUMBER: 11,
    HIGHER_RANGE_NUMBER: 13,

    # x_n - x_n-2
    UPPER_NUMERATOR: lambda x: float(x[-1] - x[-3]),
    # x_n -x_2
    UPPER_DENOMINATOR: lambda x: float(x[-1] - x[1]),

    # x_3 - x_1
    LOWER_NUMERATOR: lambda x: float(x[2] - x[0]),
    # x_n-1 - x_1
    LOWER_DENOMINATOR: lambda x: float(x[-2] - x[0])
}

r22 = {
    LOWER_RANGE_NUMBER: 14,

    # x_n - x_n-2
    UPPER_NUMERATOR: lambda x: float(x[-1] - x[-3]),
    # x_n -x_3
    UPPER_DENOMINATOR: lambda x: float(x[-1] - x[2]),

    # x_3 - x_1
    LOWER_NUMERATOR: lambda x: float(x[2] - x[0]),
    # x_n-2 - x_1
    LOWER_DENOMINATOR: lambda x: float(x[-3] - x[0])
}


def generic_formula_dixon_q_test(r, subset):
    upper_numerator = r[UPPER_NUMERATOR](subset)
    upper_denominator = r[UPPER_DENOMINATOR](subset)
    lower_numerator = r[LOWER_NUMERATOR](subset)
    lower_denominator = r[LOWER_DENOMINATOR](subset)

    return upper_numerator, upper_denominator, lower_numerator, lower_denominator

