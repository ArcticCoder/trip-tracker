from repositories.profile_repository import profile_repository


class TripTrackerService:
    def __init__(self):
        pass

    def get_profiles(self):
        return profile_repository.list_all()

    def add_profile(self, name: str):
        profile_repository.add(name)

    def remove_profile(self, profile_id: int):
        profile_repository.remove(profile_id)


trip_tracker_service = TripTrackerService()
