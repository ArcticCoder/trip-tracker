import unittest
from db_connection import get_db_connection
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
        self.assertEqual(sorted([profile[1] for profile in profiles]), ["Alice", "Bob", "Charlie"])

    def test_find_name(self):
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        self.assertEqual(profile_repository.find_name(1), "Alice")
        self.assertEqual(profile_repository.find_name(2), "Bob")
        self.assertIsNone(profile_repository.find_name(3))

    def test_find_id(self):
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        self.assertEqual(profile_repository.find_id("Alice"), 1)
        self.assertEqual(profile_repository.find_id("Bob"), 2)
        self.assertIsNone(profile_repository.find_id("Charlie"))

    def test_add(self):
        profile_repository.add("Alice")
        profile_repository.add("Alice")
        profiles = profile_repository.list_all()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0][1], "Alice")

    def test_remove(self):
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        profile_repository.remove("Alice")
        profiles = profile_repository.list_all()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0][1], "Bob")
