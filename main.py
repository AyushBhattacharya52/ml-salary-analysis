import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import re
from datetime import datetime, timedelta

# === Setup ===
plt.style.use('ggplot')
pd.set_option('display.max_columns', None)

# === Load and Clean Data ===
df = pd.read_csv(r'ExploratoryDataAnalysis\data\Software Engineer Salaries.csv')
df = df.drop(columns=["Job Title"], errors="ignore")

# === Extract Salary Min/Max/Avg from 'Salary' string ===
def extract_salary_range(s):
    try:
        s = s.split('(')[0]  # Remove any text in parentheses
        s = s.replace('$', '').replace('K', '')  # Remove $ and K
        parts = s.split('-')
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
    except:
        return np.nan, np.nan
    return np.nan, np.nan

df[['Salary Min', 'Salary Max']] = df['Salary'].apply(lambda x: pd.Series(extract_salary_range(x)))
df['Salary Avg'] = df[['Salary Min', 'Salary Max']].mean(axis=1)

# Ensure Company Score is numeric
df['Company Score'] = pd.to_numeric(df['Company Score'], errors='coerce')

# === Convert Relative Dates (e.g., '3 days ago') to Timestamps ===
def convert_relative_date(x):
    try:
        x = str(x).lower()
        if 'just posted' in x:
            return datetime.today()
        match = re.search(r'(\d+)', x)
        if match:
            days_ago = int(match.group(1))
            return datetime.today() - timedelta(days=days_ago)
    except:
        return np.nan
    return np.nan

df['Date'] = df['Date'].apply(convert_relative_date)

# === Drop rows without dates or salary info ===
df_sorted = df.dropna(subset=['Date', 'Salary Min', 'Salary Max', 'Salary Avg']).sort_values('Date')

# === Create cumulative sums for salaries ===
df_sorted['Cumulative Salary Min'] = df_sorted['Salary Min'].cumsum()
df_sorted['Cumulative Salary Max'] = df_sorted['Salary Max'].cumsum()
df_sorted['Cumulative Salary Avg'] = df_sorted['Salary Avg'].cumsum()

# === Plot cumulative salary over time ===
plt.figure(figsize=(12, 6))
plt.plot(df_sorted['Date'], df_sorted['Cumulative Salary Min'], label='Cumulative Min Salary', linestyle='--')
plt.plot(df_sorted['Date'], df_sorted['Cumulative Salary Max'], label='Cumulative Max Salary', linestyle='--')
plt.plot(df_sorted['Date'], df_sorted['Cumulative Salary Avg'], label='Cumulative Avg Salary', linewidth=2)
plt.xlabel("Date")
plt.ylabel("Cumulative Salary ($1000s)")
plt.title("Cumulative Salary Progression Over Time")
plt.legend()
plt.tight_layout()
plt.show()


# === Plot 1: Pairplot of numeric features ===
"""
sns.pairplot(df, vars=['Company Score', 'Salary Min', 'Salary Max', 'Salary Avg'], kind='reg')
plt.title("Pairwise Relationships Between Numerical Features")
plt.show()
"""

# === Plot 2: Top 10 Companies by Listings ===
"""
df['Company'].value_counts().head(10).plot(kind='barh', figsize=(10, 6), color='skyblue')
plt.title("Top 10 Companies by Number of Job Listings")
plt.xlabel("Number of Listings")
plt.ylabel("Company")
plt.tight_layout()
plt.show()
"""

# === Plot 3: Histogram of Average Salaries ===
"""
df['Salary Avg'].dropna().plot(kind='hist', bins=30, figsize=(10, 6), color='coral')
plt.title("Distribution of Average Salaries")
plt.xlabel("Salary ($1000s)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
"""

# === Plot 4: Boxplot of Salary by Location ===
"""
plt.figure(figsize=(12, 6))
sns.boxplot(x='Location', y='Salary Avg', data=df)
plt.xticks(rotation=45, ha='right')
plt.title("Salary Distribution by Location")
plt.tight_layout()
plt.show()
"""

# === Plot 5: Top 10 Locations by Count ===
"""
plt.figure(figsize=(12, 6))
sns.countplot(y='Location', data=df, order=df['Location'].value_counts().iloc[:10].index)
plt.title("Top 10 Locations by Number of Listings")
plt.tight_layout()
plt.show()
"""

# === Plot 6: Correlation Heatmap ===
"""
plt.figure(figsize=(8, 6))
sns.heatmap(df[['Company Score', 'Salary Min', 'Salary Max', 'Salary Avg']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap of Numeric Features")
plt.tight_layout()
plt.show()
"""

# === Plot 7: Average Salary Over Time (Monthly) ===
'''''''''
df_sorted = df.dropna(subset=['Date', 'Salary Avg']).sort_values('Date')
df_grouped = df_sorted.groupby(df_sorted['Date'].dt.to_period('M'))['Salary Avg'].mean()
df_grouped.index = df_grouped.index.to_timestamp()  # Convert PeriodIndex to TimestampIndex

if not df_grouped.empty:
    df_grouped.plot(figsize=(10, 5), marker='o')
    plt.title("Average Salary Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Salary")
    plt.tight_layout()
    plt.show()
else:
    print("No data available to plot average salary over time.")
'''''''''''
