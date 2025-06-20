import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import re

plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

# Load and clean data
df = pd.read_csv(r'ExploratoryDataAnalysis\data\Software Engineer Salaries.csv')
df = df.drop(columns=["Job Title"], errors="ignore")

# --- Helper: extract average salary from string ---
def extract_salary_range(s):
    try:
        s = s.split('(')[0]  # Remove (Glassdoor est.) or any parentheses
        s = s.replace('$', '').replace('K', '')
        parts = s.split('-')
        if len(parts) == 2:
            return (int(parts[0]), int(parts[1]))
    except:
        return (np.nan, np.nan)
    return (np.nan, np.nan)

df[['Salary Min', 'Salary Max']] = df['Salary'].apply(lambda x: pd.Series(extract_salary_range(x)))
df['Salary Avg'] = df[['Salary Min', 'Salary Max']].mean(axis=1)

# --- Plot 1: Bar chart - Top 10 companies ---
df['Company'].value_counts().head(10).plot(kind='barh', figsize=(10, 6), color='skyblue')
plt.title("Top 10 Companies by Number of Job Listings")
plt.xlabel("Number of Listings")
plt.ylabel("Company")
plt.tight_layout()
plt.show()

# --- Plot 2: Histogram of average salary ---
# df['Salary Avg'].dropna().plot(kind='hist', bins=30, figsize=(10, 6), color='coral')
# plt.title("Distribution of Average Salaries")
# plt.xlabel("Salary ($1000s)")
# plt.ylabel("Frequency")
# plt.tight_layout()
# plt.show()

# --- Plot 3: Boxplot of salary by location ---
# plt.figure(figsize=(12, 6))
# sns.boxplot(x='Location', y='Salary Avg', data=df)
# plt.xticks(rotation=45, ha='right')
# plt.title("Salary Distribution by Location")
# plt.tight_layout()
# plt.show()

# --- Plot 4: Count plot by location ---
# plt.figure(figsize=(12, 6))
# sns.countplot(y='Location', data=df, order=df['Location'].value_counts().iloc[:10].index)
# plt.title("Top 10 Locations by Number of Listings")
# plt.tight_layout()
# plt.show()

# --- Plot 5: Correlation heatmap ---
# plt.figure(figsize=(8, 6))
# sns.heatmap(df[['Company Score', 'Salary Min', 'Salary Max', 'Salary Avg']].corr(), annot=True, cmap='coolwarm')
# plt.title("Correlation Heatmap")
# plt.tight_layout()
# plt.show()

# --- Plot 6: Line plot of average salary over time ---
# df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
# df_sorted = df.dropna(subset=['Date', 'Salary Avg']).sort_values('Date')
# df_grouped = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))['Salary Avg'].mean()
# df_grouped.plot(figsize=(10, 5))
# plt.title("Average Salary Over Time")
# plt.xlabel("Date")
# plt.ylabel("Average Salary")
# plt.tight_layout()
# plt.show()
