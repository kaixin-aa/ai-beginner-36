import numpy as np

scores = np.array([80, 50])
print("每项及格", (scores >= 60).tolist())
print("至少一项及格", (scores >= 60).any())
print("全部及格", (scores >= 60).all())
