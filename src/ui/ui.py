import tkinter as tk
from services.trip_tracker_service import trip_tracker_service
from ui.profile_view import ProfileView
from ui.trip_view import TripView


class UI:
    """Graafisesta käyttöliittymästä vastaava luokka."""

    def __init__(self, root):
        """Luokan konstruktori

        Args:
            root:
                TKinter-elementti, jonka sisään käyttöliittymä luodaan.
        """
        self._root = root
        self._current_view = None

    def start(self):
        """Käynnistää graafisen käyttöliittymän."""
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

    def _handle_profile_select(self, profile_id: int):
        #Avaa matkanäkymän, kun profiili valitaan
        trip_tracker_service.select_profile(profile_id)
        trip_tracker_service.select_time_range()
        self._show_trips_view()

    def _handle_exit_trip_view(self):
        #Palaa profiilin valintaa, kun matkanäkymä suljetaan
        trip_tracker_service.select_profile(-1)
        self._show_profile_view()
