# from pathlib import Path
# import sys
# import pandas as pd
# from openpyxl.styles import Border, Side, Font, Alignment
# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter
# import zipfile
# import shutil
# import tempfile
# import xml.etree.ElementTree as ET
# # -----------------------------
# # Read paths from command line
# # -----------------------------
# input_dir = Path(sys.argv[1])
# output_dir = Path(sys.argv[2])
# all_timesheets_folder = output_dir / "All Timesheets"
# all_timesheets_folder.mkdir(parents=True, exist_ok=True)
# # Find uploaded Excel file
# excel_files = list(input_dir.glob("*.xlsx"))

# if not excel_files:
#     raise FileNotFoundError(f"No Excel file found in {input_dir}")

# input_file = excel_files[0]

# def repair_excel(input_file):
#     """
#     Repairs SAP generated xlsx files that contain invalid
#     empty <fill/> elements inside styles.xml.
#     Returns the repaired workbook path.
#     """

#     temp_dir = Path(tempfile.mkdtemp())

#     with zipfile.ZipFile(input_file, "r") as z:
#         z.extractall(temp_dir)

#     styles = temp_dir / "xl" / "styles.xml"

#     if styles.exists():

#         ns = {
#             "x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
#         }

#         tree = ET.parse(styles)
#         root = tree.getroot()

#         fills = root.find("x:fills", ns)

#         if fills is not None:

#             changed = False

#             for fill in fills.findall("x:fill", ns):

#                 if len(fill) == 0:

#                     pattern = ET.SubElement(
#                         fill,
#                         "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}patternFill"
#                     )

#                     pattern.set("patternType", "none")

#                     changed = True

#             if changed:
#                 tree.write(
#                     styles,
#                     encoding="utf-8",
#                     xml_declaration=True
#                 )

#     repaired = temp_dir / "repaired.xlsx"

#     with zipfile.ZipFile(
#         repaired,
#         "w",
#         zipfile.ZIP_DEFLATED
#     ) as new_zip:

#         for file in temp_dir.rglob("*"):

#             if file.is_file() and file != repaired:

#                 new_zip.write(
#                     file,
#                     file.relative_to(temp_dir)
#                 )

#     return repaired

# def format_name(email):
#     try:
#         local_part = email.split("@")[0]
#         first, last = local_part.split(".")
#         first = "".join(filter(str.isalpha, first))
#         last = "".join(filter(str.isalpha, last))
#         return f"{first.title()} {last.title()}"
#     except Exception:
#         return email


# # Read second sheet
# try:

#     df = pd.read_excel(
#         input_file,
#         sheet_name=1,
#         engine="openpyxl",
#         dtype=str
#     )

# except Exception as e:

#     # print("Repairing workbook...")

#     repaired = repair_excel(input_file)

#     df = pd.read_excel(
#         repaired,
#         sheet_name=1,
#         engine="openpyxl",
#         dtype=str
#     )

# # Select required columns
# # selected_columns = df.iloc[:, [8, 10, 13, 20]].copy()

# # selected_columns.columns = [
# #     "Name",
# #     "Timesheet Date",
# #     "Recorded Hours",
# #     "Note"
# # ]
# required_columns = [
#     "Name",
#     "Timesheet Date",
#     "Recorded Hours",
#     "Note",
#     "Project"
# ]

# # Create a mapping so column matching is case-insensitive
# column_map = {
#     str(column).strip().lower(): column
#     for column in df.columns
# }

# missing_columns = []

# for column in required_columns:
#     if column.lower() not in column_map:
#         missing_columns.append(column)

# if missing_columns:
#     print("This Excel file format is not supported.")
#     print(f"Missing columns: {', '.join(missing_columns)}")
#     sys.exit(1)

# # Get actual Excel column names
# name_column = column_map["name"]
# date_column = column_map["timesheet date"]
# hours_column = column_map["recorded hours"]
# note_column = column_map["note"]
# project_column = column_map["project"]

# # Select by column NAME, not position
# selected_columns = df[
#     [
#         name_column,
#         date_column,
#         hours_column,
#         note_column
#     ]
# ].copy()

# selected_columns.columns = [
#     "Name",
#     "Timesheet Date",
#     "Recorded Hours",
#     "Note"
# ]

# # Add Project
# selected_columns["Project"] = df[project_column].astype(str).str.strip()

# selected_columns["Name"] = (
#     selected_columns["Name"]
#     .apply(format_name)
#     .str.strip()
#     .str.title()
# )

# # Split by Name
# for name in selected_columns["Name"].unique():

#     filtered_df = selected_columns[
#         selected_columns["Name"] == name
#     ]

#     # safe_name = "".join(filter(str.isalpha, name))

#     # output_path = output_dir / f"{safe_name}.xlsx"
#     month_year=pd.to_datetime(
#         filtered_df["Timesheet Date"].iloc[0]
#     ).strftime("%B %Y")

