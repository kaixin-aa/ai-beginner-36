import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

frame = pd.DataFrame({"minutes": [20, None, 15, 40], "done": [True, True, False, True]})
paired = frame.dropna(subset=["minutes", "done"])
fig, ax = plt.subplots()
ax.scatter(paired["minutes"], paired["done"].astype(int))
plt.close(fig)
print("配对时长", paired["minutes"].to_list())
print("配对状态", paired["done"].astype(int).to_list())
print("横纵坐标数量一致", len(paired["minutes"]) == len(paired["done"]))
