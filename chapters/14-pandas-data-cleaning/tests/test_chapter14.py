from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd

CHAPTER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHAPTER / "examples"))
from clean_records import FIELDS, clean_records


class CleaningTests(unittest.TestCase):
    def test_sample_audit(self):
        raw = pd.read_csv(CHAPTER / "data/raw_records.csv", dtype="string", keep_default_na=False)
        clean, duplicates, rejected, audit = clean_records(raw)
        self.assertEqual(audit, {"input_rows": 8, "duplicate_rows": 2, "rejected_rows": 1, "output_rows": 5, "raw_missing_minutes": 1, "invalid_minute_text_after_dedup": 1, "clean_missing_minutes": 2, "known_minutes_count": 3, "known_minutes_total": 75.0, "completed_rows": 3})
        self.assertEqual(clean["record_id"].to_list(), ["L01", "L02", "L03", "L04", "L05"])
        self.assertEqual(duplicates["source_row"].to_list(), [5, 9])
        self.assertEqual(rejected["source_row"].to_list(), [8])
        self.assertEqual(clean.loc[3, "minutes_status"], "invalid_text")

    def test_input_is_preserved(self):
        raw = pd.read_csv(CHAPTER / "data/raw_records.csv", dtype="string", keep_default_na=False)
        original = raw.copy(deep=True)
        clean_records(raw)
        pd.testing.assert_frame_equal(raw, original)

    def test_missing_column(self):
        with self.assertRaises(ValueError):
            clean_records(pd.DataFrame({"title": ["变量"]}))

    def test_empty_table(self):
        clean, duplicates, rejected, audit = clean_records(pd.DataFrame(columns=FIELDS))
        self.assertTrue(clean.empty and duplicates.empty and rejected.empty)
        self.assertEqual(audit["input_rows"], 0)

    def test_invalid_fields(self):
        for field, value in (("title", " "), ("done", "yes"), ("record_id", ""), ("minutes", "inf"), ("minutes", "1441")):
            item = {"record_id": "L01", "title": "变量", "done": "true", "minutes": "20", "tag": "Python"}
            item[field] = value
            with self.subTest(field=field, value=value):
                clean, _, rejected, _ = clean_records(pd.DataFrame([item]))
                self.assertTrue(clean.empty)
                self.assertEqual(len(rejected), 1)

    def test_conflicting_id_is_not_silently_dropped(self):
        first = {"record_id": "L01", "title": "变量", "done": "true", "minutes": "20", "tag": "Python"}
        second = dict(first, minutes="30")
        clean, duplicate, rejected, audit = clean_records(pd.DataFrame([first, second]))
        self.assertTrue(clean.empty and duplicate.empty)
        self.assertEqual(len(rejected), 2)
        self.assertTrue(rejected["reason"].str.contains("冲突").all())

    def test_excel_matches_csv(self):
        csv = pd.read_csv(CHAPTER / "data/raw_records.csv", dtype="string", keep_default_na=False)
        excel = pd.read_excel(CHAPTER / "data/raw_records.xlsx", dtype="string", keep_default_na=False, engine="openpyxl")
        pd.testing.assert_frame_equal(csv, excel)


if __name__ == "__main__":
    unittest.main()
