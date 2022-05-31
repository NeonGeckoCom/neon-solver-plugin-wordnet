import unittest
from neon_solver_wordnet_plugin import WordnetSolver
from unittest.mock import Mock


class TestSolverBaseMethods(unittest.TestCase):
    def test_internal_cfg(self):
        solver = WordnetSolver()
        self.assertEqual(solver.default_lang, "en")

    def test_get_spoken_cache(self):
        solver = WordnetSolver()
        solver.spoken_cache.clear()
        solver.get_spoken_answer = Mock()
        solver.get_spoken_answer.return_value = "42"

        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_called()

        # now test that the cache is loaded and method not called again
        solver.get_spoken_answer = Mock()
        solver.get_spoken_answer.return_value = "42"
        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_not_called()

        # clear cache, method is called again
        solver.spoken_cache.clear()
        ans = solver.spoken_answer("some query")
        solver.get_spoken_answer.assert_called()

    def test_get_data_cache(self):
        solver = WordnetSolver()
        solver.cache.clear()
        solver.get_data = Mock()
        solver.get_data.return_value = {"dummy": "42"}

        ans = solver.search("some query")
        solver.get_data.assert_called()

        # now test that the cache is loaded and method not called again
        solver.get_data = Mock()
        solver.get_data.return_value = {"dummy": "42"}
        ans = solver.search("some query")
        solver.get_data.assert_not_called()

        # clear cache, method is called again
        solver.cache.clear()
        ans = solver.search("some query")
        solver.get_data.assert_called()

    def test_translation(self):
        solver = WordnetSolver()
        solver.translator.translate = Mock()
        solver.translator.translate.return_value = "a wild translation appears"

        # no translation
        ans = solver.spoken_answer("some query")
        solver.translator.translate.assert_not_called()

        # translation
        ans = solver.spoken_answer("not english", context={"lang": "unk"})
        solver.translator.translate.assert_called()
