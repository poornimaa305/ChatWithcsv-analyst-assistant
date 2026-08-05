import pandas as pd
import re

# Load the CSV and normalize column names to lowercase
df = pd.read_csv("sales.csv")
df.columns = df.columns.str.lower()

question = input("Ask a question: ").lower()

# Helper to parse a requested row count from text
def parse_row_count(text):
    match = re.search(r"(\d+)\s*(?:rows|row|records)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"(?:top|first|head)\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None

# General dataset queries
num_rows = parse_row_count(question)
if "show data" in question or "display data" in question or "show dataset" in question:
    print(df)
elif "dataset info" in question or "data info" in question or "dataset information" in question:
    print(f"Number of rows: {len(df)}")
    print(f"Number of columns: {len(df.columns)}")
elif num_rows is not None and ("top" in question or "head" in question or "first" in question or "rows" in question or "records" in question):
    print(df.head(num_rows))
elif "top 5" in question or "top five" in question or "head" in question:
    print(df.head())
elif "how many rows" in question or "row count" in question or ("rows" in question and "how" in question):
    print(f"Number of rows: {len(df)}")
elif "columns" in question or "list columns" in question or "column names" in question:
    print("Columns:")
    for col in df.columns:
        print(f"- {col}")
elif "data type" in question or "data types" in question or "dtypes" in question:
    print("Column data types:")
    print(df.dtypes)
elif "missing" in question or "null" in question or "na" in question:
    print("Missing values per column:")
    print(df.isnull().sum())
elif "describe" in question or "summary" in question or "summarize" in question or "statistical summary" in question:
    print("Dataset summary:")
    print(df.describe(include='all'))
elif "correlation" in question or "correlation matrix" in question or "correlations" in question:
    print("Correlation matrix:")
    print(df.corr(numeric_only=True))
else:
    # Numeric operations on a column
    column_name = None
    for col in df.columns:
        if col in question:
            column_name = col
            break

    if column_name:
        friendly_name = column_name.replace("_", " ").title()
        if "highest" in question or "max" in question:
            result = df[column_name].max()
            print(f"The highest {friendly_name} is {result}.")
        elif "lowest" in question or "min" in question:
            result = df[column_name].min()
            print(f"The lowest {friendly_name} is {result}.")
        elif "average" in question or "mean" in question:
            result = df[column_name].mean()
            print(f"The average {friendly_name} is {result}.")
        elif "total" in question or "sum" in question:
            result = df[column_name].sum()
            print(f"The total {friendly_name} is {result}.")
        else:
            print(f"I found the column {friendly_name}, but could not determine the operation.")
    else:
        print("Sorry, I couldn't understand the question. Try: show data, top 5 rows, how many rows, list columns, or ask about a column.")