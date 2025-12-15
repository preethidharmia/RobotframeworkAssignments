import os
import datetime
import pandas as pd
import pdfplumber
from docx import Document


def read_file(file_path, file_type):
    if file_type.lower() == 'pdf':
        with pdfplumber.open(file_path) as pdf:
            table = pdf.pages[0].extract_table()
            df = pd.DataFrame(table[1:], columns=table[0])
    elif file_type.lower() == 'docx' or file_type.lower() == 'word':
        doc = Document(file_path)
        table = doc.tables[0]
        data = []
        for row in table.rows:
            data.append([cell.text.strip() for cell in row.cells])
        df = pd.DataFrame(data[1:], columns=data[0])
    elif file_type.lower() in ['xlsx', 'xls', 'excel']:
        df = pd.read_excel(file_path)
    elif file_type.lower() in ['csv', 'txt', 'dat']:
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            try:
                df[col] = pd.to_numeric(df[col].str.replace(',', '') if df[col].dtype == 'object' else df[col], errors='ignore')
            except:
                pass
            try:
                df[col] = pd.to_datetime(df[col], errors='ignore')
            except:
                pass
            df[col] = df[col].apply(lambda x: True if str(x).lower() in ['true', 'yes'] else (
                False if str(x).lower() in ['false', 'no'] else x))

    df = df.replace({pd.NA: None, 'NULL': None, 'null': None})
    df = df.fillna('')
    return df

def compare_dataframes(df1, df2, log_file):
    with open(log_file, 'w') as log:
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        if cols1 != cols2:
            mismatch_cols = cols1.symmetric_difference(cols2)
            msg = f"Mismatched columns: {mismatch_cols}\n"
            print(msg)
            log.write(msg)
        else:
            msg = "All columns match.\n"
            print(msg)
            log.write(msg)

        common_cols = list(cols1.intersection(cols2))
        df1 = df1[common_cols]
        df2 = df2[common_cols]

        if df1.shape[0] != df2.shape[0]:
            msg = f"Row count mismatch: File1 has {df1.shape[0]} rows, File2 has {df2.shape[0]} rows\n"
            print(msg)
            log.write(msg)
        else:
            mismatches = []
            for i in range(df1.shape[0]):
                row1 = df1.iloc[i]
                row2 = df2.iloc[i]
                diff = row1 != row2
                if diff.any():
                    mismatch_details = {col: (row1[col], row2[col]) for col in common_cols if diff[col]}
                    mismatches.append(f"Row {i + 1} mismatch: {mismatch_details}\n")

            if mismatches:
                msg = "Data mismatches found:\n" + ''.join(mismatches)
                print(msg)
                log.write(msg)
            else:
                msg = "All data matches.\n"
                print(msg)
                log.write(msg)

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
    print(f"Log saved to: {log_file}")


if __name__ == "__main__":
    main()