# This file takes the data from the master csv file - "uvm_employee_salary_data_1994-2014.csv"
# And the data from the successfully data minded info in - "allData_complete.txt"
# in order to make a dataframe & csv file of the combined data - "combined_data_2014.csv"


import pprint
import numpy as np
import pandas as pd

allData = []

filename = "data/allData_complete.txt"
with open(filename, 'r') as f:
    for line in f:
        row = line.rstrip("\n").split("||")
#         row[0] = row_list[0].rstrip()
        allData.append(row)
        allData[-1][0] = allData[-1][0].rstrip()
f.close()
data = np.array(allData)
df_more_info = pd.DataFrame(data, columns=['original_name', 'netId', "proper_name", "department", "title", "primary_affiliation"])

# make df_allData_2014
df_salary = pd.read_csv(filepath_or_buffer="data/uvm_employee_salary_data_1994-2014.csv")
df_salary_2014 = pd.DataFrame(df_salary.loc[df_salary.Year == 2014])

# Make complete data for 2014
df_complete_2014 = pd.merge(df_more_info, df_salary_2014, left_on="original_name", right_on="Name", how="outer")

df_complete_2014.to_csv("data/combinedData_2014.csv")
# print ("hello")
# df_complete_2014.head()
