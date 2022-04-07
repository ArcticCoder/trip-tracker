import tkinter as tk
import tkinter.font as tkf
from functools import partial
from entities.trip import Trip
from services.trip_tracker_service import trip_tracker_service


class TripView():
    def __init__(self, root, profile_id):
        self._root = root
        self._profile_id = profile_id
        self._frame = tk.Frame(self._root)
        self._trips_frame = tk.Frame(self._root)

        #self._new_user_frame = tk.Frame(self._frame, pady=5)
        # self._new_name_lbl = tk.Label(
        #    self._new_user_frame, text="Nimi:", padx=5)
        #self._new_name_entry = tk.Entry(self._new_user_frame)
        # self._new_name_entry.bind(
        #    "<Return>", lambda event: self._handle_add_btn())
        # self._new_user_btn = tk.Button(
        #    self._new_user_frame, text="Lisää", command=self._handle_add_btn, padx=5)

        #self._new_name_lbl.grid(row=0, column=0)
        #self._new_name_entry.grid(row=0, column=1)
        #self._new_user_btn.grid(row=0, column=2)
        #self._new_user_frame.pack(fill=tk.constants.BOTH, expand=True)

        self._print_trips()

    def pack(self):
        self._frame.pack(fill=tk.constants.BOTH, expand=True)
        self._root.update()
        self._root.resizable(False, False)

    def destroy(self):
        self._frame.destroy()
        self._root.resizable(True, True)

    def _print_trips(self):
        if self._trips_frame:
            self._trips_frame.destroy()

        self._trips_frame = tk.Frame(self._frame)

        name_lbl = tk.Label(self._trips_frame, text="Nimi", anchor=tk.constants.W,
                            bg="lightgrey", borderwidth=2, relief=tk.constants.RAISED)
        name_lbl.grid(row=0, column=0, sticky=tk.constants.NSEW)

        start_lbl = tk.Label(self._trips_frame, text="Aloitus", anchor=tk.constants.W,
                             bg="lightgrey", borderwidth=2, relief=tk.constants.RAISED)
        start_lbl.grid(row=0, column=1, sticky=tk.constants.NSEW)

        end_lbl = tk.Label(self._trips_frame, text="Lopetus", anchor=tk.constants.W,
                           bg="lightgrey", borderwidth=2, relief=tk.constants.RAISED)
        end_lbl.grid(row=0, column=2, sticky=tk.constants.NSEW)

        duration_lbl = tk.Label(self._trips_frame, text="Kesto", anchor=tk.constants.W,
                                bg="lightgrey", borderwidth=2, relief=tk.constants.RAISED)
        duration_lbl.grid(row=0, column=3, sticky=tk.constants.NSEW)

        length_lbl = tk.Label(self._trips_frame, text="Pituus (m)", anchor=tk.constants.W,
                              bg="lightgrey", borderwidth=2, relief=tk.constants.RAISED)
        length_lbl.grid(row=0, column=4, sticky=tk.constants.NSEW)

        speed_lbl = tk.Label(self._trips_frame, text="Keskinopeus (m/s)", anchor=tk.constants.W,
                             bg="lightgrey", borderwidth=2, relief=tk.constants.RAISED)
        speed_lbl.grid(row=0, column=5, sticky=tk.constants.NSEW)

        empty_btn = tk.Button(self._trips_frame, text="", anchor=tk.constants.W,
                              activebackground="grey", bg="grey", highlightbackground="grey", relief=tk.constants.FLAT)
        empty_btn.grid(row=0, column=6, sticky=tk.constants.EW)

        trips = trip_tracker_service.get_trips(self._profile_id)
        if trips:
            for i in range(len(trips)):
                trip = trips[i]

                length_str = f"{trip.length:.0f}"
                duration_str = trip_tracker_service.seconds_to_string(
                    trip.duration)
                speed_str = f"{trip.speed:.2f}"

                name_lbl = tk.Label(self._trips_frame, text=trip.name, anchor=tk.constants.W,
                                    bg="lightgrey", borderwidth=1, relief=tk.constants.SOLID)
                name_lbl.grid(row=i+1, column=0, sticky=tk.constants.NSEW)

                start_lbl = tk.Label(self._trips_frame, text=trip.start_time, anchor=tk.constants.W,
                                     bg="lightgrey", borderwidth=1, relief=tk.constants.SOLID)
                start_lbl.grid(row=i+1, column=1, sticky=tk.constants.NSEW)

                end_lbl = tk.Label(self._trips_frame, text=trip.end_time, anchor=tk.constants.W,
                                   bg="lightgrey", borderwidth=1, relief=tk.constants.SOLID)
                end_lbl.grid(row=i+1, column=2, sticky=tk.constants.NSEW)

                duration_lbl = tk.Label(self._trips_frame, text=duration_str, anchor=tk.constants.W,
                                        bg="lightgrey", borderwidth=1, relief=tk.constants.SOLID)
                duration_lbl.grid(row=i+1, column=3, sticky=tk.constants.NSEW)

                length_lbl = tk.Label(self._trips_frame, text=length_str, anchor=tk.constants.W,
                                      bg="lightgrey", borderwidth=1, relief=tk.constants.SOLID)
                length_lbl.grid(row=i+1, column=4, sticky=tk.constants.NSEW)

                speed_lbl = tk.Label(self._trips_frame, text=speed_str, anchor=tk.constants.W,
                                     bg="lightgrey", borderwidth=1, relief=tk.constants.SOLID)
                speed_lbl.grid(row=i+1, column=5, sticky=tk.constants.NSEW)

                del_btn = tk.Button(self._trips_frame, text="X", anchor=tk.constants.W,
                                    activebackground="grey", bg="lightgrey", highlightbackground="black", relief=tk.constants.FLAT,
                                    command=partial(self._del_btn_click, trip.id))
                del_btn.grid(row=i+1, column=6, sticky=tk.constants.EW)

        self._trips_frame.pack(fill=tk.constants.BOTH, expand=True)

    def _handle_add_btn(self):
        # TODO get info
        #name = self._new_name_entry.get()
        #self._new_name_entry.delete(0, "end")
        trip_tracker_service.add_trip(name)
        self._print_trips()

    def _del_btn_click(self, trip_id):
        trip_tracker_service.remove_trip(trip_id)
        self._print_trips()
