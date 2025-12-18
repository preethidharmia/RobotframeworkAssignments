import os
import datetime
import pandas as pd
import pdfplumber
from docx import Document
import re


# ************************************************************ #
# Text normalization
# ************************************************************ #
def normalize_text(value, case_insensitive=True):
    if not isinstance(value, str):
        return value
    value = re.sub(r'\s+', ' ', value).strip()
    return value.lower() if case_insensitive else value


# ************************************************************ #
# NULL normalization
# ************************************************************ #
NULL_EQUIVALENTS = {'', 'null', 'none', 'na', 'n/a', '-'}

def normalize_null(value):
    if isinstance(value, str) and value.strip().lower() in NULL_EQUIVALENTS:
        return ''
    return value


# ************************************************************ #
# Numeric normalization
# ************************************************************ #
def normalize_number(value):
    try:
        return float(str(value).replace(',', ''))
    except Exception:
        return value


# ************************************************************ #
# Date normalization
# ************************************************************ #
def normalize_date(value):
    try:
        return pd.to_datetime(value, dayfirst=True).date()
    except Exception:
        return value


# ************************************************************ #
# Read file into DataFrame
# ************************************************************ #
def read_file(file_path, file_type):
    file_type = file_type.lower()

    if file_type == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            table = pdf.pages[0].extract_table()
            if not table:
                raise ValueError("No table found in PDF")
            df = pd.DataFrame(table[1:], columns=table[0])

    elif file_type in ['docx', 'word']:
        doc = Document(file_path)
        table = doc.tables[0]
        data = [[cell.text for cell in row.cells] for row in table.rows]
        df = pd.DataFrame(data[1:], columns=data[0])

    elif file_type in ['xlsx', 'xls', 'excel']:
        df = pd.read_excel(file_path)

    elif file_type in ['csv', 'txt']:
        df = pd.read_csv(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Normalize headers
    df.columns = [normalize_text(col) for col in df.columns]

    # Normalize cell values
    for col in df.columns:
        df[col] = df[col].apply(normalize_null)
        df[col] = df[col].apply(normalize_text)
        df[col] = df[col].apply(normalize_number)
        df[col] = df[col].apply(normalize_date)

    return df.fillna('')


# ************************************************************ #
# HTML Diff Visualization  (WITH FILE NAMES)
# ************************************************************ #
def generate_html_diff(mismatches, output_file, file1_name, file2_name, key_col):
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            .diff {{ background-color: #ffcccc; }}
            .key {{ background-color: #e6f2ff; font-weight: bold; }}
        </style>
    </head>
    <body>
    <h2>Data Comparison – Difference Report</h2>
    <p>
        <b>Key Column:</b> {key_col}<br>
        <b>File 1:</b> {file1_name}<br>
        <b>File 2:</b> {file2_name}
    </p>
    """

    for key, diff_data in mismatches.items():
        html += f"<h3>{key_col}: {key}</h3>"
        html += "<table>"
        html += f"<tr><th>Column</th><th>{file1_name}</th><th>{file2_name}</th></tr>"

        for col, (v1, v2) in diff_data.items():
            html += (
                f"<tr>"
                f"<td class='key'>{col}</td>"
                f"<td class='diff'>{v1}</td>"
                f"<td class='diff'>{v2}</td>"
                f"</tr>"
            )

        html += "</table>"

    html += "</body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


# ************************************************************ #
# Compare DataFrames (KEY-BASED)
# ************************************************************ #
def compare_dataframes(df1, df2, log_file, file1_name, file2_name, KEY_COL):
    html_mismatches = {}

    with open(log_file, 'w', encoding='utf-8') as log:

        # Column order check
        if list(df1.columns) != list(df2.columns):
            log.write("Column order mismatch detected\n")
            log.write(f"{file1_name} columns: {list(df1.columns)}\n")
            log.write(f"{file2_name} columns: {list(df2.columns)}\n\n")

        # Key column validation
        if KEY_COL not in df1.columns:
            log.write(f"Key column '{KEY_COL}' missing in {file1_name}\n")
            return

        if KEY_COL not in df2.columns:
            log.write(f"Key column '{KEY_COL}' missing in {file2_name}\n")
            return

        # -----------------------------------------------------
        # Key value validation (NULL / empty keys)
        # -----------------------------------------------------
        invalid_keys_f1 = df1[df1[KEY_COL].astype(str).str.strip() == '']
        invalid_keys_f2 = df2[df2[KEY_COL].astype(str).str.strip() == '']

        if not invalid_keys_f1.empty:
            log.write(
                f"WARNING: {len(invalid_keys_f1)} rows in {file1_name} have NULL/empty {KEY_COL}. "
                f"Key columns should not be null/empty.\n"
            )

        if not invalid_keys_f2.empty:
            log.write(
                f"WARNING: {len(invalid_keys_f2)} rows in {file2_name} have NULL/empty {KEY_COL}. "
                f"Key columns should not be null/empty.\n"
            )

        # Drop invalid key rows
        df1 = df1[df1[KEY_COL].astype(str).str.strip() != '']
        df2 = df2[df2[KEY_COL].astype(str).str.strip() != '']

        # Stop if no valid keys remain
        if df1.empty or df2.empty:
            log.write(
                f"ERROR: No valid {KEY_COL} values left after removing NULL/empty keys. "
                f"Comparison aborted.\n"
            )
            return

        # ************************************************************ #
        # Duplicate key detection
        # ************************************************************ #
        if df1[KEY_COL].duplicated().any():
            log.write(f"Duplicate keys found in {file1_name}\n")
            return

        if df2[KEY_COL].duplicated().any():
            log.write(f"Duplicate keys found in {file2_name}\n")
            return

        df1 = df1.set_index(KEY_COL)
        df2 = df2.set_index(KEY_COL)

        keys1, keys2 = set(df1.index), set(df2.index)

        for k in keys1 - keys2:
            log.write(f"{KEY_COL} {k} present in {file1_name} but missing in {file2_name}\n")

        for k in keys2 - keys1:
            log.write(f"{KEY_COL} {k} present in {file2_name} but missing in {file1_name}\n")

        common_keys = keys1 & keys2
        non_key_cols = [c for c in df1.columns if c in df2.columns]

        for key in common_keys:
            row1, row2 = df1.loc[key], df2.loc[key]
            diff = row1[non_key_cols] != row2[non_key_cols]

            if diff.any():
                html_mismatches[key] = {
                    col: (row1[col], row2[col])
                    for col in non_key_cols if diff[col]
                }
                log.write(f"Mismatch for {KEY_COL} {key}: {html_mismatches[key]}\n")

        if not html_mismatches:
            log.write("All records matched successfully.\n")

    if html_mismatches:
        html_file = log_file.replace(".log", "_diff.html")
        generate_html_diff(
            html_mismatches,
            html_file,
            file1_name,
            file2_name,
            KEY_COL
        )
        print(f"HTML diff generated: {html_file}")


# ************************************************************ #
# Main
# ************************************************************ #
def main():
    file1_path = input("Enter path to first file: ")
    file1_type = input("Enter type of first file: ")

    file2_path = input("Enter path to second file: ")
    file2_type = input("Enter type of second file: ")

    key_input = input("Enter key column name (e.g., Emp ID): ")
    KEY_COL = normalize_text(key_input)

    df1 = read_file(file1_path, file1_type)
    df2 = read_file(file2_path, file2_type)

    file1_name = os.path.basename(file1_path)
    file2_name = os.path.basename(file2_path)

    today = datetime.date.today().strftime("%d-%m-%Y")
    os.makedirs("logs", exist_ok=True)

    run = 1
    log_base = f"{file1_type}_{file2_type}_{file1_name}_{file2_name}_{today}_run"
    log_file = f"logs/{log_base}{run}.log"

    while os.path.exists(log_file):
        run += 1
        log_file = f"logs/{log_base}{run}.log"

    compare_dataframes(df1, df2, log_file, file1_name, file2_name, KEY_COL)
    print(f"Log saved to: {log_file}")


if __name__ == "__main__":
    main()
