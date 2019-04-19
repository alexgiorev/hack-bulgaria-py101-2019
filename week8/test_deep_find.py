import unittest
from deep_find import *

class TestDeepFind(unittest.TestCase):
    def setUp(self):
        self.l1 = [{'a': 10, 'b': 20}, {'c': 30, 'd': 40}]
        self.d11 = {'x': 50}
        self.d13 = {'a': -10, 'b': -20, 'c': -30, 'd': -40}
        self.d1 = {'d11': self.d11, 'd12': {'y': 60}, 'd13': self.d13}
        self.t1 = ({'A': 100, 'B': 200}, {'C': 300, 'D': 400})
        self.data = {'l1': self.l1, 'd1': self.d1, 't1': self.t1}
        self.data['d2'] = self.data # add a cycle
        
    def test_deep_find_dfs(self):
        self.assertTrue(deep_find_dfs(self.data, 'l1') is self.l1)
        self.assertTrue(deep_find_dfs(self.data, 'd1') is self.d1)
        self.assertTrue(deep_find_dfs(self.data, 'd11') is self.d11)
        self.assertTrue(deep_find_dfs(self.data, 'd13') is self.d13)
        self.assertTrue(deep_find_dfs(self.data, 't1') is self.t1)
        self.assertEqual(deep_find_dfs(self.data, 'x'), 50)
        self.assertEqual(deep_find_dfs(self.data, 'A'), 100)
        self.assertEqual(deep_find_dfs(self.data, 'B'), 200)
        self.assertEqual(deep_find_dfs(self.data, 'C'), 300)
        self.assertEqual(deep_find_dfs(self.data, 'D'), 400)
        self.assertRaises(KeyError, deep_find_dfs, self.data, 'z')

    def test_deep_find_all_dfs(self):
        self.assertEqual(set(deep_find_all_dfs(self.data, 'a')), {10, -10})
        self.assertEqual(set(deep_find_all_dfs(self.data, 'b')), {20, -20})
        self.assertEqual(set(deep_find_all_dfs(self.data, 'A')), {100})
        self.assertEqual(set(deep_find_all_dfs(self.data, 'Z')), set())

    def test_deep_find_bfs(self):
        # basically the same as for dfs
        self.assertTrue(deep_find_bfs(self.data, 'l1') is self.l1)
        self.assertTrue(deep_find_bfs(self.data, 'd1') is self.d1)
        self.assertTrue(deep_find_bfs(self.data, 'd11') is self.d11)
        self.assertTrue(deep_find_bfs(self.data, 'd13') is self.d13)
        self.assertTrue(deep_find_bfs(self.data, 't1') is self.t1)
        self.assertEqual(deep_find_bfs(self.data, 'x'), 50)
        self.assertEqual(deep_find_bfs(self.data, 'A'), 100)
        self.assertEqual(deep_find_bfs(self.data, 'B'), 200)
        self.assertEqual(deep_find_bfs(self.data, 'C'), 300)
        self.assertEqual(deep_find_bfs(self.data, 'D'), 400)
        self.assertRaises(KeyError, deep_find_bfs, self.data, 'z')

    def test_deep_find_all_bfs(self):
        # basically the same as for dfs
        self.assertEqual(set(deep_find_all_bfs(self.data, 'a')), {10, -10})
        self.assertEqual(set(deep_find_all_bfs(self.data, 'b')), {20, -20})
        self.assertEqual(set(deep_find_all_bfs(self.data, 'A')), {100})
        self.assertEqual(set(deep_find_all_bfs(self.data, 'Z')), set())

unittest.main()
