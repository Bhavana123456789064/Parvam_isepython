#pandas series a 1d array
import pandas as pd
#creating a pandas series
data = [10, 20, 30, 40, 50]
s = pd.Series(data)
print(s)

#dataframe a 2d array
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 40, 45],      
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']}
df=pd.DataFrame(data)
print(df)

#data from csv file
df_csv = pd.read_csv('student.csv')
print("\nData from CSV file:")
print(df_csv)

#display data from excel file
df_excel = pd.read_excel('data.xlsx')
print("\nData from Excel file:")
print(df_excel)
