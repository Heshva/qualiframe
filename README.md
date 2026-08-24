# QualiFrame

**QualiFrame** is a Python package for automated **data quality analysis and reporting**. It analyzes tabular datasets and generates useful statistics, quality checks, visualizations, and a PDF report.

## Installation

```bash
pip install qualiframe
```

## Usage

```python
from qualiframe import audit
audit("data.csv", output_dir="output")
```

QualiFrame automatically checks:

* Missing values
* Duplicate records
* Data types
* Statistical summaries
* Correlations
* Data distributions
* Overall data quality

A structured **PDF audit report** is generated in the specified output directory.

## Requirements

Python 3.10+

Built with **Pandas, Matplotlib, Seaborn, and ReportLab**.

## Author

**Heshva**

## License

No license specified.
