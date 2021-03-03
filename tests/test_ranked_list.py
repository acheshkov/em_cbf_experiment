import unittest

from ranked_list import RankedList


class TestRankedList(unittest.TestCase):

    def mk_rlist_data(self, length: int, true_pos: int):
        ''' Make list of specific length  and True value at specific position'''
        return [(i + 1, True if i+1 == true_pos else False) for i in range(length)]

    def test_from_list(self):
        rl = RankedList.from_list([(1, True), (2, False)])
        self.assertEqual(rl.true_positions, [1])

    def test_empty_list(self):
        rl = RankedList.from_list([])
        self.assertEqual(rl.true_positions, [])
