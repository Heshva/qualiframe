\# QualiFrame



\*\*QualiFrame\*\* is a Python package for automated \*\*data-quality auditing and exploratory data analysis\*\*.



It analyzes a Pandas DataFrame and generates a structured PDF report containing key data-quality insights, statistics, visualizations, and recommendations.



\## Features



\* Dataset summary

\* Automatic datatype detection

\* Missing-value analysis

\* Empty and constant column detection

\* Duplicate-row analysis

\* Descriptive statistics

\* Correlation analysis

\* Automated data-quality recommendations

\* Professional PDF report generation



\## Installation



Install QualiFrame directly from PyPI:



```bash

pip install qualiframe

```



\## Usage



```python

from qualiframe import audit



audit(data.csv)

```



QualiFrame analyzes the dataset and generates a PDF audit report.



\## What the Report Provides



The generated report includes:



\* Dataset overview

\* Column-level information

\* Missing-data analysis

\* Duplicate analysis

\* Statistical summary

\* Correlation visualization

\* Data-quality recommendations



\## Example Workflow



```text

CSV / Pandas DataFrame

&#x20;       │

&#x20;       ▼

&#x20;   QualiFrame

&#x20;       │

&#x20;       ├── Data Quality Analysis

&#x20;       ├── Statistics

&#x20;       ├── Correlation Analysis

&#x20;       └── Recommendations

&#x20;       │

&#x20;       ▼

&#x20;   PDF Audit Report

```



\## Requirements



\* Python 3.10+

\* pandas

\* matplotlib

\* seaborn

\* reportlab



\## Intended Use



QualiFrame can be used for:



\* Data-quality screening

\* Exploratory data analysis

\* Research datasets

\* Sensor and environmental datasets

\* Time-series datasets

\* Machine-learning preprocessing



\## Note



QualiFrame is a \*\*screening and reporting tool\*\*. Its recommendations should be reviewed before making changes to the original dataset.



\## Version



\*\*0.1.0\*\*



\## Author



\*\*Heshva\*\*

\[Github](https://github.com/Heshva)



\*\*QualiFrame — Automated Data Quality Auditing for Python\*\*



