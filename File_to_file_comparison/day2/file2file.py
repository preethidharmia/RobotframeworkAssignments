import os
import datetime
import pandas as pd
import pdfplumber
from docx import Document
import re


# ------------------------------------------------------------
# Normalize text from PDF / Word / Excel / CSV
# ------------------------------------------------------------
def normalize_text(value):
    if not isinstance(value, str):
        return value
    # Replace newlines, tabs, multiple spaces with single space
    value = re.sub(r'\s+', ' ', value)
    return value.strip()


# ------------------------------------------------------------
# Read input file into DataFrame
# ------------------------------------------------------------
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
        data = []
        for row in table.rows:
            data.append([cell.text for cell in row.cells])
        df = pd.DataFrame(data[1:], columns=data[0])

    elif file_type in ['xlsx', 'xls', 'excel']:
        df = pd.read_excel(file_path)

    elif file_type in ['csv', 'txt', 'dat']:
        df = pd.read_csv(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------
    df.columns = [normalize_text(col) for col in df.columns]

    # --------------------------------------------------------
    # Normalize cell values
    # --------------------------------------------------------
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(normalize_text)

    # Standard NULL handling
    df = df.replace({pd.NA: '', 'NULL': '', 'null': ''})
    df = df.fillna('')

    return df


# ------------------------------------------------------------
# Compare DataFrames and log results
# ------------------------------------------------------------
def compare_dataframes(df1, df2, log_file):
    with open(log_file, 'w', encoding='utf-8') as log:

        cols1 = set(df1.columns)
        cols2 = set(df2.columns)

        # ---------------- Column comparison ----------------
        if cols1 != cols2:
            mismatch_cols = cols1.symmetric_difference(cols2)
            msg = f"Mismatched columns: {mismatch_cols}\n"
            print(msg)
            log.write(msg)
        else:
            msg = "All columns match.\n"
            print(msg)
            log.write(msg)

        common_cols = sorted(list(cols1.intersection(cols2)))
        df1 = df1[common_cols]
        df2 = df2[common_cols]

        # ---------------- Row count comparison ----------------
        if df1.shape[0] != df2.shape[0]:
            msg = (
                f"Row count mismatch: "
                f"File1 has {df1.shape[0]} rows, "
                f"File2 has {df2.shape[0]} rows\n"
            )
            print(msg)
            log.write(msg)
            return

        # ---------------- Data comparison ----------------
        found_diff = False

        for i in range(df1.shape[0]):
            row1 = df1.iloc[i]
            row2 = df2.iloc[i]

            diff = row1 != row2

            if diff.any():
                found_diff = True
                mismatch_details = {
                    col: (row1[col], row2[col])
                    for col in common_cols if diff[col]
                }

                msg = f"Row {i + 1} mismatch: {mismatch_details}\n"
                print(msg)
                log.write(msg)

        if not found_diff:
            msg = "All data matches.\n"
            print(msg)
            log.write(msg)


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    file1_path = input("Enter path to first file: ")
    file1_type = input("Enter type of first file (pdf, docx, excel, csv, txt, dat): ")

    file2_path = input("Enter path to second file: ")
    file2_type = input("Enter type of second file (pdf, docx, excel, csv, txt, dat): ")

    df1 = read_file(file1_path, file1_type)
    df2 = read_file(file2_path, file2_type)

    file1_name = os.path.splitext(os.path.basename(file1_path))[0]
    file2_name = os.path.splitext(os.path.basename(file2_path))[0]
    today = datetime.date.today().strftime("%d-%m-%Y")

    run_num = 1
    log_base = f"{file1_type}_{file2_type}_{file1_name}_{file2_name}_{today}_run"
    log_file = f"{log_base}{run_num}.log"

    while os.path.exists(log_file):
        run_num += 1
        log_file = f"{log_base}{run_num}.log"

    compare_dataframes(df1, df2, log_file)

    print(f"\nLog saved to: {log_file}")


# ------------------------------------------------------------
if __name__ == "__main__":
    main()
