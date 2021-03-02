import unittest
import pandas as pd

from dataset import split_dataset, get_emos_ranges, get_emos_vectors, get_synth_dataset

class TestDataset(unittest.TestCase):


    def test_split_dataset(self):
        df = pd.DataFrame(
            [('A', i) for i in range(1, 101)] + [('B', i) for i in range(101, 105)],
            columns=['project', 'id']
        )
        train, test = split_dataset(df)

        self.assertEqual(len(df.query("project == 'A'")), 100)
        self.assertEqual(len(df.query("project == 'B'")), 4)
        self.assertEqual(len(test.query("project == 'A'")), 25)
        self.assertEqual(len(test.query("project == 'B'")), 1)
        

    def test_get_emos_ranges(self):
        pass

    def test_get_emos_vectors(self):
        pass

    def test_get_synth_dataset(self):
        pass

