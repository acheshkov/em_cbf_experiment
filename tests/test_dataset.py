import unittest
import tempfile
import pandas as pd
from dataset import split_dataset, get_synth_dataset


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
        path_to_java_files = '/tmp/some_folder'
        columns = [
            'output_filename',
            'insertion_start',
            'insertion_end',
            'class_name',
            'target_method',
            'project_id',
            'target_method_start_line'
        ]
        with tempfile.NamedTemporaryFile(mode='w+') as temp_csv:
            temp_csv.write(','.join(columns) + '\n')
            temp_csv.write('fn_1,2,10,class,method,project,2\n')
            temp_csv.write('fn_1,2,10,class,method,project,2\n')
            temp_csv.write('fn_2,2,10,class,method,project,2\n')
            temp_csv.seek(0)
            synth = get_synth_dataset(temp_csv.name, path_to_java_files)
            print(synth[['filename', 'true_inline_range']].values)
            self.assertEqual(len(synth), 1)  # we remove duplicates by 'output_filename' column
