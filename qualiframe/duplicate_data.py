def duplicate_report(df):
    """
    Generate a report on duplicate rows in the DataFrame.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame to check for duplicate rows.

    Returns
    -------
    dict
        Contains the number and percentage of duplicate rows.
    """

    # Count the number of duplicate rows
    duplicate_count = df.duplicated().sum()

    # Calculate duplicate percentage only if the DataFrame is not empty
    if len(df) > 0:
        duplicate_percentage = (duplicate_count / len(df) * 100)
    else:
        duplicate_percentage = 0

    # Return duplicate count and percentage
    return {
        "Duplicate Rows": duplicate_count,
        "Duplicate Percentage": round(duplicate_percentage, 2)
    }