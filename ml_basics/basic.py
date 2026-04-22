import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('StudentPerformanceFactors.csv')
df = pd.DataFrame(data)

plt.figure(figsize=(15, 8))

#histogram
plt.subplot(2, 3, 1)
plt.hist(df['Hours_Studied'], bins=20, edgecolor='black')
plt.title('Hours Studied')

#boxplot plot 
plt.subplot(2, 3, 2)
plt.boxplot(df['Exam_Score'])
plt.title('Exam Score Distribution')

#scatter plot
plt.subplot(2, 3, 3)
plt.scatter(df['Hours_Studied'], df['Exam_Score'])
plt.title('Hours vs Score')

#bar plot
plt.subplot(2, 3, 4)
plt.bar(df['Attendance'], df['Exam_Score'])
plt.xlabel("Attendance Rate")
plt.ylabel("Exam Score")
plt.title("Attendance Rate vs Exam Score")  

#line plot
plt.subplot(2, 3, 5)
df_sorted = df.sort_values('Hours_Studied')
plt.plot(df_sorted['Hours_Studied'], df_sorted['Exam_Score'], marker='o')
plt.xlabel("Hours Studied")
plt.ylabel("Exam Score")
plt.title("Hours Studied vs Exam Score")

#pie chart
plt.subplot(2, 3, 6)
plt.pie(df['Extracurricular_Activities'].value_counts(), labels=df['Extracurricular_Activities'].unique(), autopct='%1.1f%%')
plt.title("Extracurricular Activities Distribution")

plt.tight_layout()
plt.show()

plt.figure(figsize=(16, 8))

plt.subplot(2,3,1)
sns.histplot(df['Exam_Score'], bins=20, kde=True)
plt.title('Exam Score Distribution')

plt.subplot(2,3,2)
sns.scatterplot(x='Hours_Studied', y='Exam_Score', data=df)
plt.title('Hours Studied vs Exam Score')
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')

plt.subplot(2,3,3)
sns.regplot(x = 'Hours_Studied', y = 'Exam_Score',data=df)
plt.title('Regression: Hours Studied vs Exam Score')
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')

plt.subplot(2,3,4)
sns.boxplot(x='Gender', y='Exam_Score', data=df)
plt.title('Exam Score by Gender')
plt.xlabel('Gender')
plt.ylabel('Exam Score')    

plt.subplot(2,3,5)
sns.countplot(x='Extracurricular_Activities', data=df)
plt.title('Extracurricular Activities Count')
plt.xlabel('Extracurricular Activities')
plt.ylabel('Count') 

plt.subplot(2,3,6)
sns.barplot(x='Physical_Activity', y='Exam_Score', data=df)
plt.title('Average Exam Score by Physical Activity Level')
plt.xlabel('Physical Activity Level')
plt.ylabel('Average Exam Score')

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title('Correlation Heatmap')
plt.show()



#numpy array operations
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b) 
print(a * b,end='\n\n')  

#element-wise operations
a = np.array([1, 2, 3])
print(a + 10,end='\n\n')   

#boolean indexing
a = np.array([10, 20, 30])
print(a > 15)      
print(a[a > 15],end='\n\n')  

#matrix multiplication
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
print(A @ B,end='\n\n')  

#statistical functions
a = np.array([1, 2, 3, 4])
print(np.sum(a))   
print(np.mean(a)) 