#     safe_name="".join(c for c in name if c.isalnum() or c == " ").strip()
#     file_name=f"{month_year} Timesheet {safe_name}.xlsx"
#     output_path=output_dir/file_name
#     folder_output_path = all_timesheets_folder / file_name
#     for save_path in [output_path, folder_output_path]:

#         with pd.ExcelWriter(save_path, engine="openpyxl") as writer:

#             filtered_df.to_excel(
#                 writer,
#                 index=False,
#                 sheet_name="Sheet1"
#             )

#             worksheet = writer.sheets["Sheet1"]

#             thin_border = Border(
#                 left=Side(style="thin"),
#                 right=Side(style="thin"),
#                 top=Side(style="thin"),
#                 bottom=Side(style="thin")
#             )

#             for col_idx, column in enumerate(filtered_df.columns, 1):

#                 col_letter = get_column_letter(col_idx)

#                 max_length = max(
#                     filtered_df[column].astype(str).map(len).max(),
#                     len(column)
#                 ) + 2

#                 worksheet.column_dimensions[col_letter].width = max_length

#                 for row in range(2, len(filtered_df) + 2):
#                     worksheet[f"{col_letter}{row}"].border = thin_border

#             for col_idx in range(1, len(filtered_df.columns) + 1):
#                 worksheet[f"{get_column_letter(col_idx)}1"].border = thin_border
# # ============================================================
# # CREATE FGSS TIMESHEET XLSX
# #
# # Workbook contains:
# #   1. All Projects
# #   2. One separate sheet for every Project
# #
# # Project is picked directly from the "Project" column
# # of Timesheet Logs Master.
# # ============================================================


# # ------------------------------------------------------------
# # Get Project column from Timesheet Logs Master
# # ------------------------------------------------------------

# project_column = None

# for column in df.columns:

#     if str(column).strip().lower() == "project":
#         project_column = column
#         break

# if project_column is None:
#     raise ValueError(
#         "Project column was not found in Timesheet Logs Master."
#     )


# # ------------------------------------------------------------
# # Add Project to selected data
# # ------------------------------------------------------------

# selected_columns["Project"] = (
#     df.loc[
#         selected_columns.index,
#         project_column
#     ]
#     .astype(str)
#     .str.strip()
# )


# # ------------------------------------------------------------
# # Clean data
# # ------------------------------------------------------------

# selected_columns["Timesheet Date"] = pd.to_datetime(
#     selected_columns["Timesheet Date"],
#     errors="coerce"
# )

# selected_columns["Recorded Hours"] = pd.to_numeric(
#     selected_columns["Recorded Hours"],
#     errors="coerce"
# ).fillna(0)

# selected_columns = selected_columns[
#     selected_columns["Timesheet Date"].notna()
# ].copy()


# # Remove empty projects

# selected_columns = selected_columns[
#     selected_columns["Project"].notna() &
#     selected_columns["Project"].ne("") &
#     selected_columns["Project"].ne("nan")
# ].copy()


# # ------------------------------------------------------------
# # Determine month
# # ------------------------------------------------------------

# month_start = (
#     selected_columns["Timesheet Date"]
#     .min()
#     .replace(day=1)
# )

# month_end = (
#     month_start + pd.offsets.MonthEnd(1)
# )

# dates = pd.date_range(
#     start=month_start,
#     end=month_end,
#     freq="D"
# )

# month_year = month_start.strftime(
#     "%B %Y"
# )


# # ------------------------------------------------------------
# # Create workbook
# # ------------------------------------------------------------

# fgss_wb = Workbook()


# # Remove default sheet

# default_sheet = fgss_wb.active

# fgss_wb.remove(default_sheet)


# # ------------------------------------------------------------
# # Styles
# # ------------------------------------------------------------

# thin_side = Side(style="thin")

# thin_border = Border(
#     left=thin_side,
#     right=thin_side,
#     top=thin_side,
#     bottom=thin_side
# )

# bold_font = Font(
#     bold=True
# )

# center_alignment = Alignment(
#     horizontal="center",
#     vertical="center"
# )


# # ============================================================
# # FUNCTION TO CREATE A PROJECT TIMESHEET SHEET
# # ============================================================

# def create_project_sheet(
#     workbook,
#     sheet_name,
#     project_data
# ):

#     # --------------------------------------------------------
#     # Create sheet
#     # --------------------------------------------------------

#     ws = workbook.create_sheet(
#         title=sheet_name
#     )

#     # --------------------------------------------------------
#     # Month / Year
#     # --------------------------------------------------------

#     ws["B2"] = month_year

#     ws["B2"].font = bold_font
#     ws["B2"].alignment = center_alignment
#     ws["B2"].border = thin_border

#     # --------------------------------------------------------
#     # Headers
#     # --------------------------------------------------------

#     headers = [
#         "Project",
#         "Resource",
#         "Total Working Days",
#         "Leaves",
#         "Working Days After Leavs"
#     ]

