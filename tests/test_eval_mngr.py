import unittest
import pandas as pd
from ranked_list import RankedList
from eval_mngr import EvalMngr


class TestEvalMngr(unittest.TestCase):
    def test_jaccard_1(self):
        mgr = EvalMngr()
        rl_jaccard = RankedList(pd.DataFrame(
            [(1, True, '[4, 6]', '[4, 6]'), (2, False, '[5, 7]', '[4, 6]')],
            columns=['score', 'is_true', 'range', 'true_range']
        ))
        self.assertEqual(mgr.jaccard([rl_jaccard]), 1)

    def test_jaccard_2(self):
        mgr = EvalMngr()
        rl_jaccard = RankedList(pd.DataFrame(
            [(1, True, '[3, 5]', '[4, 6]'), (2, False, '[5, 7]', '[4, 6]')],
            columns=['score', 'is_true', 'range', 'true_range']
        ))
        self.assertEqual(mgr.jaccard([rl_jaccard]), 0.5)

    def test_jaccard_3(self):
        mgr = EvalMngr()
        rl_jaccard = RankedList(pd.DataFrame(
            [(1, True, '[2, 4]', '[4, 6]'), (2, False, '[5, 7]', '[4, 6]')],
            columns=['score', 'is_true', 'range', 'true_range']
        ))
        self.assertEqual(mgr.jaccard([rl_jaccard]), 1 / 5)
