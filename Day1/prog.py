import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# DATA
# -----------------------
data = {
    'Name': ['Asha', 'Ravi', 'Kiran', 'Neha', 'Rahul'],
    'Maths': [85, 78, 92, 70, 88],
    'Science': [90, 82, 88, 75, 84],
    'English': [88, 80, 91, 72, 86],
    'Social': [87, 75, 89, 74, 85],
    'Computer': [92, 85, 95, 78, 90]
}

df = pd.DataFrame(data)

# -----------------------
# CALCULATIONS
# -----------------------
marks = df.iloc[:, 1:].values
df['Total'] = np.sum(marks, axis=1)
df['Average'] = np.mean(marks, axis=1)

# Grade function
def grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 80:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 60:
        return 'C'
    else:
        return 'F'

df['Grade'] = df['Average'].apply(grade)

# Rank
df['Rank'] = df['Total'].rank(ascending=False).astype(int)

# -----------------------
# SELECT ONE STUDENT
# -----------------------
student = df.iloc[0]   # change index (0–4) for different student

subjects = ['Maths', 'Science', 'English', 'Social', 'Computer']

# -----------------------
# CREATE REPORT CARD UI
# -----------------------
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('off')

# Header
plt.text(0.5, 0.95, "ABC HIGH SCHOOL", ha='center',
         fontsize=16, fontweight='bold')
plt.text(0.5, 0.90, "ANNUAL REPORT CARD", ha='center',
         fontsize=12)

# Student Info
info = f"""
Name   : {student['Name']}
Class  : 10
Section: A
"""
plt.text(0.05, 0.75, info, fontsize=11)

# Table Data
table_data = [[sub, student[sub]] for sub in subjects]

table = plt.table(cellText=table_data,
                  colLabels=["Subject", "Marks"],
                  loc='center',
                  cellLoc='center')

table.scale(1, 1.5)

# Result Summary
result = f"""
Total   : {student['Total']}
Average : {student['Average']:.2f}
Grade   : {student['Grade']}
Rank    : {student['Rank']}
"""
plt.text(0.65, 0.30, result, fontsize=11)

# Footer
plt.text(0.1, 0.05, "Class Teacher Signature")
plt.text(0.6, 0.05, "Principal Signature")

plt.show()