#     for col, header in enumerate(headers, 1):

#         cell = ws.cell(
#             row=3,
#             column=col
#         )

#         cell.value = header
#         cell.font = bold_font
#         cell.border = thin_border
#         cell.alignment = center_alignment

#     # --------------------------------------------------------
#     # Day headers
#     # --------------------------------------------------------

#     for i, date in enumerate(dates):

#         col = 6 + i

#         cell = ws.cell(
#             row=3,
#             column=col
#         )

#         cell.value = date.strftime("%a")
#         cell.font = bold_font
#         cell.border = thin_border
#         cell.alignment = center_alignment

#     # --------------------------------------------------------
#     # Total column
#     # --------------------------------------------------------

#     total_col = 6 + len(dates)

#     cell = ws.cell(
#         row=3,
#         column=total_col
#     )

#     cell.value = "Total"
#     cell.font = bold_font
#     cell.border = thin_border
#     cell.alignment = center_alignment

#     # --------------------------------------------------------
#     # Create lookup
#     #
#     # IMPORTANT:
#     # Project + Name + Date
#     # --------------------------------------------------------

#     hours_lookup = (
#         project_data
#         .groupby(
#             [
#                 "Project",
#                 "Name",
#                 "Timesheet Date"
#             ],
#             as_index=False
#         )["Recorded Hours"]
#         .sum()
#     )

#     hours_dict = {}

#     for _, record in hours_lookup.iterrows():

#         key = (
#             record["Project"],
#             record["Name"],
#             record["Timesheet Date"].date()
#         )

#         hours_dict[key] = record["Recorded Hours"]

#     # --------------------------------------------------------
#     # IMPORTANT:
#     # Create unique Project + User combinations
#     #
#     # This fixes the All Projects problem.
#     # --------------------------------------------------------

#     user_projects = (
#         project_data[
#             ["Project", "Name"]
#         ]
#         .drop_duplicates()
#         .sort_values(
#             ["Project", "Name"]
#         )
#     )

#     # --------------------------------------------------------
#     # Create user rows
#     # --------------------------------------------------------

#     start_row = 4

#     for index, user_project in enumerate(
#         user_projects.itertuples(index=False),
#         start=0
#     ):

#         row = start_row + index

#         current_project = user_project.Project
#         user = user_project.Name

#         # ----------------------------------------------------
#         # Project
#         # ----------------------------------------------------

#         ws.cell(
#             row=row,
#             column=1
#         ).value = current_project

#         # ----------------------------------------------------
#         # Resource
#         # ----------------------------------------------------

#         ws.cell(
#             row=row,
#             column=2
#         ).value = user

#         # ----------------------------------------------------
#         # Total Working Days
#         # ----------------------------------------------------

#         working_days = sum(
#             1
#             for date in dates
#             if date.weekday() < 5
#         )

#         ws.cell(
#             row=row,
#             column=3
#         ).value = working_days

#         # ----------------------------------------------------
#         # Daily hours
#         # ----------------------------------------------------

#         leaves = 0

#         for i, date in enumerate(dates):

#             col = 6 + i

#             hours = hours_dict.get(
#                 (
#                     current_project,
#                     user,
#                     date.date()
#                 ),
#                 0
#             )

#             # Weekend
#             if date.weekday() >= 5:
#                 hours = 0

#             # Weekday without hours
#             elif hours == 0:
#                 leaves += 1

#             cell = ws.cell(
#                 row=row,
#                 column=col
#             )

#             cell.value = hours
#             cell.border = thin_border
#             cell.alignment = center_alignment

#         # ----------------------------------------------------
#         # Leaves
#         # ----------------------------------------------------

#         ws.cell(
#             row=row,
#             column=4
#         ).value = leaves

#         # ----------------------------------------------------
#         # Working Days After Leaves
#         # ----------------------------------------------------

#         ws.cell(
#             row=row,
#             column=5
#         ).value = working_days - leaves

#         # ----------------------------------------------------
#         # Total Hours
#         # ----------------------------------------------------

#         first_day_column = get_column_letter(6)

#         last_day_column = get_column_letter(
#             6 + len(dates) - 1
#         )

#         # ws.cell(
#         #     row=row,
#         #     column=total_col
#         # ).value = (
#         #     f"=SUM("
#         #     f"{first_day_column}{row}:"
#         #     f"{last_day_column}{row}"
#         #     f")"
#         # )
#         total_hours = sum(hours_dict.get(
#         (
#             current_project,
#             user,
#             date.date()
#         ),0) for date in dates )

#         ws.cell(
#             row=row,
#             column=total_col
#         ).value = total_hours

#     # --------------------------------------------------------
#     # Total row
#     # --------------------------------------------------------

#     last_user_row = (
#         start_row +
#         len(user_projects) -
#         1
#     )

#     total_row = last_user_row + 1

#     ws.merge_cells(
#         start_row=total_row,
#         start_column=1,
#         end_row=total_row,
#         end_column=2
#     )

