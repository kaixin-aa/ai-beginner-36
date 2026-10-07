import pandas as pd

frame = pd.DataFrame({"minutes": [20]})
print("列名", frame.columns.to_list())
print(frame["minutes"].to_list())
