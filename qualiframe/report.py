from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Image
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

import pandas as pd
from pathlib import Path
from datetime import datetime


def generate_report(
    file,
    df,
    datatype_data,
    summary_report,
    statistics_report,
    duplicate_data,
    suggestion,
    heatmap_file,
    output_dir
):
    """Generate the complete PDF data quality report."""

    file_name = Path(file).stem
    output_path = str(Path(output_dir) / f"{file_name}_report.pdf")
    
    #Create the timestamp once so it stays the same throughout the report.
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Document

    doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=60,
    bottomMargin=55
)
    
    doc.timestamp = timestamp
    styles = getSampleStyleSheet()

    elements = []


    # Add the report title.
    add_title(elements,styles,file_name)

    # Add the main audit summary.
    add_audit_summary(elements,styles,df,summary_report,duplicate_data)
    
    add_suggestions(elements,styles,suggestion)

    # Add basic dataset information.
    add_dataset_summary(elements,styles,summary_report)

    # Add column-level information.
    add_datatype_table(elements,styles, df,datatype_data)

    # Add duplicate-row information.
    add_duplicate_section(elements,styles,duplicate_data)

    # Add numerical statistics.
    add_statistics(elements,styles, statistics_report)
    
    add_correlation_section(elements,styles,heatmap_file)


    doc.build(
    elements,
    onFirstPage=add_header_footer,
    onLaterPages=add_header_footer
)

    print("Report Generated Successfully.")
    print(f"Output: {output_path}")


def add_title(elements, styles, file_name):
    """Add the report title and file name to the PDF."""

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        leading=26,
        spaceAfter=8
    )

    file_style = ParagraphStyle(
        "FileName",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=colors.blue,  # Changed color to blue (you can use colors.red, colors.green, etc.)
        fontName="Helvetica-Bold",  # Added bold font
        spaceAfter=18
    )

    elements.append(
        Paragraph(
            "QualiFrame",
            title_style
        )
    )

    elements.append(
        Paragraph(
            f"Automated Data Quality Report",
            styles["Heading3"]
        )
    )

    elements.append(
        Paragraph(
            f"File: {file_name}",
            file_style
        )
    )

    elements.append(
        Spacer(1, 8)
    )


def add_audit_summary(elements,styles,df,summary_report,duplicate_data):
    """Add a quick overview of the main data quality checks."""

    elements.append(
        Paragraph(
            "Audit Summary",
            styles["Heading2"]
        )
    )

    # Missing data percentage

    if df.size > 0:
        missing_percentage = (
            df.isna().sum().sum() / df.size
        ) * 100
    else:
        missing_percentage = 0

    # Rows / Columns

    rows = len(df)
    columns = len(df.columns)

    # Duplicate rows

    duplicate_rows = duplicate_data.get(
        "Duplicate Rows",
        df.duplicated().sum()
    )

    # Summary table

    summary_data = [
        ["Metric", "Value"],

       
        [
            "Rows",
            rows
        ],

        [
            "Columns",
            columns
        ],

        [
            "Duplicate Rows",
            duplicate_rows
        ],

        [
            "Missing Data",
            f"{missing_percentage:.1f}%"
        ]
    ]

    table = Table(
        summary_data,
        colWidths=[220, 220]
    )

    table.setStyle(
        TableStyle([
            # Header
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            # Body
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                7
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            # Highlight score
            (
                "FONTNAME",
                (0, 1),
                (0, 2),
                "Helvetica-Bold"
            ),

            (
                "FONTNAME",
                (1, 1),
                (1, 2),
                "Helvetica-Bold"
            ),
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 22)
    )


def add_dataset_summary(elements, styles, data):
    """Add basic information about the dataset."""

    elements.append(
        Paragraph(
            "1. Dataset Summary",
            styles["Heading2"]
        )
    )

    empty_columns = len(data["Empty Columns"])

    table_data = [
        ["Metric", "Value"],
        ["Total Rows", data["Total Rows"]],
        ["Total Columns", data["Total Columns"]],
        ["Memory Usage (MB)", data["Memory Usage (MB)"]],
        ["Duplicate Rows", data["Duplicate Rows"]],
        ["Empty Columns", empty_columns]
    ]

    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table_style = [
        # Header
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.grey
        ),

        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),

        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),

        # Grid
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.black
        ),

        (
            "PADDING",
            (0, 0),
            (-1, -1),
            6
        ),

        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            9
        )
    ]

    # Highlight empty columns.

    if empty_columns > 0:

        # Show the count in red when empty columns exist.
        table_style.extend([
            (
                "TEXTCOLOR",
                (1, 5),
                (1, 5),
                colors.red
            ),

            (
                "FONTNAME",
                (1, 5),
                (1, 5),
                "Helvetica-Bold"
            )
        ])

    else:

        # Use green when there are no empty columns.
        table_style.extend([
            (
                "TEXTCOLOR",
                (1, 5),
                (1, 5),
                colors.green
            ),

            (
                "FONTNAME",
                (1, 5),
                (1, 5),
                "Helvetica-Bold"
            )
        ])

    table.setStyle(
        TableStyle(table_style)
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )


