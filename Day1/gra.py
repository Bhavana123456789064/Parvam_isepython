import matplotlib.pyplot as plt

# Sample data
students = ['Asha', 'Ravi', 'Kiran', 'Neha', 'Rahul']
maths = [85, 78, 92, 70, 88]
science = [90, 82, 88, 75, 84]
english = [88, 80, 91, 72, 86]

# Create subplot (2 rows, 3 columns)
plt.figure(figsize=(12, 8))

# 1. Line Graph
plt.subplot(2, 3, 1)
plt.plot(students, maths, marker='o')
plt.title("Line Graph")

# 2. Bar Graph
plt.subplot(2, 3, 2)
plt.bar(students, science)
plt.title("Bar Graph")

# 3. Histogram
plt.subplot(2, 3, 3)
plt.hist(english, bins=5)
plt.title("Histogram")

# 4. Pie Chart
plt.subplot(2, 3, 4)
plt.pie(maths, labels=students, autopct='%1.1f%%')
plt.title("Pie Chart")

# 5. Scatter Plot
plt.subplot(2, 3, 5)
plt.scatter(maths, science)
plt.title("Scatter Plot")

# 6. Box Plot
plt.subplot(2, 3, 6)
plt.boxplot([maths, science, english],
            labels=['Maths', 'Science', 'English'])
plt.title("Box Plot")

plt.tight_layout()
plt.show()