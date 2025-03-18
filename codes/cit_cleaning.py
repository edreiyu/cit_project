# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 14:40:58 2025
@author: Edrei
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Define file path
file_path = "D:\\cit_project\\data"
file_name = "1702RT_v2018_2023_sample.csv"

# Load CSV file
def load_data(file_path, file_name):
    full_path = os.path.join(file_path, file_name)
    df = pd.read_csv(full_path)
    return df

# Data exploration
def explore_data(df):
    print("Data Summary:\n", df.info())
    print("\nDescriptive Statistics:\n", df.describe())
    print("\nMissing Values:\n", df.isnull().sum())

# Check
# df["43 Tax Due "].describe()
# explore_data(df["43 Tax Due "])

# Data cleaning
def clean_data(df):
    # Select columns to retain in analysis
    selected_columns = ["43 Tax Due", "column_2", "column_3", "column_4"]  # Replace with actual column names
    required_columns = ["43 Tax Due", "column_2", "column_3"]  # Replace with actual column names
    df_cleaned = df.dropna(subset=required_columns)  # Remove rows with NaN in all specified columns
    # df_cleaned.to_csv("cleaned_data.csv", index=False)
    return df_cleaned

# Save into dataframes
data_x = clean_data(x)
data_y = clean_data(y)

# Merge two cleaned datasets
def merge_data(df1, df2):
    df_merged = pd.concat([df1, df2], ignore_index=True)
    df_merged.to_csv("merged_data.csv", index=False)
    return df_merged


# Create two separate cleaned datasets
def create_cleaned_datasets(df):
    selected_columns = ["43 Tax Due", "column_2", "column_3", "column_4"]  # Replace with actual column names
    df_selected = df[selected_columns]
    
    required_columns = ["43 Tax Due", "column_2", "column_3"]
    df1 = df_selected.dropna(subset=required_columns)
    df2 = df_selected.dropna(subset=required_columns)
    
    return df1, df2


#  Optional to save as csv
    # df1.to_csv("df1.csv", index=False)
    # df2.to_csv("df2.csv", index=False)

# Statistical analysis
def analyze_data(df):
    df['Decile'] = pd.qcut(df['numeric_column'], 10, labels=False)
    summary = df.groupby(['Industry', 'Decile'])['numeric_column'].agg(['mean', 'std']).reset_index()
    return summary

# Data visualization
def visualize_data(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Industry', y='numeric_column', data=df)
    plt.xticks(rotation=45)
    plt.title("Industry-wise Distribution")
    plt.savefig("visualization.png")
    plt.show()

# Quarto report (write a .qmd template separately)
def generate_report():
    with open("report.qmd", "w") as f:
        f.write("""
---
title: "Data Analysis Report"
format: html
---

# Data Overview
```{python}
df = pd.read_csv("cleaned_data.csv")
df.head()
```

# Statistical Summary
```{python}
summary = analyze_data(df)
summary
```

# Data Visualization
```{python}
from IPython.display import display
from PIL import Image
display(Image.open("visualization.png"))
```
        """)
    print("Quarto report created: report.qmd")

if __name__ == "__main__":
    df = load_data(file_path, file_name)
    explore_data(df)
    df_cleaned = clean_data(df)
    summary = analyze_data(df_cleaned)
    visualize_data(df_cleaned)
    generate_report()
