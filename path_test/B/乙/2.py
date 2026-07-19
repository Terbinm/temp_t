import os

file_path = os.path.abspath(__file__)
cwd = os.getcwd()
print(f"[檔案路徑] {file_path}  |  [執行路徑 CWD] {cwd}")