#     ws.cell(
#         row=total_row,
#         column=1
#     ).value = "Total:"

#     ws.cell(
#         row=total_row,
#         column=1
#     ).font = bold_font

#     for col in range(
#         1,
#         total_col + 1
#     ):

#         cell = ws.cell(
#             row=total_row,
#             column=col
#         )

#         cell.border = thin_border
#         cell.alignment = center_alignment

#     for col in range(
#         3,
#         total_col + 1
#     ):

#         column_letter = get_column_letter(col)

#         # ws.cell(
#         #     row=total_row,
#         #     column=col
#         # ).value = (
#         #     f"=SUM("
#         #     f"{column_letter}{start_row}:"
#         #     f"{column_letter}{last_user_row}"
#         #     f")"
#         # )
#         for col in range(3, total_col + 1):

#             total_value = 0

#             for row in range(
#                 start_row,
#                 last_user_row + 1
#             ):

#                 value = ws.cell(
#                     row=row,
#                     column=col
#                 ).value

#                 if isinstance(value, (int, float)):
#                     total_value += value

#             ws.cell(
#                 row=total_row,
#                 column=col
#             ).value = total_value

#     # --------------------------------------------------------
#     # Total Hours
#     # --------------------------------------------------------

#     total_hours_row = total_row + 2

#     ws.cell(
#         row=total_hours_row,
#         column=2
#     ).value = "Total Hours"

#     ws.cell(
#         row=total_hours_row,
#         column=2
#     ).font = bold_font

#     ws.cell(
#         row=total_hours_row,
#         column=2
#     ).border = thin_border

#     total_column_letter = get_column_letter(
#         total_col
#     )

#     # ws.cell(
#     #     row=total_hours_row,
#     #     column=3
#     # ).value = (
#     #     f"={total_column_letter}{total_row}"
#     # )
#     total_hours = sum(
#         ws.cell(
#             row=row,
#             column=total_col
#         ).value or 0
#         for row in range(
#             start_row,
#             last_user_row + 1
#         )
#     )
#     ws.cell(
#         row=total_hours_row,
#         column=3
#     ).value = total_hours
    
#     ws.cell(
#         row=total_hours_row,
#         column=3
#     ).border = thin_border

#     ws.cell(
#         row=total_hours_row,
#         column=3
#     ).alignment = center_alignment
#     # --------------------------------------------------------
#     # Formatting
#     # --------------------------------------------------------

#     for row in ws.iter_rows(
#         min_row=3,
#         max_row=total_hours_row,
#         min_col=1,
#         max_col=total_col
#     ):

#         for cell in row:

#             cell.border = thin_border
#             cell.alignment = center_alignment

#     # --------------------------------------------------------
#     # Column widths
#     # --------------------------------------------------------

#     ws.column_dimensions["A"].width = 28
#     ws.column_dimensions["B"].width = 25
#     ws.column_dimensions["C"].width = 20
#     ws.column_dimensions["D"].width = 12
#     ws.column_dimensions["E"].width = 25

#     for col in range(
#         6,
#         total_col
#     ):

#         ws.column_dimensions[
#             get_column_letter(col)
#         ].width = 6

#     ws.column_dimensions[
#         get_column_letter(total_col)
#     ].width = 12

#     # --------------------------------------------------------
#     # Freeze panes
#     # --------------------------------------------------------

#     ws.freeze_panes = "F4"


# # ============================================================
# # 1. ALL PROJECTS SHEET
# # ============================================================

# create_project_sheet(
#     fgss_wb,
#     "All Projects",
#     selected_columns
# )


# # ============================================================
# # 2. SEPARATE SHEET FOR EACH PROJECT
# # ============================================================

# projects = sorted(
#     selected_columns[
#         "Project"
#     ]
#     .dropna()
#     .unique()
# )


# for project in projects:

#     project_data = selected_columns[
#         selected_columns[
#             "Project"
#         ] == project
#     ].copy()


#     # --------------------------------------------------------
#     # Excel sheet name restrictions
#     # --------------------------------------------------------

#     safe_sheet_name = str(project)

#     for character in [
#         "\\",
#         "/",
#         "*",
#         "?",
#         ":",
#         "[",
#         "]"
#     ]:

#         safe_sheet_name = (
#             safe_sheet_name
#             .replace(character, "_")
#         )


#     safe_sheet_name = safe_sheet_name[
#         :31
#     ]


#     # Avoid duplicate sheet names

#     if safe_sheet_name in fgss_wb.sheetnames:

#         counter = 2

#         original_name = safe_sheet_name

#         while safe_sheet_name in fgss_wb.sheetnames:

#             suffix = f"_{counter}"

#             safe_sheet_name = (
#                 original_name[
#                     :31 - len(suffix)
#                 ]
#                 + suffix
#             )

#             counter += 1


#     create_project_sheet(
#         fgss_wb,
#         safe_sheet_name,
#         project_data
#     )


