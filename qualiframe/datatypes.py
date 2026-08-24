import pandas as pd
import re

"""
Datatype detection module.

This module identifies the likely datatype of each column in a DataFrame.
It can detect numeric types, categorical data, boolean values, emails,
phone numbers, URLs, dates, times, months, years, and general text.

The detect_datatype() function combines all individual detection methods
and returns the detected datatype for each column.
"""

def numeric(series):
    """
    Detect whether a series contains Integer or Float values.
    Returns None if the values cannot be converted to numeric data.
    """
    try:
        converted = pd.to_numeric(series)
        if (converted % 1 == 0).all():
            return "Integer"
        else:
            return "Float"
    except Exception:
        return None


def category(series):
    """
    Detect categorical columns based on the number and ratio of unique values.
    A column is considered categorical when it has at most 10 unique values
    and the unique-value ratio is below 10%.
    """
    unique = series.nunique()
    total = len(series)

    ratio = unique / total

    if unique <= 10 and ratio < 0.10:
        return "Categorical"
    else:
        return None


def boolean(series, lower_values):
    """
    Detect columns containing boolean-like values such as True/False,
    Yes/No, Y/N, 1/0, On/Off, etc.
    """
    bool_values = {
        "true", "false",
        "no", "yes",
        "y", "n",
        "1", "0",
        "t", "f",
        "on", "off",
    }

    unique = set(lower_values)

    if unique.issubset(bool_values) and len(unique) <= 2:
        return "Boolean"
    else:
        return None


def email(series, values):
    """
    Detect email columns using a regular expression pattern.
    Returns Email if more than 90% of the values match the pattern.
    """
    pattern = re.compile(
        r'^[A-Za-z0-9,_%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    )

    valid = values.apply(lambda x: bool(pattern.match(x)))

    if valid.mean() > 0.9:
        return "Email"
    else:
        return None


def phoneno(series, values):
    """
    Detect phone number columns using a regular expression pattern.
    Supports optional '+' prefixes and phone numbers containing 7 to 15 digits.
    """
    pattern = re.compile(r'^\+?\d{7,15}$')

    valid = values.apply(lambda x: bool(pattern.match(x)))

    if valid.mean() > 0.9:
        return "Phone number"
    else:
        return None


def url(series, values):
    """
    Detect URL columns using HTTP/HTTPS or www. patterns.
    """
    pattern = re.compile(r'^https?://|www\.')

    valid = values.apply(lambda x: bool(pattern.match(x)))

    if valid.mean() > 0.9:
        return "URL"
    else:
        return None


def datetime(values, col):
    """
    Detect whether a column contains Date, Time, or Datetime values.
    The function first checks whether the values appear date/time-like,
    then attempts conversion using pandas datetime parsing.
    """
    sample = values.head(20)

    date_like = sample.str.contains(
        r"[-/:.]|\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}",regex=True).mean()

    if date_like < 0.5:
        return None

    converted = pd.to_datetime(values,errors="coerce", format="mixed"
    )

    if converted.notna().mean() < 0.9:
        return None

    sample = values.iloc[0]

    has_date = any(sep in sample for sep in ["/", "-", "."])
    has_time = ":" in sample

    if has_date and has_time:
        return "Datetime"

    elif has_date:
        return "Date"

    elif has_time:
        return "Time"

    return None


def year_month(series):
    """
    Detect columns containing month names or year values.
    Recognizes full and abbreviated month names and years between
    1000 and 2200.
    """
    values = series.dropna().astype(str).str.strip()

    months = {
        "jan", "january", "feb", "february", "mar", "march",
        "apr", "april", "may", "jun", "june", "jul", "july",
        "aug", "august", "sep", "sept", "september",
        "oct", "october", "nov", "november", "dec", "december"
    }

    lower = values.str.lower()

    if lower.isin(months).mean() > 0.9:
        return "Month"

    try:
        num = pd.to_numeric(values, errors='coerce')

        if (num % 1 == 0).all():
            if num.between(1000, 2200).all():
                return "Year"
    except:
        pass

    return None


def detect_datatype(df):
    """
    Detect the datatype of every column in the DataFrame.

    Each column is tested against multiple datatype detection functions.
    The first matching datatype is assigned to the column. If no specific
    datatype is detected, the column is classified as Text.

    Returns
    -------
    dict
        Dictionary containing column names and their detected datatypes.
    """
    datatype_dict = {}

    for col in df.columns:
        cols = df[col].dropna()
        

        if cols.empty:
         datatype_dict[col] = "Empty"
         continue

        # Sample up to 1000 values for efficient datatype detection
        series = cols.sample(min(1000, len(cols)), random_state=42)

        lower_values = series.astype(str).str.strip().str.lower()
        str_values = series.astype(str).str.strip()

        dtype = (
            boolean(series, lower_values)
            or datetime(str_values, col)
            or email(series, str_values)
            or phoneno(series, str_values)
            or url(series, lower_values)
            or year_month(series)
            or numeric(series)
            or category(series)
            or "Text"
        )

        datatype_dict[col] = dtype

    return datatype_dict