import unittest
from db_management import init_db
from entities.trip import Trip
from repositories.trip_repository import trip_repository
from repositories.profile_repository import profile_repository


class TestTripRepository(unittest.TestCase):
    def setUp(self):
        init_db()
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        trip_repository.add(1, "Test1_1", "2022-03-01 02:00",
                            "2022-03-02 15:28", 82800)
        trip_repository.add(1, "Test1_2", "2022-01-01 12:00",
                            "2022-01-01 15:28", 12800)

    def test_find_by_profile(self):
        trips_1 = trip_repository.find_by_profile(1)
        trips_2 = trip_repository.find_by_profile(2)
        self.assertEqual(len(trips_1), 2)
        self.assertEqual(len(trips_2), 0)
        self.assertEqual([trip.name for trip in trips_1],
                         ["Test1_2", "Test1_1"])
        trip_1 = trips_1[0]
        self.assertEqual(trip_1.name, "Test1_2")
        self.assertEqual(trip_1.duration, 12480)
        self.assertEqual(trip_1.length, 12800)
        self.assertEqual(trip_1.speed, 12800/12480)

    def test_add(self):
        trips_1 = trip_repository.find_by_profile(1)
        self.assertEqual(len(trips_1), 2)

        trip_repository.add(1, "Test1_3", "2021-03-01 02:00",
                            "2021-03-02 15:28", 82800)
        trip_repository.add(1, "Test1_4", "2021-04-01 02:00",
                            "2021-03-02 15:28", 82800)
        trip_repository.add(1, "Test1_5", "2021-04-01 02:00",
                            "2022-03-02 15:28", -1)
        trip_repository.add(2, "Test2_1", "2022-01-01 12:00",
                            "2022-01-01 12:00", 12800)

        trips_1 = trip_repository.find_by_profile(1)
        trips_2 = trip_repository.find_by_profile(2)
        self.assertEqual(len(trips_1), 3)
        self.assertEqual(len(trips_2), 1)

        trip_1 = trips_1[0]
        self.assertEqual(trip_1.name, "Test1_3")
        self.assertEqual(trip_1.duration, 134880)
        self.assertEqual(trip_1.length, 82800)
        self.assertEqual(trip_1.speed, 82800/134880)

        self.assertEqual(trips_2[0].speed, 0)

    def test_remove(self):
        trips_1 = trip_repository.find_by_profile(1)
        self.assertEqual(len(trips_1), 2)

        trip_repository.remove(1)

        trips_1 = trip_repository.find_by_profile(1)
        self.assertEqual(len(trips_1), 1)
        trip_1 = trips_1[0]
        self.assertEqual(trip_1.name, "Test1_2")

    def test_remove_by_profile(self):
        trip_repository.add(2, "Test2_1", "2022-01-01 12:00",
                            "2022-01-01 12:00", 12800)

        trips_1 = trip_repository.find_by_profile(1)
        trips_2 = trip_repository.find_by_profile(2)
        self.assertEqual(len(trips_1), 2)
        self.assertEqual(len(trips_2), 1)

        trip_repository.remove_by_profile(1)

        trips_1 = trip_repository.find_by_profile(1)
        trips_2 = trip_repository.find_by_profile(2)
        self.assertEqual(len(trips_1), 0)
        self.assertEqual(len(trips_2), 1)
