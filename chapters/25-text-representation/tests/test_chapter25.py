import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"examples"))
from text_core import *


class Chapter25Tests(unittest.TestCase):
    def test_01_cosine_geometry(self):
        self.assertAlmostEqual(cosine([1,2],[10,20]),1)
        self.assertEqual(cosine([1,0],[0,1]),0)
        self.assertEqual(cosine([1,0],[-1,0]),-1)
        self.assertAlmostEqual(cosine([1,0],[1,2]),1/np.sqrt(5))

    def test_02_invalid_cosine(self):
        for a,b in [([0,0],[1,1]),([1],[1,2]),([float('nan')],[1])]:
            with self.assertRaises(ValueError): cosine(a,b)

    def test_03_token_roundtrip_and_longest_match(self):
        data = load_data()
        for text in data["sentences"]:
            tokens = tokenize_words(text,data["vectors"])
            self.assertEqual("".join(tokens),text)
        self.assertEqual(tokenize_words("学习",data["vectors"]),["学习"])

    def test_04_lookup_and_arbitrary_ids(self):
        data = load_data()
        ids,matrix = vocabulary_and_matrix(data["vectors"])
        np.testing.assert_array_equal(matrix[ids["电脑"]],matrix[ids["计算机"]])
        vector,tokens,numbers = sentence_vector(data["sentences"][0],data["vectors"])
        np.testing.assert_allclose(vector,[.6,0,0,0])
        self.assertEqual(len(tokens),len(numbers))

    def test_05_character_counts(self):
        vocabulary,matrix = character_vectors(["猫猫桌","猫桌"])
        self.assertEqual(matrix[0,vocabulary.index("猫")],2)
        self.assertAlmostEqual(cosine(matrix[0],matrix[1]),3/np.sqrt(10))

    def test_06_negation_counterexample(self):
        data = load_data()
        a = sentence_vector(data["sentences"][6],data["vectors"])[0]
        b = sentence_vector(data["sentences"][7],data["vectors"])[0]
        self.assertEqual(cosine(a,b),1)

    def test_07_bpe_merges_with_independent_first_count(self):
        data = load_data()
        rules,splits,alphabet = train_bpe(data["bpe_word_counts"])
        self.assertEqual((rules[0]["left"],rules[0]["right"],rules[0]["count"]),("l","o",8))
        for word,parts in splits.items():
            self.assertEqual("".join(parts),word)
            self.assertEqual(tokenize_bpe(word,rules,alphabet),parts)
        self.assertEqual("".join(tokenize_bpe("newlow",rules,alphabet)),"newlow")

    def test_08_unknown_and_zero_mean(self):
        data = load_data()
        with self.assertRaises(ValueError): tokenize_words("量子",data["vectors"])
        with self.assertRaises(ValueError): tokenize_words("",data["vectors"])
        zeros = sentence_vector("我在上",data["vectors"])[0]
        with self.assertRaises(ValueError): cosine(zeros,zeros)


if __name__ == "__main__":
    unittest.main()
