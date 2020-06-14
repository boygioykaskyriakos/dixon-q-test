# DixtonQ
A simple framework that applies the DixtonQ algorithm on integer datasets. 

The project contains an .ini file that needs to be configured. 

Input is a csv file, with four column:
NODE: string
TIME: integer
DATA TYPE: string
VALUES: integer

Output is a csv file, with x columns:
outlier_no: integer : number of outliers
subset_size: integer: the size of the list that contains the numbers that the outlier was found
subset: string: the list of numbers
NODE: reflects to input file
DATA TYPE: reflects to input file
index_first_element: integer: within the in memory grouped, subset's starting position
index_last_element: integer: within the in memory grouped, subset's finishing position



