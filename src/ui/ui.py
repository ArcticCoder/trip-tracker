import tkinter as tk
from services.trip_tracker_service import trip_tracker_service
from ui.profile_view import ProfileView
from ui.trip_view import TripView


class UI:
    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_profile_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()
        self._current_view = None

    def _show_profile_view(self):
        self._hide_current_view()
        self._current_view = ProfileView(
            self._root, self._handle_profile_select)
        self._current_view.pack()

    def _show_trips_view(self):
        self._hide_current_view()
        self._current_view = TripView(
            self._root, self._handle_exit_trip_view)
        self._current_view.pack()

    def _handle_profile_select(self, profile_id):
        trip_tracker_service.select_profile(profile_id)
        trip_tracker_service.select_time_range()
        self._show_trips_view()

    def _handle_exit_trip_view(self):
        trip_tracker_service.select_profile(-1)
        trip_tracker_service.select_time_range()
        self._show_profile_view()
