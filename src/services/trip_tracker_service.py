import re
from repositories.profile_repository import profile_repository
from repositories.trip_repository import trip_repository


class TripTrackerService:
    def __init__(self):
        pass

    def get_profiles(self):
        return profile_repository.list_all()

    def add_profile(self, name: str):
        profile_repository.add(name)

    def remove_profile(self, profile_id: int):
        trip_repository.remove_by_profile(profile_id)
        profile_repository.remove(profile_id)

    def get_trips(self, profile_id):
        return trip_repository.find_by_profile(profile_id)

    def add_trip(self, profile_id: int, name: str, start_time: str, end_time: str, length: int):
        trip_repository.add(profile_id, name, start_time, end_time, length)

    def remove_trip(self, trip_id):
        trip_repository.remove(trip_id)

    def seconds_to_string(self, seconds):
        hours = seconds // 3600
        seconds -= hours*3600
        minutes = seconds // 60
        seconds -= minutes*60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def valid_time(self, time: str):
        pattern1 = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
        pattern2 = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
        return pattern1.match(time) or pattern2.match(time)


trip_tracker_service = TripTrackerService()
