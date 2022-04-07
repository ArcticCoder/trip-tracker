import tkinter as tk
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

    def _show_trips_view(self, profile_id):
        self._hide_current_view()
        self._current_view = TripView(
            self._root, profile_id, self._handle_exit_trip_view)
        self._current_view.pack()

    def _handle_profile_select(self, profile_id):
        self._show_trips_view(profile_id)

    def _handle_exit_trip_view(self):
        self._show_profile_view()
