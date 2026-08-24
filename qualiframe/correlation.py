import matplotlib.pyplot as plt
import seaborn as sns


def correlation_heatmap(df, output_file="correlation_heatmap.png"):
    """
    Generate and save a correlation heatmap for numerical columns.

    Empty and constant columns are removed before calculating
    correlations. Returns None if there are not enough usable
    numerical columns to create a meaningful heatmap.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataset.

    output_file : str, optional
        Path where the heatmap will be saved.

    Returns
    -------
    str or None
        Output file path if successful, otherwise None.
    """

    # Select numerical columns and remove empty/constant columns
    numeric_df = df.select_dtypes(include="number").copy()
    numeric_df = numeric_df.dropna(axis=1,how="all")
    numeric_df = numeric_df.loc[:,numeric_df.nunique(dropna=True) > 1]

    # At least two columns are required for correlation analysis
    if numeric_df.shape[1] < 2:
        return None

    # Calculate correlation matrix
    correlation = numeric_df.corr()

    # Remove columns with no valid correlation values
    correlation = correlation.dropna(axis=0,how="all").dropna(axis=1,how="all")

    if correlation.shape[0] < 2:
        return None

    # Create and plot the correlation heatmap
    plt.figure(figsize=(15, 9))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm_r",
        vmin=-1,
        vmax=1,
        linewidths=0.5
    )

    plt.title( "Correlation Heatmap",fontsize=14,fontweight="bold")
    plt.xticks(rotation=45,ha="right")
    plt.tight_layout()

    # Save the heatmap
    plt.savefig(output_file, dpi=200,bbox_inches="tight")
    plt.close()

    return output_file