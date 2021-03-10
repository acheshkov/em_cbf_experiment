import unittest
import tempfile
from line_range import Range
from source_code_utils import complement_range, complement_range_file
from source_code_utils import remove_comments, get_source_code


class TestSourceCodeUtils(unittest.TestCase):

    def test_get_source_code(self):
        with tempfile.NamedTemporaryFile(mode='w+') as temp_java_file:
            temp_java_file.write('public class A {')
            temp_java_file.write('\n')
            temp_java_file.write('}')
            temp_java_file.seek(0)
            sc = get_source_code(temp_java_file.name)
            self.assertNotEqual(sc, 'public class B {\n}')
            self.assertEqual(sc, 'public class A {\n}')

    def test_remove_comments(self):
        self.assertEqual(remove_comments('xxxx // comment'), 'xxxx ')
        self.assertEqual(remove_comments('xxxx /* comment */'), 'xxxx ')
        self.assertEqual(remove_comments('xxxx /* comment */ yyyy'), 'xxxx  yyyy')

    def test_complement_range(self):
        self.assertEqual(complement_range('1', Range(0, 0)), Range(0, 0))
        self.assertEqual(complement_range('1;', Range(0, 0)), Range(0, 0))
        self.assertEqual(complement_range('1{}', Range(0, 0)), Range(0, 0))
        self.assertEqual(complement_range('1{};', Range(0, 0)), Range(0, 0))
        self.assertEqual(complement_range('1{};\n2{};\n3{};\n4{};\n5{};', Range(1, 3)), Range(1, 3))
        self.assertEqual(complement_range('1{};\n2{};\n3{};\n4{};\n5{};', Range(0, 0)), Range(0, 0))
        self.assertEqual(complement_range('1{;}\n2{;}\n3{;\n4}\n5{;}', Range(0, 2)), Range(0, 3))
        self.assertEqual(complement_range('1{;}\n2{;}\n3{;\n4;\n5;}', Range(0, 4)), Range(0, 4))
        self.assertEqual(complement_range('1;\n2;\n3\n4;\n5', Range(0, 1)), Range(0, 1))
        self.assertEqual(complement_range('1;\n2\n3\n4;\n5', Range(0, 1)), Range(0, 3))

    def test_complement_range_file(self):
        with tempfile.NamedTemporaryFile(mode='w+') as temp_java_file:
            temp_java_file.write('for(int i=1; i<10; i++){')
            temp_java_file.write('\n')
            temp_java_file.write('int a = 1;')
            temp_java_file.write('\n')
            temp_java_file.write('}')

            temp_java_file.seek(0)
            self.assertEqual(
                complement_range_file(temp_java_file.name, 0, 0),
                Range(0, 2)
            )
            self.assertEqual(
                complement_range_file(temp_java_file.name, 0, 1),
                Range(0, 2)
            )
