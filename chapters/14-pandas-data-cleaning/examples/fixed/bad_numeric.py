import pandas as pd

source = pd.Series(["20", "二十"])
converted = pd.to_numeric(source, errors="coerce")
print(converted.to_list())
print("无法转换", source[converted.isna()].to_list())
