from pathlib import Path

from .loader import load
from .summary import summary
from .data_statistics import statistics
from .datatypes import detect_datatype
from .duplicate_data import duplicate_report
from .data_quality import data_quality_score
from .correlation import correlation_heatmap
from .suggestions import generate_suggestions
from .report import generate_report


def audit(file, output_dir=None):
    """Run a complete data-quality audit and generate a PDF report."""

    file_path = Path(file)

    # Save outputs beside the input file by default.
    if output_dir is None:
        output_dir = file_path.parent
    else:
        output_dir = Path(output_dir)

    # Create the output directory if it does not exist.
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load(file)

    if df is None:
        return

    datatype_report = detect_datatype(df)
    summary_report = summary(df)
    statistics_report = statistics(df)
    duplicate_data = duplicate_report(df)
    score, quality = data_quality_score(df)
    suggestions = generate_suggestions(df)
    heatmap_file = correlation_heatmap(df,output_dir / "correlation.png")

    # Generate PDF report in the same output directory.
    generate_report(
        file=file,
        df=df,
        datatype_data=datatype_report,
        summary_report=summary_report,
        statistics_report=statistics_report,
        duplicate_data=duplicate_data,
        suggestion=suggestions,
        heatmap_file=heatmap_file,
        output_dir=output_dir
    )