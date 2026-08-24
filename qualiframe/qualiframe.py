from .loader import load
from .summary import summary
from .data_statistics import statistics
from .datatypes import detect_datatype
from .duplicate_data import duplicate_report
from .data_quality import data_quality_score
from .correlation import correlation_heatmap
from .suggestions import generate_suggestions
from .report import generate_report

def audit(file):
    df = load(file)
    
    if df is None:
     return

    datatype_report = detect_datatype(df)
    summary_report = summary(df)
    statistics_report = statistics(df)
    duplicate_data = duplicate_report(df)
    score, quality = data_quality_score(df)
    suggestions = generate_suggestions(df)
    heatmap_file = correlation_heatmap(
     df,
     "correlation_heatmap.png"
 )

    generate_report(
    file=file,
    df=df,
    datatype_data=datatype_report,
    summary_report=summary_report,
    statistics_report=statistics_report,
    duplicate_data=duplicate_data,
    suggestion = suggestions,
    heatmap_file=heatmap_file

)
    
    
   
   