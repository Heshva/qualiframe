import pandas as pd

def generate_suggestions(df):
    """
    Generate simple, actionable suggestions based on
    common data-quality issues in the DataFrame.

    Returns
    -------
    list
        List of suggestions containing severity, title,
        and message.
    """

    if df.empty:
        return [{
            "severity": "High",
            "title": "Empty Dataset",
            "message": "The dataset contains no usable data."
        }]

    suggestions = []

    # Missing data
    missing = df.isna().mean() * 100

    empty_cols = missing[missing == 100].index.tolist()
    high_missing = missing[(missing >= 30) & (missing < 100)]
    low_missing = missing[(missing > 0) & (missing < 30)]

    if empty_cols:
        suggestions.append({
            "severity": "High",
            "title": "Empty Columns",
            "message": f"Consider dropping empty columns: {', '.join(empty_cols)}."})

    if not high_missing.empty:
        suggestions.append({
            "severity": "Medium",
            "title": "High Missing Data",
            "message": "Consider investigating or imputing columns with high missing values."})

    if not low_missing.empty:
        suggestions.append({
            "severity": "Low",
            "title": "Missing Data",
            "message": "Review columns containing missing values."})

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates:
        suggestions.append({
            "severity": "Medium",
            "title": "Duplicate Rows",
            "message": f"{duplicates} duplicate rows found. Consider removing them."})

    # Constant columns
    constant_cols = [
        col for col in df.columns
        if df[col].nunique(dropna=True) <= 1 and col not in empty_cols]

    if constant_cols:
        suggestions.append({
            "severity": "Medium",
            "title": "Constant Columns",
            "message": f"Consider removing constant columns: {', '.join(constant_cols)}."})

    # Object columns that may need conversion
    text_cols = df.select_dtypes(include="object").columns.tolist()

    if text_cols:
        suggestions.append({
            "severity": "Low",
            "title": "Text Columns",
            "message": (
                f"Review text columns for possible numeric or datetime conversion: "
                f"{', '.join(text_cols)}." )})

    # No issues found
    if not suggestions:
        suggestions.append({
            "severity": "Good",
            "title": "No Major Issues",
            "message": "No major data-quality issues were detected."})

    return suggestions