# # ============================================================
# # SAVE FINAL FGSS XLSX
# # ============================================================

# fgss_file_name = (
#     f"{month_year} Timesheet.xlsx"
# )

# fgss_output_path = (
#     output_dir /
#     fgss_file_name
# )


# fgss_wb.save(
#     fgss_output_path
# )


# print()
# print("Created All Timesheet Zip")
# print("Created timesheet for particular candidates")
# print(f"Created {fgss_file_name}")
# print("Please download all the files or zip within 10 mins")

from pathlib import Path
import sys
import pandas as pd
from openpyxl.styles import Border, Side, Font, Alignment
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import zipfile
import shutil
import tempfile
import xml.etree.ElementTree as ET
# -----------------------------
# Read paths from command line
# -----------------------------
input_dir = Path(sys.argv[1])
output_dir = Path(sys.argv[2])
all_timesheets_folder = output_dir / "All Timesheets"
all_timesheets_folder.mkdir(parents=True, exist_ok=True)
# Find uploaded Excel file
excel_files = list(input_dir.glob("*.xlsx"))

if not excel_files:
    raise FileNotFoundError(f"No Excel file found in {input_dir}")

input_file = excel_files[0]

def repair_excel(input_file):
    """
    Repairs SAP generated xlsx files that contain invalid
    empty <fill/> elements inside styles.xml.
    Returns the repaired workbook path.
    """

    temp_dir = Path(tempfile.mkdtemp())

    with zipfile.ZipFile(input_file, "r") as z:
        z.extractall(temp_dir)

    styles = temp_dir / "xl" / "styles.xml"

    if styles.exists():

        ns = {
            "x": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        }

        tree = ET.parse(styles)
        root = tree.getroot()

        fills = root.find("x:fills", ns)

        if fills is not None:

            changed = False

            for fill in fills.findall("x:fill", ns):

                if len(fill) == 0:

                    pattern = ET.SubElement(
                        fill,
                        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}patternFill"
                    )

                    pattern.set("patternType", "none")

                    changed = True

            if changed:
                tree.write(
                    styles,
                    encoding="utf-8",
                    xml_declaration=True
                )

    repaired = temp_dir / "repaired.xlsx"

    with zipfile.ZipFile(
        repaired,
        "w",
        zipfile.ZIP_DEFLATED
    ) as new_zip:

        for file in temp_dir.rglob("*"):

            if file.is_file() and file != repaired:

                new_zip.write(
                    file,
                    file.relative_to(temp_dir)
                )

    return repaired

def format_name(email):
    try:
        local_part = email.split("@")[0]
        first, last = local_part.split(".")
        first = "".join(filter(str.isalpha, first))
        last = "".join(filter(str.isalpha, last))
        return f"{first.title()} {last.title()}"
    except Exception:
        return email


# Read second sheet
try:
    df = pd.read_excel(
        input_file,
        sheet_name=1,
        engine="openpyxl",
        dtype=str
    )

except Exception:
    try:
        repaired = repair_excel(input_file)

        df = pd.read_excel(
            repaired,
            sheet_name=1,
            engine="openpyxl",
            dtype=str
        )

    except Exception:
        print("This Excel file format is not supported.")
        sys.exit(1)


# ============================================================
# VALIDATE AND SELECT COLUMNS BY COLUMN NAME
# ============================================================

# Normalize headers only for matching.
# This makes matching case-insensitive and ignores leading/trailing spaces.
column_map = {
    str(column).strip().lower(): column
    for column in df.columns
}

# The SAP Timesheet Logs Master uses "Employee" for the employee email/name.
# It is renamed to "Name" internally so the rest of the script can remain unchanged.
required_columns = [
    "employee",
    "timesheet date",
    "recorded hours",
    "note",
    "project"
]

missing_columns = [
    column
    for column in required_columns
    if column not in column_map
]

if missing_columns:
    print("This Excel file format is not supported.")
    print(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )
    sys.exit(1)


# Get actual Excel column names from the header.
employee_column = column_map["employee"]
date_column = column_map["timesheet date"]
hours_column = column_map["recorded hours"]
note_column = column_map["note"]
project_column = column_map["project"]


# Select columns by NAME instead of column number.
selected_columns = df[
    [
        employee_column,
        date_column,
        hours_column,
        note_column,
        project_column
    ]
].copy()

# Use internal names expected by the rest of the script.
selected_columns.columns = [
    "Name",
    "Timesheet Date",
    "Recorded Hours",
    "Note",
    "Project"
]


# ============================================================
# CLEAN DATA
# ============================================================

selected_columns["Name"] = (
    selected_columns["Name"]
    .apply(format_name)
    .str.strip()
    .str.title()
)

# Convert dates safely.
selected_columns["Timesheet Date"] = pd.to_datetime(
    selected_columns["Timesheet Date"],
    errors="coerce"
)

