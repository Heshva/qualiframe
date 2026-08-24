def summary(df):
    """
    Generate a summary of the input DataFrame.

    Includes basic information such as:
        - Memory usage
        - Number of rows and columns
        - Numeric and text columns
        - Duplicate rows
        - Unique values
        - Data types
        - Missing values and percentages
        - Completely empty columns

    Parameters
    ----------
    df : DataFrame
        Input DataFrame to summarize.

    Returns
    -------
    dict
        Dictionary containing the summary information.
    """

    print('Summarizing data')

    # Calculate basic dataset and data-quality information
    summary = {
        # Total memory used by the DataFrame in MB
        "Memory Usage (MB)": (df.memory_usage(deep=True).sum() / 1024 ** 2).round(2),

        # Number of columns and rows
        "Total Columns": len(df.columns),
        "Total Rows": len(df),

        # Identify columns based on their data type
        "Numeric Columns": df.select_dtypes(include="number").columns.tolist(),
        "Text Columns": df.select_dtypes(include="object").columns.tolist(),

        # Count completely duplicated rows
        "Duplicate Rows": df.duplicated().sum(),

        # List all column names
        "Column Names": list(df.columns),

        # Count unique non-missing values in each column
        "Unique Values": df.nunique(dropna=True).to_dict(),

        # Get the data type of each column
        "Data Types": df.dtypes.astype(str).to_dict(),

        # Count missing values in each column
        "Missing Values": df.isna().sum().to_dict(),

        # Identify columns where all values are missing
        "Empty Columns": df.columns[df.isna().all()].tolist(),

        # Calculate missing values as a percentage for each column
        "Missing Percentage": ((df.isna().mean() * 100).round(2)).to_dict(),
    }

    return summary