import unittest
from db_management import init_db
from entities.trip import Trip
from repositories.trip_repository import trip_repository
from repositories.profile_repository import profile_repository
from services.trip_tracker_service import trip_tracker_service


class TestTripTrackerService(unittest.TestCase):
    def setUp(self):
        init_db()
        profile_repository.add("Alice")
        profile_repository.add("Bob")
        trip_repository.add(1, "Test1_1", "2022-03-01 02:00:00",
                            "2022-03-02 15:28:00", 82800)
        trip_repository.add(1, "Test1_2", "2022-01-01 12:00:00",
                            "2022-01-01 15:28:00", 12800)
        trip_tracker_service.select_profile(-1)

    def test_get_profiles(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(sorted([profile[1]
                         for profile in profiles]), ["Alice", "Bob"])

    def test_add_profile(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(sorted([profile[1]
                         for profile in profiles]), ["Alice", "Bob"])

        trip_tracker_service.add_profile("Charlie")
        trip_tracker_service.add_profile("Bob")

        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 3)
        self.assertEqual(sorted([profile[1] for profile in profiles]), [
            "Alice", "Bob", "Charlie"])

    def test_remove_profile(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(sorted([profile[1]
                         for profile in profiles]), ["Alice", "Bob"])

        trip_tracker_service.remove_profile(1)

        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(sorted([profile[1] for profile in profiles]), ["Bob"])

    def test_get_trips(self):
        trip_tracker_service.select_profile(1)
        trips = trip_tracker_service.get_trips()

        self.assertEqual(len(trips), 2)
        self.assertEqual([trip.name for trip in trips],
                         ["Test1_2", "Test1_1"])
        trip_1 = trips[0]
        self.assertEqual(trip_1.name, "Test1_2")
        self.assertEqual(trip_1.duration, 12480)
        self.assertEqual(trip_1.length, 12800)
        self.assertEqual(trip_1.speed, 12800/12480)

        trip_tracker_service.select_time_range("2022-01-02")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 1)
        trip_1 = trips[0]
        self.assertEqual(trip_1.name, "Test1_1")
        self.assertEqual(trip_1.duration, 134880)
        self.assertEqual(trip_1.length, 82800)
        self.assertEqual(trip_1.speed, 82800/134880)

        trip_tracker_service.select_time_range(None, "2022-01-03")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 1)
        trip_1 = trips[0]
        self.assertEqual(trip_1.name, "Test1_2")
        self.assertEqual(trip_1.duration, 12480)
        self.assertEqual(trip_1.length, 12800)
        self.assertEqual(trip_1.speed, 12800/12480)

        trip_tracker_service.select_time_range("2022-01-02", "2022-01-03")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 0)

        trip_tracker_service.select_time_range()
        trip_tracker_service.select_time_range("1", "1")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 2)

        trip_tracker_service.select_profile(2)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 0)

        trip_tracker_service.select_profile(1)
        trip_tracker_service.select_profile(3)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 2)

    def test_get_statistics(self):
        trip_tracker_service.select_profile(1)
        avg_speed, avg_duration, avg_length, speeds, durations, lengths, dates = trip_tracker_service.get_statistics()

        self.assertAlmostEqual(avg_speed, 0.82, 2)
        self.assertEqual(avg_duration, 73680)
        self.assertEqual(avg_length, 47800)

        speeds_test = [1.03, 0.61]
        durations_test = [12480, 134880]
        lengths_test = [12800, 82800]
        dates_test = ["2022-01-01 12:00:00", "2022-03-01 02:00:00"]

        for i in range(len(speeds)):
            self.assertAlmostEqual(speeds[i], speeds_test[i], 2)
            self.assertEqual(durations[i], durations_test[i])
            self.assertEqual(lengths[i], lengths_test[i])
            self.assertEqual(dates[i], dates_test[i])

        trip_tracker_service.select_profile(2)
        avg_speed, avg_duration, avg_length, speeds, durations, lengths, dates = trip_tracker_service.get_statistics()

        self.assertAlmostEqual(avg_speed, 0.00, 2)
        self.assertEqual(avg_duration, 0)
        self.assertEqual(avg_length, 0)
        self.assertEqual(speeds, [])
        self.assertEqual(durations, [])
        self.assertEqual(lengths, [])
        self.assertEqual(dates, [])

    def test_add_trip(self):
        trip_tracker_service.select_profile(1)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 2)

        trip_tracker_service.add_trip("Test1_3", "2021-03-01 02:00",
                                      "2021-03-02 15:28", 82800)

        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 3)
        trip_tracker_service.add_trip("Test1_3", "1", "1", 82800)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 3)

        trip_1 = trips[0]
        self.assertEqual(trip_1.name, "Test1_3")
        self.assertEqual(trip_1.duration, 134880)
        self.assertEqual(trip_1.length, 82800)
        self.assertEqual(trip_1.speed, 82800/134880)

    def test_remove_trip(self):
        trip_tracker_service.select_profile(1)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 2)

        trip_tracker_service.remove_trip(1)

        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 1)
        trip_1 = trips[0]
        self.assertEqual(trip_1.name, "Test1_2")

    def test_seconds_to_string(self):
        self.assertEqual(trip_tracker_service.seconds_to_string(0), "00:00:00")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(20), "00:00:20")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(60), "00:01:00")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(3671), "01:01:11")
        self.assertEqual(
            trip_tracker_service.seconds_to_string(216069), "60:01:09")

    def test_valid_date_time(self):
        self.assertTrue(trip_tracker_service.valid_date_time("2022"))
        self.assertTrue(trip_tracker_service.valid_date_time("2022-01"))
        self.assertTrue(trip_tracker_service.valid_date_time("2022-01-03"))
        self.assertTrue(trip_tracker_service.valid_date_time("2022-01-03 12"))
        self.assertTrue(
            trip_tracker_service.valid_date_time("2022-01-03 12:00"))
        self.assertTrue(trip_tracker_service.valid_date_time(
            "2022-01-03 12:00:50"))

        self.assertFalse(trip_tracker_service.valid_date_time("22"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022:03"))
        self.assertFalse(
            trip_tracker_service.valid_date_time("2022:01:03 02:00"))
        self.assertFalse(
            trip_tracker_service.valid_date_time("22-01-03 02:00"))
        self.assertFalse(
            trip_tracker_service.valid_date_time("2022-01-03 2:00"))
        self.assertFalse(
            trip_tracker_service.valid_date_time("2022-1-03 12:00:50"))
        self.assertFalse(
            trip_tracker_service.valid_date_time("2022-01-3 12:00:50"))
        self.assertFalse(
            trip_tracker_service.valid_date_time("2022-01-03 a2:00"))
        self.assertFalse(trip_tracker_service.valid_date_time("0000-01-03"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022-00-03"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022-01-00"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022-13-00"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022-01-32"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022-02-30"))
        self.assertFalse(trip_tracker_service.valid_date_time("2022-02-30 25"))

    def test_valid_time(self):
        self.assertTrue(trip_tracker_service.valid_time("2022-01-03 12:00"))
        self.assertTrue(trip_tracker_service.valid_time("2022-01-03 12:00:50"))

        self.assertFalse(trip_tracker_service.valid_time("2022:01:03 02:00"))
        self.assertFalse(trip_tracker_service.valid_time("22-01-03 02:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-03 2:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-1-03 12:00:50"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-3 12:00:50"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-03 12"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-03 a2:00"))
        self.assertFalse(trip_tracker_service.valid_time("0000-01-03 12:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-00-03 12:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-00 12:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-13-00 12:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-32 12:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-01 25:00"))
        self.assertFalse(trip_tracker_service.valid_time("2022-01-01 00:60"))
        self.assertFalse(
            trip_tracker_service.valid_time("2022-01-01 00:00:60"))

    def test_adjust_end_time(self):
        self.assertEqual(trip_tracker_service.adjust_end_time("A"), "")
        self.assertEqual(trip_tracker_service.adjust_end_time(
            "2022"), "2022-99-99 99:99:99")
        self.assertEqual(trip_tracker_service.adjust_end_time(
            "2022-01"), "2022-01-99 99:99:99")
        self.assertEqual(trip_tracker_service.adjust_end_time(
            "2022-01-02"), "2022-01-02 99:99:99")
        self.assertEqual(trip_tracker_service.adjust_end_time(
            "2022-01-02 03"), "2022-01-02 03:99:99")
        self.assertEqual(trip_tracker_service.adjust_end_time(
            "2022-01-02 03:04"), "2022-01-02 03:04:99")
        self.assertEqual(trip_tracker_service.adjust_end_time(
            "2022-01-02 03:04:05"), "2022-01-02 03:04:05")

    # Test that combines most of the functionality of the entire program
    def test_simulated_path(self):
        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(profiles[0][1], "Alice")

        trip_tracker_service.select_profile(profiles[0][0])
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 2)
        trip_tracker_service.add_trip(
            "Test1_3", "2022-01-01 08:00", "2022-01-01 09:00", 10000)
        trip_tracker_service.add_trip(
            "Test1_4", "2022-0X-01 08:00", "2022-01-01 09:00", 10000)

        trip_tracker_service.select_profile(-1)
        trip_tracker_service.add_profile("Alice")
        trip_tracker_service.remove_profile(profiles[1][0])
        trip_tracker_service.add_profile("Charlie")

        profiles = trip_tracker_service.get_profiles()
        self.assertEqual(len(profiles), 2)
        self.assertEqual(profiles[1][1], "Charlie")
        trip_tracker_service.select_profile(profiles[1][0])

        trip_tracker_service.add_trip(
            "Test2_1", "2022-01-01 08:00", "2022-01-01 09:00", 10000)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 1)
        trip_tracker_service.select_profile(-1)

        trip_tracker_service.select_profile(1)
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 3)
        trip_1 = trips[0]
        self.assertEqual(trip_1.name, "Test1_3")
        self.assertEqual(trip_1.duration, 3600)
        self.assertEqual(trip_1.length, 10000)
        self.assertEqual(trip_1.speed, 10000/3600)

        avg_speed, avg_duration, avg_length, speeds, durations, lengths, dates = trip_tracker_service.get_statistics()

        self.assertAlmostEqual(avg_speed, 1.47, 2)
        self.assertEqual(avg_duration, 50320)
        self.assertEqual(avg_length, 35200)

        speeds_test = [2.78, 1.03, 0.61]
        durations_test = [3600, 12480, 134880]
        lengths_test = [10000, 12800, 82800]
        dates_test = ["2022-01-01 08:00:00",
                      "2022-01-01 12:00:00", "2022-03-01 02:00:00"]

        for i in range(len(speeds)):
            self.assertAlmostEqual(speeds[i], speeds_test[i], 2)
            self.assertEqual(durations[i], durations_test[i])
            self.assertEqual(lengths[i], lengths_test[i])
            self.assertEqual(dates[i], dates_test[i])

        trip_tracker_service.remove_trip(trip_1.id)
        trip_tracker_service.select_time_range("2022", "2022-01")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 1)
        trip_tracker_service.select_time_range("2022", "2022-03")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 2)
        trip_tracker_service.select_time_range("2022", "2022-01")
        trip_tracker_service.select_time_range("2022", "2022-X1")
        trips = trip_tracker_service.get_trips()
        self.assertEqual(len(trips), 1)
