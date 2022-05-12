import unittest
from db_management import init_db
from repositories.profile_repository import profile_repository


class TestProfileRepository(unittest.TestCase):
    def setUp(self):
        init_db()

    def test_list_all(self):
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        profile_repository.add("Charlie")
        profiles = profile_repository.list_all()
        self.assertEqual(len(profiles), 3)
        self.assertEqual(sorted([profile[1] for profile in profiles]), [
                         "Alice", "Bob", "Charlie"])

    def test_add(self):
        profile_repository.add("Alice")
        profile_repository.add("Alice")
        profiles = profile_repository.list_all()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0][1], "Alice")

    def test_remove(self):
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        profile_repository.remove(1)
        profiles = profile_repository.list_all()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0][1], "Bob")

    def test_exists(self):
        self.assertFalse(profile_repository.exists(1))
        self.assertFalse(profile_repository.exists(2))
        profile_repository.add("Alice")
        self.assertTrue(profile_repository.exists(1))
        self.assertFalse(profile_repository.exists(2))
        profile_repository.add("Bob")
        self.assertTrue(profile_repository.exists(1))
        self.assertTrue(profile_repository.exists(2))
