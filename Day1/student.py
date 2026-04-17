#build a python-based student performance analysis system using pandas, numpy and matplotlib
import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
def analyze_student_performance(file_path):
    # Load data
    df = pd.read_csv(file_path)
    
    # Basic statistics
    print("Basic Statistics:")
    print(df.describe())
    
    # Average score per subject
    subjects = ['Maths', 'Science', 'English']
    avg_scores = df[subjects].mean()
    print("\nAverage Scores:")
    print(avg_scores)
    
    # Plotting average scores
    plt.bar(subjects, avg_scores, color=['blue', 'green', 'orange'])
    plt.title('Average Scores per Subject')
    plt.xlabel('Subjects')
    plt.ylabel('Average Score')
    plt.ylim(0, 100)
    plt.show()
# Example usage
analyze_student_performance('student.csv')