def add_datatype_table(elements,styles,df,datatype_data):
    """Add detected column types and missing-value details."""

    elements.append(
        Paragraph(
            "2. Column Information",
            styles["Heading2"]
        )
    )

    table_data = [
        [
            "Column",
            "Detected Type",
            "Missing",
            "Missing %",
            "Unique"
        ]
    ]

    # Keep track of columns that are completely empty.
    empty_row_indexes = []

    for col in df.columns:

        missing = df[col].isna().sum()

        if len(df) > 0:
            missing_percent = round(
                missing / len(df) * 100,
                2
            )
        else:
            missing_percent = 0

        unique = df[col].nunique(
            dropna=True
        )

        table_data.append([
            str(col),
            datatype_data.get(
                col,
                "Unknown"
            ),
            missing,
            missing_percent,
            unique
        ])

        # Mark columns that contain only missing values.
        if len(df) > 0 and missing == len(df):

            # Row 0 is the table header.
            empty_row_indexes.append(
                len(table_data) - 1
            )

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            105,
            100,
            65,
            65,
            65
        ]
    )

    table_style = [
        # Header

        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.grey
        ),

        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),

        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),

        # Grid

        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.black
        ),

        # Font

        (
            "FONTSIZE",
            (0, 0),
            (-1, -1),
            8
        ),

        (
            "PADDING",
            (0, 0),
            (-1, -1),
            4
        ),

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        )
    ]

    # Highlight completely empty columns

    for row_index in empty_row_indexes:

        # Highlight the empty column.
        table_style.append(
            (
                "BACKGROUND",
                (0, row_index),
                (-1, row_index),
                colors.lightpink
            )
        )

        # Make the warning stand out.
        table_style.append(
            (
                "TEXTCOLOR",
                (0, row_index),
                (-1, row_index),
                colors.red
            )
        )

        # Use bold text for the warning.
        table_style.append(
            (
                "FONTNAME",
                (0, row_index),
                (-1, row_index),
                "Helvetica-Bold"
            )
        )

    table.setStyle(
        TableStyle(table_style)
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )


def add_duplicate_section(elements,styles,data):
    """Add the duplicate-row results to the report."""

    elements.append(
        Paragraph(
            "3. Duplicate Analysis",
            styles["Heading2"]
        )
    )

    table_data = [
        ["Metric", "Value"],

        [
            "Duplicate Rows",
            data["Duplicate Rows"]
        ],

        [
            "Duplicate Percentage",
            f'{data["Duplicate Percentage"]:.2f}%'
        ]
    ]

    table = Table(
        table_data,
        colWidths=[220, 220]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            )
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )


