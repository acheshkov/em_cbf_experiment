import unittest
import pandas as pd
import tempfile
from dataset import split_dataset, get_emos_vectors, combine_all_together
from dataset import SynthDataset, EmosVectorsDataset
from dataset import _drop_duplicates_by_filename, _drop_rows_with_undefined_true_range, _mk_full_path_to_java_files


class TestDataset(unittest.TestCase):

    def _mock_synth_dataset(self) -> SynthDataset:
        columns = [
            'output_filename',
            'insertion_start',
            'insertion_end',
            'class_name',
            'target_method',
            'target_method_start_line',
            'project_id',
            'filename',
            'true_inline_range'
        ]
        return pd.DataFrame(
            [
                ('/path/to/file_1.java', '40', '59', 'Foo', 'getItem', '34', 'apache/netbeans', 'file_1.java', '[40, 60]'),
                ('/path/to/file_2.java', '3', '6', 'Boo', 'subscribe', '2', 'apache/netbeans', 'file_2.java', '[3, 10]')
            ],
            columns=columns
        )

    def _mock_emos_vectors_dataset(self) -> EmosVectorsDataset:
        columns = ['emo_uid', 'filename_origin', 'range', 'vector_str']
        return pd.DataFrame(
            [
                ('/emo/uid/1', 'file_1.java', '[40, 60]', '-0.1 0.3 -0.9'),
                ('/emo/uid/2', 'file_1.java', '[40, 50]', '-0.2 0.3 -0.9'),
                ('/emo/uid/3', 'file_2.java', '[5, 7]', '-0.1 0.3 -0.8'),
                ('/emo/uid/4', 'file_2.java', '[4, 7]', '-0.1 0.2 -0.9'),
            ],
            columns=columns
        )

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

    def test_get_emos_vectors(self):
        with tempfile.NamedTemporaryFile(mode='w+') as temp_csv:
            temp_csv.write(','.join(['/path/to/p1_p2_p3_p4_p5_3_8.java', '-0.1 0.3 -0.9']))
            temp_csv.write(','.join(['/path/to/p1_p2_p3_p4_p5_3_8.java', '-0.1 0.3 -0.9']))
            temp_csv.write(','.join(['/path/to/p1_p2_p3_p4_p5_5_7.java', '-0.3 -0.3 0.2']))
            temp_csv.seek(0)
            emos_vectors = get_emos_vectors(temp_csv.name)
            self.assertIsInstance(emos_vectors, pd.DataFrame)
            self.assertIn('vector_str', emos_vectors.columns)
            self.assertEqual(len(emos_vectors), 1)
            self.assertEqual(emos_vectors.range[0], '[5, 7]')
            self.assertEqual(emos_vectors.filename_origin[0], 'p1_p2_p3_p4.java')
            self.assertEqual(emos_vectors.emo_uid[0], 'p1_p2_p3_p4_p5_5_7.java')

    def test_combine_all_together(self):
        emos_vectors: EmosVectorsDataset = self._mock_emos_vectors_dataset()
        synth: SynthDataset = self._mock_synth_dataset()
        dataset = combine_all_together(emos_vectors, synth)

        columns = [
            'filename', 'emo_uid', 'vector', 'project', 'is_true_emo', 'range_len',
            'target_method', 'target_method_start_line', 'range', 'true_range'
        ]
        for col_name in columns:
            self.assertIn(col_name, dataset.columns)
        self.assertIsInstance(dataset, pd.DataFrame)
        self.assertEqual(len(dataset), 4)
        self.assertEqual(len(dataset.query('filename == "/path/to/file_1.java" and is_true_emo == True')), 1)
        self.assertEqual(dataset.query('filename == "/path/to/file_1.java" and is_true_emo == True').true_range[0], '[40, 60]')
        self.assertEqual(len(dataset.query('filename == "/path/to/file_2.java" and is_true_emo == True')), 0)

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
