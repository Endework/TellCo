import pandas as pd
import os
import sys
import numpy as np  # Import numpy for numeric data type checking
from datetime import datetime

# Get the absolute path to the parent directory of the notebook
current_dir = os.path.abspath(r'C:\\Users\\ende\\Desktop\\10x\\Week-2\\scripts')
# Get the absolute path to the parent directory of the notebook's parent directory
project_dir = os.path.dirname(current_dir)
# Add the project directory to the Python path
sys.path.append(project_dir)
from src.utils import missing_values_table

def clean_data(df):
    # Convert 'Start' and 'End' to datetime format and drop rows with null values in these columns
    for column in ['Start', 'End']:
        df.loc[:, column] = pd.to_datetime(df.loc[:, column], errors='coerce')
        df = df.loc[df[column].notna()]

    # Get the DataFrame of missing values
    missing_df = missing_values_table(df)

    # Get columns with more than 50% missing values
    #columns_to_drop = missing_df[missing_df['% of Total Values'] > 50].index

    # Drop these columns
    #df = df.drop(columns_to_drop, axis=1)

    # Get columns with missing values that are left
    columns_with_na = df.columns[df.isna().any()].tolist()

    # Fill missing values with mean for numeric columns and with the most frequent value for non-numeric columns
    for column in columns_with_na:
        if pd.api.types.is_numeric_dtype(df[column].dtype):
            # Check if all values in the column can be converted to numeric values
            try:
                df[column] = pd.to_numeric(df[column])
                df[column] = df[column].fillna(df[column].mean())
            except ValueError:
                print(f"Column {column} contains non-numeric values.")
                df[column] = df[column].fillna(df[column].mode()[0])
        else:
            df[column] = df[column].fillna(df[column].mode()[0])

    return df
