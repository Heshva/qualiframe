def statistics(df):
    """
    Generate statistical information for numeric columns.

    Parameters
    ----------
    df : DataFrame
        Input DataFrame.

    Returns
    -------
    dict
        Contains descriptive statistics, skewness, and kurtosis.
    """

    # Select only numeric columns for statistical analysis
    numeric_df = df.select_dtypes(include="number")

    # Calculate descriptive statistics and distribution measures
    result = {
        # Count, mean, standard deviation, minimum, maximum, and quartiles
        "describe": numeric_df.describe().round(2),
        
        # Measure the asymmetry of each numeric column
        "skewness": numeric_df.skew().round(2),
        
        # Measure the shape/tailedness of the distribution
        "kurtosis": numeric_df.kurt().round(2)
    }

    return result