def add_statistics(elements,styles,stats):
    """Add descriptive statistics for numerical columns."""

    elements.append(
        Paragraph(
            "4. Statistical Analysis",
            styles["Heading2"] ))

    elements.append(
        Paragraph(
            "Descriptive Statistics",
            styles["Heading3"]))

    describe_df = stats["describe"]

    skewness = stats.get(
        "skewness",
        {})

    kurtosis = stats.get(
        "kurtosis",
        {})

    # Build table
    #
    # Column | Mean | Min | Max | Std | Skew | Kurtosis

    table_data = [
        [
            "Column",
            "Mean",
            "Min",
            "Max",
            "Std",
            "Skew",
            "Kurtosis"
        ]
    ]

    # Get the columns included in the statistics.
    columns = list(describe_df.columns)

    for col in columns:

        # These values come from pandas describe().
        # mean, min, max, std

        mean = describe_df.loc[ "mean", col] if "mean" in describe_df.index else None

        minimum = describe_df.loc[ "min", col] if "min" in describe_df.index else None

        maximum = describe_df.loc["max", col] if "max" in describe_df.index else None

        std = describe_df.loc[ "std", col] if "std" in describe_df.index else None

        skew = skewness.get(col,None)

        kurt = kurtosis.get(col, None )

        table_data.append([
            str(col),

            f"{mean:.2f}"
            if pd.notna(mean)
            else "-",

            f"{minimum:.2f}"
            if pd.notna(minimum)
            else "-",

            f"{maximum:.2f}"
            if pd.notna(maximum)
            else "-",

            f"{std:.2f}"
            if pd.notna(std)
            else "-",

            f"{skew:.2f}"
            if pd.notna(skew)
            else "-",

            f"{kurt:.2f}"
            if pd.notna(kurt)
            else "-"
        ])

    # Split table if there are many columns

    # Keep the table narrow enough to fit on an A4 page.
    # Use a smaller font so all columns fit.

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=[
            95,     # Column
            55,     # Mean
            55,     # Min
            55,     # Max
            55,     # Std
            55,     # Skew
            65      # Kurtosis
        ]
    )

    table.setStyle(
        TableStyle([
            # Header
            ("BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.grey),

            ("TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white),

            ( "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"),

            # Grid
            ("GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.black),

            # Font
            ("FONTSIZE",
                (0, 0),
                (-1, -1),
                7.5),

            ("PADDING",
                (0, 0),
                (-1, -1),
                4),

            # Alignment
            ("ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER" ),

            ( "ALIGN",
                (0, 0),
                (0, -1),
                "LEFT"),

            ("VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            )]))

    elements.append(table)
    elements.append(Spacer(1, 20))
    
    
def add_correlation_section(elements,styles,heatmap_file):
    """Add the correlation heatmap to the report."""

    elements.append(Paragraph("5. Correlation Analysis", styles["Heading2"] ))

    if heatmap_file is None:
        elements.append(Paragraph("Correlation analysis requires at least two numerical columns.",styles["Normal"] ))
        elements.append(Spacer(1, 20))
        return

    image = Image(heatmap_file, width=500,height=400)

    elements.append(image)
    elements.append(Spacer(1, 20))


def add_header_footer(canvas, doc):
    """Draw the header and footer on each PDF page."""

    canvas.saveState()

    timestamp = doc.timestamp

    # Header
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(35, 810, "QualiFrame")

    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(92, 811, "Automated Data Quality Report")

    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        555,
        811,
        f"Generated: {timestamp}"
    )

    canvas.setStrokeColor(colors.grey)
    canvas.line(40, 798, 555, 798)

    # Footer
    canvas.line(40, 42, 555, 42)

    canvas.setFont("Helvetica", 8)

    canvas.drawString(
        40,
        27,
        "Generated by QualiFrame"
    )

    canvas.drawCentredString(
        297.5,
        27,
        "Automated Data Quality Report"
    )

    canvas.drawRightString(
        555,
        27,
        f"Page {doc.page}"
    )

    canvas.restoreState()
    
    
def add_suggestions(elements,styles,suggestions):
    """Add data-quality recommendations to the report."""

    elements.append(Paragraph("Recommendations", styles["Heading2"]))

    # Nothing to show when there are no recommendations.

    if not suggestions:
        elements.append(Paragraph("No recommendations available.",styles["Normal"]))
        elements.append( Spacer(1, 20))
        return

    # Create one recommendation box for each suggestion

    for suggestion in suggestions:

        severity = suggestion.get("severity","Low")
        title = suggestion.get("title","Recommendation")
        message = suggestion.get("message", "")

        # Pick colors based on the recommendation severity.

        if severity == "High":
            background_color = colors.lightpink
            text_color = colors.red

        elif severity == "Medium":
            background_color = colors.lightyellow
            text_color = colors.orange

        elif severity == "Low":
            background_color = colors.whitesmoke
            text_color = colors.darkblue

        elif severity == "Good":
            background_color = colors.lightgreen
            text_color = colors.green

        else:
            background_color = colors.whitesmoke
            text_color = colors.black

        # Format the recommendation title.

        title_style = ParagraphStyle(
            "SuggestionTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10,
            textColor=text_color,
            spaceAfter=4
        )

        # Format the recommendation message.

        message_style = ParagraphStyle(
            "SuggestionMessage",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.black
        )

        # Put the title and message together.

        suggestion_content = [Paragraph(f"{severity}: {title}",title_style),Paragraph(message,message_style)]

        # Use a small table to create the recommendation box.

        suggestion_table = Table([[suggestion_content]], colWidths=[430] )

        suggestion_table.setStyle(TableStyle([
                ( "BACKGROUND", (0, 0),(-1, -1),background_color ),
                
                ("BOX", (0, 0), (-1, -1), 0.8,text_color),
                
                ("LEFTPADDING", (0, 0), (-1, -1),10),
                
                ("RIGHTPADDING", (0, 0), (-1, -1),10),
                
                ("TOPPADDING",(0, 0),(-1, -1), 8),
                
                ("BOTTOMPADDING",(0, 0), (-1, -1),8),

                ("VALIGN", (0, 0),(-1, -1),"TOP" ) ]))

        elements.append(suggestion_table)
        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 12))