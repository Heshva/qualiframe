def data_quality_score(df):
    """
    Calculate an overall data quality score and rating.

    The score evaluates:
        1. Missing data
        2. Duplicate rows
        3. Completely empty columns
        4. Constant columns
        5. Data type consistency

    Returns
    -------
    tuple
        (overall_score, quality_rating)
    """

    # =====================================================
    # EMPTY DATASET
    # =====================================================

    if df.empty or len(df.columns) == 0:
        return 0, "Poor"

    # =====================================================
    # 1. MISSING DATA SCORE
    # =====================================================

    total_cells = df.size

    missing_cells = df.isna().sum().sum()

    missing_percentage = (
        missing_cells / total_cells
    ) * 100

    missing_score = max(
        0,
        100 - missing_percentage
    )

    # =====================================================
    # 2. DUPLICATE ROW SCORE
    # =====================================================

    duplicate_rows = df.duplicated().sum()

    duplicate_percentage = (
        duplicate_rows / len(df)
    ) * 100

    duplicate_score = max(
        0,
        100 - duplicate_percentage
    )

    # =====================================================
    # 3. EMPTY COLUMN SCORE
    # =====================================================

    empty_columns = df.isna().all().sum()

    empty_percentage = (
        empty_columns / len(df.columns)
    ) * 100

    empty_column_score = max(
        0,
        100 - empty_percentage
    )

    # =====================================================
    # 4. CONSTANT COLUMN SCORE
    # =====================================================

    # Columns containing only one unique non-null value
    constant_columns = 0

    for col in df.columns:

        unique_values = df[col].nunique(
            dropna=True
        )

        if unique_values <= 1:
            constant_columns += 1

    constant_percentage = (
        constant_columns / len(df.columns)
    ) * 100

    constant_score = max(
        0,
        100 - constant_percentage
    )

    # =====================================================
    # 5. DATA TYPE CONSISTENCY SCORE
    # =====================================================

    # Count columns where pandas detected an object type.
    #
    # Object columns are not automatically bad, because
    # they can legitimately contain text/categorical data.
    #
    # Therefore we only penalize object columns when they
    # appear to contain mixed data types.

    inconsistent_columns = 0

    for col in df.columns:

        if df[col].dtype == "object":

            non_null = df[col].dropna()

            if len(non_null) > 0:

                detected_types = (
                    non_null
                    .map(type)
                    .nunique()
                )

                if detected_types > 1:
                    inconsistent_columns += 1

    datatype_percentage = (
        inconsistent_columns / len(df.columns)
    ) * 100

    datatype_score = max(
        0,
        100 - datatype_percentage
    )

    # =====================================================
    # FINAL WEIGHTED SCORE
    # =====================================================

    score = (
        missing_score * 0.35
        + duplicate_score * 0.20
        + empty_column_score * 0.15
        + constant_score * 0.10
        + datatype_score * 0.20
    )

    score = round(
        score,
        2
    )

    # =====================================================
    # QUALITY RATING
    # =====================================================

    if score >= 90:
        rating = "Excellent"

    elif score >= 75:
        rating = "Good"

    elif score >= 50:
        rating = "Needs Improvement"

    else:
        rating = "Poor"

    return score, rating

