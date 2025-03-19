# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 14:40:58 2025
@author: Edrei
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# %% Defining functions

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
    
# Data cleaning
def clean_data(df):
    # Select columns to retain in analysis
    selected_columns = ["PSIC CODE", "PSIC Description", "Reference No", "5 ATC", "10 Date of Incorporation",
                        "Source", "RDO Reg     ",
                        "13 Method of Deductions ", "14 Tax Due ", "21 TOTAL AMOUNT PAYABLE / (Overpayment)", 
                        "27 Sales/Receipts/Revenues/Fees", "29 Net Sales/Receipts/Revenues/Fees",
                        "30 Less: Cost of Sales/Services", "31 Gross Income from Operation ",
                        "33 Total Taxable Income ", "34 Ordinary Allowable Itemized Deductions ", 
                        "36 N O L C O", "37 Total Deductions", "38 Optional Standard Deduction (OSD) ",
                        "39 Net Taxable Income/(Loss)", "40 Applicable Income Tax Rate",
                        "41 Income Tax Due other than Minimum Corporate Income Tax (MCIT)", 
                        "42 MCIT Due ", "43 Tax Due ", "56 Net Tax Payable / (Overpayment)"]
    df = df[selected_columns]   
    required_columns = ["29 Net Sales/Receipts/Revenues/Fees", "31 Gross Income from Operation ", 
                        "39 Net Taxable Income/(Loss)", "43 Tax Due "]
    df_cleaned = df.dropna(subset=required_columns)  # Drop rows with NaN in all required columns
    # Convert column to numeric to avoid errors
    df_cleaned["27 Sales/Receipts/Revenues/Fees"] = pd.to_numeric(df_cleaned["27 Sales/Receipts/Revenues/Fees"], errors='coerce')
    # Assign deciles based on "27 Sales/Receipts/Revenues/Fees"
    df_cleaned["Decile"] = pd.qcut(df_cleaned["27 Sales/Receipts/Revenues/Fees"], 10, labels=False, duplicates="drop")
    return df_cleaned

cleaned_df1 = clean_data(df)
des = cleaned_df1.describe()
print(cleaned_df1.dtypes) # check datatypes of selected columns 
print(cleaned_df1.isnull().sum()) # check number of nulls in a column e.g. 4,111 nulls in PSIC Description
cleaned_df1.to_csv("data/cleaned_df1.csv", index=True) #Optional to save as csv

# Check distribution of deciles
summary = cleaned_df1.groupby('Decile')['27 Sales/Receipts/Revenues/Fees'].agg(['count','mean', 'std']).reset_index()
    

# %% Data visualization

def dist_num(df, cat_col, num_col):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=cat_col, y=num_col, data=df)
    plt.xticks(rotation=45)
    plt.title("Decile Distribution")
    # Save the plot as an image file
    plt.savefig(f"{num_col}_by_{cat_col}.png", dpi=300, bbox_inches='tight')
    plt.show()
dist_num(cleaned_df1, "Decile", "43 Tax Due ")

def groupby_num(df, cat_col, num_col):
    grouped_df = df.groupby(cat_col)[num_col].sum().reset_index() # Aggregate total of num_col by cat_col
    plt.figure(figsize=(12, 6))
    # Create a bar chart
    plt.bar(grouped_df[cat_col], grouped_df[num_col], color="royalblue")
    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha="right")
    # Set labels and title
    plt.xlabel(cat_col)
    plt.ylabel(f"Total {num_col}")
    plt.title(f"Total {num_col} by {cat_col}")
    # Save the plot as an image file
    plt.savefig(f"{num_col}_by_{cat_col}.png", dpi=300, bbox_inches='tight')
    plt.show()
groupby_num(cleaned_df1, "Decile", "43 Tax Due ")


# %% Quarto report (write a .qmd template separately)

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
    groupby_num(cleaned_df1, "Decile", "43 Tax Due ")
    generate_report()

# %% Notes

# Check
# df["43 Tax Due "].describe()
# explore_data(df["43 Tax Due "])


# Save into dataframes
# data_x = clean_data(x)
# data_y = clean_data(y)

    # df_cleaned.to_csv("cleaned_data.csv", index=False)

    # df2 = df_selected.dropna(subset=required_columns)
    # return df1, df2


#  Optional to save as csv
    # df1.to_csv("df1.csv", index=False)
    # df2.to_csv("df2.csv", index=False)
    
#%% When merging
    
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

    
    
