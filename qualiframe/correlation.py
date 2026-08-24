import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def correlation_heatmap(df, output_file="correlation_heatmap.png"):
    """
    Generate and save a correlation heatmap for numerical columns.
    """

    # Select numerical columns and remove empty/constant columns.
    numeric_df = df.select_dtypes(include="number").copy()

    numeric_df = numeric_df.dropna(
        axis=1,
        how="all"
    )

    numeric_df = numeric_df.loc[
        :,
        numeric_df.nunique(dropna=True) > 1
    ]

    # At least two columns are required.
    if numeric_df.shape[1] < 2:
        return None

    # Calculate correlation matrix.
    correlation = numeric_df.corr()

    # Remove columns with no valid correlation values.
    correlation = (
        correlation
        .dropna(axis=0, how="all")
        .dropna(axis=1, how="all")
    )

    if correlation.shape[0] < 2:
        return None

    # Create the heatmap.
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

    plt.title(
        "Correlation Heatmap",
        fontsize=14,
        fontweight="bold"
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.tight_layout()

    # Make sure the output path is handled correctly.
    output_file = Path(output_file)
    plt.savefig(str(output_file),dpi=200,bbox_inches="tight")

    plt.close()

    return str(output_file)