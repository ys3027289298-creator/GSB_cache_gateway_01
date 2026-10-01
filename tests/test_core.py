import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_overwrite_updates_value(self):
        state = core.new_game()
        self.assertTrue(core.put(state, "a", 1))
        self.assertTrue(core.put(state, "a", 2))
        self.assertEqual(core.get(state, "a"), 2)

    def test_02_negative_ttl_rejected(self):
        state = core.new_game()
        self.assertFalse(core.put(state, "a", 1, -1))

    def test_03_expired_miss(self):
        state = core.new_game()
        core.put(state, "a", 1, 0)
        self.assertIsNone(core.get(state, "a"))

    def test_04_delete_removes(self):
        state = core.new_game()
        core.put(state, "a", 1)
        core.delete(state, "a")
        self.assertFalse(core.has(state, "a"))

    def test_05_size_count(self):
        state = core.new_game()
        core.put(state, "a", 1)
        self.assertEqual(core.size(state), 1)

    def test_06_evicts_oldest(self):
        state = core.new_game()
        core.put(state, "a", 1)
        core.put(state, "b", 2)
        core.put(state, "c", 3)
        self.assertNotIn("a", state["cache"])
        self.assertIn("b", state["cache"])
        self.assertIn("c", state["cache"])

    def test_07_clear_order(self):
        state = core.new_game()
        core.put(state, "a", 1)
        core.clear(state)
        self.assertEqual(state["order"], [])

    def test_08_ttl_remaining(self):
        state = core.new_game()
        core.put(state, "a", 1, 100)
        self.assertLess(core.ttl(state, "a"), 10000)

    def test_09_missing_not_present(self):
        state = core.new_game()
        self.assertFalse(core.has(state, "missing"))

    def test_10_load_preserves_id(self):
        state = core.new_game()
        state["next_id"] = 5
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["next_id"], 5)


if __name__ == "__main__":
    unittest.main()
