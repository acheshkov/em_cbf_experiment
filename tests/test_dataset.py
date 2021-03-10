import unittest
import pandas as pd
from dataset import split_dataset
from dataset import _drop_duplicates_by_filename, _drop_rows_with_undefined_true_range, _mk_full_path_to_java_files


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

    def test_drop_duplicates_by_filename(self):
        df = pd.DataFrame({'output_filename': ['fn_1', 'fn_2', 'fn_2', 'fn_3']})
        df = _drop_duplicates_by_filename(df)
        self.assertEqual(len(df), 2)
        self.assertEqual(set(df.output_filename.values), set(df.output_filename.unique()))

    def test_drop_rows_with_undefined_true_range(self):
        df = pd.DataFrame({'true_inline_range': [None, '[3, 4]']})
        df = _drop_rows_with_undefined_true_range(df)
        self.assertEqual(len(df), 1)
        self.assertIn('[3, 4]', df.true_inline_range.values)
        self.assertNotIn(None, df.true_inline_range.values)

    def test_mk_full_path_to_java_files(self):
        df = pd.DataFrame({'output_filename': ['fn_1', 'fn_2']})
        df = _mk_full_path_to_java_files(df, '/path/to/dir')
        self.assertEqual(len(df), 2)
        for fn in df.output_filename.values:
            self.assertIn('/path/to/dir', fn)
            self.assertNotIn('/path/to/other_dir', fn)
