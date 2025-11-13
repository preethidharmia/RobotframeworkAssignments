# Simple Robot Framework library that reads a CSV with pandas

from robot.libraries.BuiltIn import BuiltIn
import pandas as pd

class PandasLibrary:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self._builtin = BuiltIn()

    #Keyword: Read CSV With Pandas

    def read_csv_with_pandas(self, csv_path):
        df = pd.read_csv(csv_path)
        records = df.to_dict(orient='records')
        self._builtin.log(f"Read {len(records)} rows from {csv_path}")
        return records

    #Keyword: Write Results To Excel
    # results_list = [{TestCaseNo:.., UserName:.., Password:.., Result:..}, ...]

    def write_results_to_excel(self, excel_path, results_list):
        if not results_list:
            self._builtin.log("No results to write to Excel.")
            return
        df = pd.DataFrame(results_list)     #DataFrame uses: DICT convert into table
        df = df[['TestCaseNo', 'UserName', 'Password', 'Result']]  #col addressing
        df.to_excel(excel_path, index=False)  #Index=False for restricting auto row numbering
        self._builtin.log(f"Excel written to: {excel_path}")