# Convert hours safely.
selected_columns["Recorded Hours"] = pd.to_numeric(
    selected_columns["Recorded Hours"],
    errors="coerce"
).fillna(0)

# Clean Project.
selected_columns["Project"] = (
    selected_columns["Project"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# VALIDATE DATA
# ============================================================

# If there are no valid dates, the uploaded file is not in
# the expected timesheet format.
if selected_columns["Timesheet Date"].notna().sum() == 0:
    print("This Excel file format is not supported.")
    print("No valid Timesheet Date was found.")
    sys.exit(1)

# Remove rows where the date is invalid.
selected_columns = selected_columns[
    selected_columns["Timesheet Date"].notna()
].copy()

# Remove rows without a Project.
selected_columns = selected_columns[
    selected_columns["Project"].ne("") &
    selected_columns["Project"].ne("nan")
].copy()

# Remove rows without a Name.
selected_columns = selected_columns[
    selected_columns["Name"].notna() &
    selected_columns["Name"].ne("")
].copy()

if selected_columns.empty:
    print("This Excel file format is not supported.")
    print("No valid timesheet records were found.")
    sys.exit(1)


# ============================================================
# CREATE INDIVIDUAL TIMESHEETS BY NAME
# ============================================================

for name in selected_columns["Name"].unique():

    filtered_df = selected_columns[
        selected_columns["Name"] == name
    ].copy()

    if filtered_df.empty:
        continue

    month_year = filtered_df["Timesheet Date"].iloc[0].strftime(
        "%B %Y"
    )

    safe_name = "".join(
        c for c in name
        if c.isalnum() or c == " "
    ).strip()

    file_name = f"{month_year} Timesheet {safe_name}.xlsx"

    output_path = output_dir / file_name
    folder_output_path = all_timesheets_folder / file_name

    for save_path in [output_path, folder_output_path]:

        with pd.ExcelWriter(
            save_path,
            engine="openpyxl"
        ) as writer:

            filtered_df.to_excel(
                writer,
                index=False,
                sheet_name="Sheet1"
            )

            worksheet = writer.sheets["Sheet1"]

            thin_border = Border(
                left=Side(style="thin"),
                right=Side(style="thin"),
                top=Side(style="thin"),
                bottom=Side(style="thin")
            )

            for col_idx, column in enumerate(
                filtered_df.columns,
                1
            ):
                col_letter = get_column_letter(col_idx)

                max_length = max(
                    filtered_df[column]
                    .fillna("")
                    .astype(str)
                    .str.len()
                    .max(),
                    len(column)
                ) + 2

                worksheet.column_dimensions[
                    col_letter
                ].width = max_length

                for row in range(
                    2,
                    len(filtered_df) + 2
                ):
                    worksheet[
                        f"{col_letter}{row}"
                    ].border = thin_border

            for col_idx in range(
                1,
                len(filtered_df.columns) + 1
            ):
                worksheet[
                    f"{get_column_letter(col_idx)}1"
                ].border = thin_border


# ============================================================
# CREATE FGSS TIMESHEET XLSX
#
# Workbook contains:
#   1. All Projects
#   2. One separate sheet for every Project
#
# Project is picked directly from the "Project" column
# of Timesheet Logs Master.
# ============================================================


# ------------------------------------------------------------
# Clean data
# ------------------------------------------------------------

selected_columns["Timesheet Date"] = pd.to_datetime(
    selected_columns["Timesheet Date"],
    errors="coerce"
)

selected_columns["Recorded Hours"] = pd.to_numeric(
    selected_columns["Recorded Hours"],
    errors="coerce"
).fillna(0)

selected_columns = selected_columns[
    selected_columns["Timesheet Date"].notna()
].copy()


# Remove empty projects

selected_columns = selected_columns[
    selected_columns["Project"].notna() &
    selected_columns["Project"].ne("") &
    selected_columns["Project"].ne("nan")
].copy()


# ------------------------------------------------------------
# Determine month
# ------------------------------------------------------------

month_start = (
    selected_columns["Timesheet Date"]
    .min()
    .replace(day=1)
)

month_end = (
    month_start + pd.offsets.MonthEnd(1)
)

dates = pd.date_range(
    start=month_start,
    end=month_end,
    freq="D"
)

month_year = month_start.strftime(
    "%B %Y"
)


# ------------------------------------------------------------
# Create workbook
# ------------------------------------------------------------

fgss_wb = Workbook()


# Remove default sheet

default_sheet = fgss_wb.active

fgss_wb.remove(default_sheet)


# ------------------------------------------------------------
# Styles
# ------------------------------------------------------------

thin_side = Side(style="thin")

thin_border = Border(
    left=thin_side,
    right=thin_side,
    top=thin_side,
    bottom=thin_side
)

bold_font = Font(
    bold=True
)

center_alignment = Alignment(
    horizontal="center",
    vertical="center"
)


# ============================================================
# FUNCTION TO CREATE A PROJECT TIMESHEET SHEET
# ============================================================

def create_project_sheet(
    workbook,
    sheet_name,
    project_data
):

    # --------------------------------------------------------
    # Create sheet
    # --------------------------------------------------------

    ws = workbook.create_sheet(
        title=sheet_name
    )

    # --------------------------------------------------------
    # Month / Year
    # --------------------------------------------------------

    ws["B2"] = month_year

    ws["B2"].font = bold_font
    ws["B2"].alignment = center_alignment
    ws["B2"].border = thin_border

    # --------------------------------------------------------
    # Headers
    # --------------------------------------------------------

    headers = [
        "Project",
        "Resource",
        "Total Working Days",
        "Leaves",
        "Working Days After Leavs"
    ]

    for col, header in enumerate(headers, 1):

        cell = ws.cell(
            row=3,
            column=col
        )

        cell.value = header
        cell.font = bold_font
        cell.border = thin_border
        cell.alignment = center_alignment

    # --------------------------------------------------------
    # Day headers
    # --------------------------------------------------------

    for i, date in enumerate(dates):

        col = 6 + i

        cell = ws.cell(
            row=3,
            column=col
        )

        cell.value = date.strftime("%a")
        cell.font = bold_font
        cell.border = thin_border
        cell.alignment = center_alignment

    # --------------------------------------------------------
    # Total column
    # --------------------------------------------------------

    total_col = 6 + len(dates)

    cell = ws.cell(
        row=3,
        column=total_col
    )

    cell.value = "Total"
    cell.font = bold_font
    cell.border = thin_border
    cell.alignment = center_alignment

    # --------------------------------------------------------
    # Create lookup
    #
    # IMPORTANT:
    # Project + Name + Date
    # --------------------------------------------------------

    hours_lookup = (
        project_data
        .groupby(
            [
                "Project",
                "Name",
                "Timesheet Date"
            ],
            as_index=False
        )["Recorded Hours"]
        .sum()
    )

    hours_dict = {}

    for _, record in hours_lookup.iterrows():

        key = (
            record["Project"],
            record["Name"],
            record["Timesheet Date"].date()
        )

        hours_dict[key] = record["Recorded Hours"]

    # --------------------------------------------------------
    # IMPORTANT:
    # Create unique Project + User combinations
    #
    # This fixes the All Projects problem.
    # --------------------------------------------------------

    user_projects = (
        project_data[
            ["Project", "Name"]
        ]
        .drop_duplicates()
        .sort_values(
            ["Project", "Name"]
        )
    )

    # --------------------------------------------------------
    # Create user rows
    # --------------------------------------------------------

    start_row = 4

    for index, user_project in enumerate(
        user_projects.itertuples(index=False),
        start=0
    ):

        row = start_row + index

        current_project = user_project.Project
        user = user_project.Name

        # ----------------------------------------------------
        # Project
        # ----------------------------------------------------

        ws.cell(
            row=row,
            column=1
        ).value = current_project

        # ----------------------------------------------------
        # Resource
        # ----------------------------------------------------

        ws.cell(
            row=row,
            column=2
        ).value = user

        # ----------------------------------------------------
        # Total Working Days
        # ----------------------------------------------------

        working_days = sum(
            1
            for date in dates
            if date.weekday() < 5
        )

        ws.cell(
            row=row,
            column=3
        ).value = working_days

        # ----------------------------------------------------
        # Daily hours
        # ----------------------------------------------------

        leaves = 0

        for i, date in enumerate(dates):

            col = 6 + i

            hours = hours_dict.get(
                (
                    current_project,
                    user,
                    date.date()
                ),
                0
            )

            # Weekend
            if date.weekday() >= 5:
                hours = 0

            # Weekday without hours
            elif hours == 0:
                leaves += 1

            cell = ws.cell(
                row=row,
                column=col
            )

            cell.value = hours
            cell.border = thin_border
            cell.alignment = center_alignment

        # ----------------------------------------------------
        # Leaves
        # ----------------------------------------------------

        ws.cell(
            row=row,
            column=4
        ).value = leaves

        # ----------------------------------------------------
        # Working Days After Leaves
        # ----------------------------------------------------

        ws.cell(
            row=row,
            column=5
        ).value = working_days - leaves

        # ----------------------------------------------------
        # Total Hours
        # ----------------------------------------------------

        first_day_column = get_column_letter(6)

        last_day_column = get_column_letter(
            6 + len(dates) - 1
        )

        # ws.cell(
        #     row=row,
        #     column=total_col
        # ).value = (
        #     f"=SUM("
        #     f"{first_day_column}{row}:"
        #     f"{last_day_column}{row}"
        #     f")"
        # )
        total_hours = sum(hours_dict.get(
        (
            current_project,
            user,
            date.date()
        ),0) for date in dates )

        ws.cell(
            row=row,
            column=total_col
        ).value = total_hours

    # --------------------------------------------------------
    # Total row
    # --------------------------------------------------------

    last_user_row = (
        start_row +
        len(user_projects) -
        1
    )

    total_row = last_user_row + 1

    ws.merge_cells(
        start_row=total_row,
        start_column=1,
        end_row=total_row,
        end_column=2
    )

    ws.cell(
        row=total_row,
        column=1
    ).value = "Total:"

    ws.cell(
        row=total_row,
        column=1
    ).font = bold_font

    for col in range(
        1,
        total_col + 1
    ):

        cell = ws.cell(
            row=total_row,
            column=col
        )

        cell.border = thin_border
        cell.alignment = center_alignment

    for col in range(
        3,
        total_col + 1
    ):

        column_letter = get_column_letter(col)

        # ws.cell(
        #     row=total_row,
        #     column=col
        # ).value = (
        #     f"=SUM("
        #     f"{column_letter}{start_row}:"
        #     f"{column_letter}{last_user_row}"
        #     f")"
        # )
        for col in range(3, total_col + 1):

            total_value = 0

            for row in range(
                start_row,
                last_user_row + 1
            ):

                value = ws.cell(
                    row=row,
                    column=col
                ).value

                if isinstance(value, (int, float)):
                    total_value += value

            ws.cell(
                row=total_row,
                column=col
            ).value = total_value

    # --------------------------------------------------------
    # Total Hours
    # --------------------------------------------------------

    total_hours_row = total_row + 2

    ws.cell(
        row=total_hours_row,
        column=2
    ).value = "Total Hours"

    ws.cell(
        row=total_hours_row,
        column=2
    ).font = bold_font

    ws.cell(
        row=total_hours_row,
        column=2
    ).border = thin_border

    total_column_letter = get_column_letter(
        total_col
    )

    # ws.cell(
    #     row=total_hours_row,
    #     column=3
    # ).value = (
    #     f"={total_column_letter}{total_row}"
    # )
    total_hours = sum(
        ws.cell(
            row=row,
            column=total_col
        ).value or 0
        for row in range(
            start_row,
            last_user_row + 1
        )
    )
    ws.cell(
        row=total_hours_row,
        column=3
    ).value = total_hours
    
    ws.cell(
        row=total_hours_row,
        column=3
    ).border = thin_border

    ws.cell(
        row=total_hours_row,
        column=3
    ).alignment = center_alignment
    # --------------------------------------------------------
    # Formatting
    # --------------------------------------------------------

    for row in ws.iter_rows(
        min_row=3,
        max_row=total_hours_row,
        min_col=1,
        max_col=total_col
    ):

        for cell in row:

            cell.border = thin_border
            cell.alignment = center_alignment

    # --------------------------------------------------------
    # Column widths
    # --------------------------------------------------------

    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 12
    ws.column_dimensions["E"].width = 25

    for col in range(
        6,
        total_col
    ):

        ws.column_dimensions[
            get_column_letter(col)
        ].width = 6

    ws.column_dimensions[
        get_column_letter(total_col)
    ].width = 12

    # --------------------------------------------------------
    # Freeze panes
    # --------------------------------------------------------

    ws.freeze_panes = "F4"


# ============================================================
# 1. ALL PROJECTS SHEET
# ============================================================

create_project_sheet(
    fgss_wb,
    "All Projects",
    selected_columns
)


# ============================================================
# 2. SEPARATE SHEET FOR EACH PROJECT
# ============================================================

projects = sorted(
    selected_columns[
        "Project"
    ]
    .dropna()
    .unique()
)


for project in projects:

    project_data = selected_columns[
        selected_columns[
            "Project"
        ] == project
    ].copy()


    # --------------------------------------------------------
    # Excel sheet name restrictions
    # --------------------------------------------------------

    safe_sheet_name = str(project)

    for character in [
        "\\",
        "/",
        "*",
        "?",
        ":",
        "[",
        "]"
    ]:

        safe_sheet_name = (
            safe_sheet_name
            .replace(character, "_")
        )


    safe_sheet_name = safe_sheet_name[
        :31
    ]


    # Avoid duplicate sheet names

    if safe_sheet_name in fgss_wb.sheetnames:

        counter = 2

        original_name = safe_sheet_name

        while safe_sheet_name in fgss_wb.sheetnames:

            suffix = f"_{counter}"

            safe_sheet_name = (
                original_name[
                    :31 - len(suffix)
                ]
                + suffix
            )

            counter += 1


    create_project_sheet(
        fgss_wb,
        safe_sheet_name,
        project_data
    )


# ============================================================
# SAVE FINAL FGSS XLSX
# ============================================================

fgss_file_name = (
    f"{month_year} Timesheet.xlsx"
)

fgss_output_path = (
    output_dir /
    fgss_file_name
)


fgss_wb.save(
    fgss_output_path
)


print()
print("Created All Timesheet Zip")
print("Created timesheet for particular candidates")
print(f"Created {fgss_file_name}")
print("Please download all the files or zip within 10 mins")