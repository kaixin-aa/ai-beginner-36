"""虚构教学成绩。每行一名学生，每列一门课程。"""
import json
from pathlib import Path
import numpy as np

STUDENTS = ["小林", "小周", "小陈", "小吴"]
SUBJECTS = ["Python", "数据处理", "AI 基础"]
SCORES = np.array([[80, 70, 90], [60, 85, 75], [95, 90, 85], [50, 60, 70]], dtype=np.float64)


def summarize(scores):
    scores = np.asarray(scores, dtype=np.float64)
    if scores.ndim != 2 or scores.shape[1] != 3:
        raise ValueError("成绩必须是二维数组，每行三门课程")
    if scores.shape[0] == 0:
        raise ValueError("成绩表至少需要一名学生")
    if not np.isfinite(scores).all():
        raise ValueError("成绩不能有缺失值或无穷值")
    if ((scores < 0) | (scores > 100)).any():
        raise ValueError("成绩必须处于 0 到 100")
    student_means = scores.mean(axis=1)
    loop_means = []
    for row in scores:
        loop_means.append(sum(row) / len(row))
    if not np.allclose(student_means, loop_means):
        raise AssertionError("批量计算与循环结果不一致")
    return {
        "shape": list(scores.shape),
        "student_means": student_means.tolist(),
        "subject_means": scores.mean(axis=0).tolist(),
        "overall_mean": float(scores.mean()),
        "passed_all": (scores >= 60).all(axis=1).tolist(),
        "adjusted_scores": np.minimum(scores + np.array([5, 0, 2]), 100).tolist(),
        "loop_means": list(map(float, loop_means)),
    }


def main():
    result = summarize(SCORES)
    print("形状", tuple(result["shape"]))
    print("学生均分", result["student_means"])
    print("课程均分", result["subject_means"])
    print("整体均分", result["overall_mean"])
    print("全部及格", result["passed_all"])
    print("批量与循环一致", np.allclose(result["student_means"], result["loop_means"]))
    target = Path(__file__).resolve().parents[1] / "results/score_summary.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
