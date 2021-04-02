import unittest

from ranked_list import RankedList
from cbf import CBFModel
from line_range import Range


class TestCBFModel(unittest.TestCase):

    def _mk_model(self) -> CBFModel:
        model = CBFModel()
        model.add('project_1', [0, 5])
        model.add('project_1', [0, 7])
        model.add('project_2', [3, 0])
        model.add('project_2', [2, 0])
        return model

    def test_creation(self):
        model = CBFModel()
        self.assertIsInstance(model, CBFModel)

    def test_add(self):
        model = CBFModel()
        model.add('project', [0, 5])
        self.assertIn('project', model.profiles_sources)
        self.assertIn([0, 5], model.profiles_sources['project'])

    def test_train(self):
        model = self._mk_model()
        model.train()
        self.assertTrue((model.profiles['project_1'] == [0, 6]).all())
        self.assertTrue((model.profiles['project_2'] == [2.5, 0]).all())

    def test_cos_dist(self):
        model = self._mk_model()
        model.train()
        self.assertEqual(model.cos_dist('project_1', [0, 1]), 0)
        self.assertEqual(model.cos_dist('project_2', [0, 1]), 1)
        self.assertEqual(model.cos_dist('project_1', [1, 0]), 1)
        self.assertEqual(model.cos_dist('project_2', [1, 0]), 0)

    def test_recommend_return_type(self):
        model = self._mk_model()
        model.train()
        recommendation = model.recommend([], 'project_1')
        self.assertIsInstance(recommendation, RankedList)

    def test_recommend_not_existing_profile(self):
        model = self._mk_model()
        model.train()
        recommendation = model.recommend([], 'not_exisiting_project')
        self.assertIsNone(recommendation)

    def test_recommend_order(self):
        model = self._mk_model()
        model.train()
        recommendation = model.recommend([], 'project_1')
        self.assertListEqual(recommendation._true_pos_idxs, [])

        recommendation = model.recommend(
            [
                ([0, 1], False, Range(0), Range(0)),
                ([1, 0], True, Range(0), Range(0))
            ],
            'project_1'
        )
        self.assertListEqual(recommendation._true_pos_idxs, [2])

        recommendation = model.recommend(
            [
                ([0, 1], True, Range(0), Range(0)),
                ([1, 0], False, Range(0), Range(0))
            ],
            'project_1'
        )
        self.assertListEqual(recommendation._true_pos_idxs, [1])
