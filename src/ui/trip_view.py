import tkinter as tk
import matplotlib.dates
from datetime import datetime
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from entities.trip import Trip
from services.trip_tracker_service import trip_tracker_service


class TripView():
    def __init__(self, root, handle_exit_btn):
        self._root = root
        self._handle_exit_btn = handle_exit_btn
        self._frame = tk.Frame(self._root)
        self._trips_frame = tk.Frame(self._root)

        self._statistics_view()
        self._print_statistics()

        self._new_trip_view()
        self._trip_selection_view()
        self._print_trips()

    def pack(self):
        self._frame.pack(fill=tk.constants.BOTH, expand=True)
        self._root.update()
        self._root.resizable(False, False)

    def destroy(self):
        self._frame.destroy()
        self._root.resizable(True, True)

    def _new_trip_view(self):
        self._new_trip_frame = tk.Frame(
            self._frame, borderwidth=2, relief=tk.constants.SUNKEN, pady=5)

        self._new_name_lbl = tk.Label(
            self._new_trip_frame, text="Nimi:", padx=5)
        self._new_name_entry = tk.Entry(self._new_trip_frame)
        self._new_length_lbl = tk.Label(
            self._new_trip_frame, text="Pituus:", padx=5)
        self._new_length_entry = tk.Entry(self._new_trip_frame)
        self._length_format_lbl = tk.Label(
            self._new_trip_frame, text="(m)", padx=5)

        self._default_datetime_str = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self._new_start_lbl = tk.Label(
            self._new_trip_frame, text="Aloitus:", padx=5)
        self._new_start_entry = tk.Entry(self._new_trip_frame)
        self._new_start_entry.insert(0, self._default_datetime_str)
        self._new_end_lbl = tk.Label(
            self._new_trip_frame, text="Lopetus:", padx=5)
        self._new_end_entry = tk.Entry(self._new_trip_frame)
        self._new_end_entry.insert(0, self._default_datetime_str)
        self._time_format_lbl = tk.Label(
            self._new_trip_frame, text="(YYYY-MM-DD HH:MM(:SS)", padx=5)

        self._new_trip_btn = tk.Button(
            self._new_trip_frame, text="Lisää", command=self._handle_add_btn, padx=5)
        self._exit_btn = tk.Button(
            self._new_trip_frame, text="Poistu", command=self._handle_exit_btn, padx=5)

        self._new_name_lbl.grid(row=0, column=0)
        self._new_name_entry.grid(row=0, column=1)
        self._new_length_lbl.grid(row=0, column=2)
        self._new_length_entry.grid(row=0, column=3)
        self._length_format_lbl.grid(row=0, column=4, sticky=tk.constants.W)

        self._new_start_lbl.grid(row=1, column=0)
        self._new_start_entry.grid(row=1, column=1)
        self._new_end_lbl.grid(row=1, column=2)
        self._new_end_entry.grid(row=1, column=3)
        self._time_format_lbl.grid(row=1, column=4)

        self._new_trip_btn.grid(row=6, column=0)
        self._exit_btn.grid(row=6, column=1)
        self._new_trip_frame.pack()

    def _trip_selection_view(self):
        self._trip_selection_frame = tk.Frame(
            self._frame, borderwidth=2, relief=tk.constants.SUNKEN, pady=5)

        self._start_lbl = tk.Label(
            self._trip_selection_frame, text="Alku:", padx=5)
        self._start_entry = tk.Entry(self._trip_selection_frame)
        self._end_lbl = tk.Label(
            self._trip_selection_frame, text="Loppu:", padx=5)
        self._end_entry = tk.Entry(self._trip_selection_frame)
        self._time_range_format_lbl = tk.Label(
            self._trip_selection_frame, text="(YYYY(-MM-DD HH:MM:SS))", padx=5)

        self._range_select_btn = tk.Button(
            self._trip_selection_frame, text="Rajaa", command=self._handle_range_select_btn, padx=5)

        self._start_lbl.grid(row=0, column=0)
        self._start_entry.grid(row=0, column=1)
        self._end_lbl.grid(row=0, column=2)
        self._end_entry.grid(row=0, column=3)
        self._time_range_format_lbl.grid(
            row=0, column=4, sticky=tk.constants.W)
        self._range_select_btn.grid(row=1, column=0)
        self._trip_selection_frame.pack()

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

        trips = trip_tracker_service.get_trips()
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

    def _statistics_view(self):
        self._statistics_frame = tk.Frame(
            self._frame, borderwidth=2, relief=tk.constants.SUNKEN)

        self._speed_lbl = tk.Label(self._statistics_frame)
        self._speed_lbl.pack()

        self._duration_lbl = tk.Label(self._statistics_frame)
        self._duration_lbl.pack()

        self._length_lbl = tk.Label(self._statistics_frame)
        self._length_lbl.pack()

        self._statistics_fig = Figure(figsize=(6, 6), dpi=100)
        self._statistics_fig.patch.set_facecolor(self._speed_lbl.cget("bg"))
        self._stats_canvas = FigureCanvasTkAgg(
            self._statistics_fig, master=self._statistics_frame)
        toolbar = NavigationToolbar2Tk(
            self._stats_canvas, self._statistics_frame)
        toolbar.update()
        self._stats_canvas.get_tk_widget().pack()

        self._speed_plt = self._statistics_fig.add_subplot(211)
        self._duration_plt = self._statistics_fig.add_subplot(223)
        self._length_plt = self._statistics_fig.add_subplot(224)

        self._statistics_frame.pack(
            side=tk.constants.LEFT, fill=tk.constants.Y, expand=True)

    def _print_statistics(self):
        avg_speed, avg_duration, avg_length, speeds, durations, lengths, dates = trip_tracker_service.get_statistics()
        dates = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date()
                 for d in dates]

        self._speed_lbl.config(text=f"Keskinopeus: {avg_speed:.1f} m/s")
        self._duration_lbl.config(
            text=f"Keskimääräinen kesto {trip_tracker_service.seconds_to_string(avg_duration)}")
        self._length_lbl.config(
            text=f"Keskimääräinen pituus {avg_length:.1f} m")

        self._speed_plt.clear()
        self._speed_plt.scatter(dates, speeds)
        self._speed_plt.grid()
        self._speed_plt.set_ylim([0, None])
        self._speed_plt.set(xlabel="Päivämäärä", ylabel="Keskinopeus (m/s)")
        self._speed_plt.xaxis.set_major_formatter(
            matplotlib.dates.DateFormatter("%Y-%m-%d"))
        self._speed_plt.xaxis.set_major_locator(
            matplotlib.dates.MonthLocator())
        self._speed_plt.tick_params(labelbottom=False)

        self._duration_plt.clear()
        self._duration_plt.scatter(
            dates, [duration/60 for duration in durations])
        self._duration_plt.grid()
        self._duration_plt.set_ylim([0, None])
        self._duration_plt.set(xlabel="Päivämäärä", ylabel="Kesto (min)")
        self._duration_plt.xaxis.set_major_formatter(
            matplotlib.dates.DateFormatter("%Y-%m-%d"))
        self._duration_plt.xaxis.set_major_locator(
            matplotlib.dates.MonthLocator())
        self._duration_plt.tick_params(labelbottom=False)

        self._length_plt.clear()
        self._length_plt.scatter(dates, lengths)
        self._length_plt.grid()
        self._length_plt.set_ylim([0, None])
        self._length_plt.set(xlabel="Päivämäärä", ylabel="Matka (m)")
        self._length_plt.xaxis.set_major_formatter(
            matplotlib.dates.DateFormatter("%Y-%m-%d"))
        self._length_plt.xaxis.set_major_locator(
            matplotlib.dates.MonthLocator())
        self._length_plt.tick_params(labelbottom=False)

        self._statistics_fig.tight_layout(pad=0.25)
        self._stats_canvas.draw()

    def _handle_add_btn(self):
        name = self._new_name_entry.get()

        start_time = self._new_start_entry.get()
        if not trip_tracker_service.valid_time(start_time):
            self._new_start_entry.delete(0, "end")
            self._new_start_entry.insert(0, self._default_datetime_str)
            return

        end_time = self._new_end_entry.get()
        if not trip_tracker_service.valid_time(end_time):
            self._new_end_entry.delete(0, "end")
            self._new_end_entry.insert(0, self._default_datetime_str)
            return

        if start_time > end_time:
            self._new_start_entry.delete(0, "end")
            self._new_start_entry.insert(0, self._default_datetime_str)
            self._new_end_entry.delete(0, "end")
            self._new_end_entry.insert(0, self._default_datetime_str)
            return

        try:
            length = int(self._new_length_entry.get())
        except ValueError:
            self._new_length_entry.delete(0, "end")
            return

        if length < 0:
            self._new_length_entry.delete(0, "end")
            return

        self._new_name_entry.delete(0, "end")
        self._new_start_entry.delete(0, "end")
        self._new_start_entry.insert(0, self._default_datetime_str)
        self._new_end_entry.delete(0, "end")
        self._new_end_entry.insert(0, self._default_datetime_str)
        self._new_length_entry.delete(0, "end")

        trip_tracker_service.add_trip(name, start_time, end_time, length)
        self._print_statistics()
        self._print_trips()

    def _handle_range_select_btn(self):
        start_time = self._start_entry.get()
        if start_time == "":
            start_time = None
        elif not trip_tracker_service.valid_date_time(start_time):
            self._start_entry.delete(0, "end")
            return

        end_time = self._end_entry.get()
        if end_time == "":
            end_time = None
        elif not trip_tracker_service.valid_date_time(end_time):
            self._end_entry.delete(0, "end")
            return

        if start_time and end_time and start_time > end_time:
            self._start_entry.delete(0, "end")
            self._end_entry.delete(0, "end")
            return

        trip_tracker_service.select_time_range(start_time, end_time)
        self._print_statistics()
        self._print_trips()

    def _del_btn_click(self, trip_id):
        trip_tracker_service.remove_trip(trip_id)
        self._print_statistics()
        self._print_trips()
