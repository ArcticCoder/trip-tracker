import tkinter as tk
from functools import partial
from services.trip_tracker_service import trip_tracker_service


class ProfileView():
    """Matkanäkymästä vastaava luokka."""

    def __init__(self, root, handle_profile_select):
        """Luokan konstruktori.

        Args:
            root:
                TKinter-elementti, jonka sisään näkymä luodaan.
            handle_profile_select:
                Arvo, jota kutsutaan, kun profiili valitaan.
                Saa argumenttina valitun profiilin id:n.
        """
        self._root = root
        self._handle_profile_select = handle_profile_select
        self._frame = tk.Frame(self._root)
        self._profile_frame = tk.Frame(self._frame)

        self._new_profile_view()
        self._print_profiles()

    def pack(self):
        """Näyttää näkymän."""
        self._frame.pack(fill=tk.constants.BOTH, expand=True)
        self._root.update()
        self._root.resizable(False, False)

    def destroy(self):
        """Poistaa näkymän."""
        self._frame.destroy()
        self._root.resizable(True, True)

    def _new_profile_view(self):
        self._new_profile_frame = tk.Frame(self._frame, pady=5)
        self._new_name_lbl = tk.Label(
            self._new_profile_frame, text="Nimi:", padx=5)
        self._new_name_entry = tk.Entry(self._new_profile_frame)
        self._new_name_entry.bind(
            "<Return>", lambda event: self._handle_add_btn())
        self._new_profile_btn = tk.Button(
            self._new_profile_frame, text="Lisää", command=self._handle_add_btn, padx=5)

        self._new_name_lbl.grid(row=0, column=0)
        self._new_name_entry.grid(row=0, column=1)
        self._new_profile_btn.grid(row=0, column=2)
        self._new_profile_frame.pack(fill=tk.constants.BOTH, expand=True)

    def _print_profiles(self):
        if self._profile_frame:
            self._profile_frame.destroy()

        profiles = trip_tracker_service.get_profiles()
        if profiles:
            self._profile_frame = tk.Frame(self._frame)

            for i in range(len(profiles)):
                profile_id, name = profiles[i]
                name_btn = tk.Button(self._profile_frame, text=name, anchor=tk.constants.W,
                                     activebackground="grey", bg="lightgrey", highlightbackground="black", relief=tk.constants.FLAT,
                                     command=partial(self._handle_profile_select, profile_id))
                name_btn.grid(row=i, column=0, sticky=tk.constants.EW)

                del_btn = tk.Button(self._profile_frame, text="X", anchor=tk.constants.W,
                                    activebackground="grey", bg="lightgrey", highlightbackground="black", relief=tk.constants.FLAT,
                                    command=partial(self._del_btn_click, profile_id))
                del_btn.grid(row=i, column=1, sticky=tk.constants.EW)

            self._profile_frame.pack(fill=tk.constants.BOTH, expand=True)

    def _handle_add_btn(self):
        name = self._new_name_entry.get()
        self._new_name_entry.delete(0, "end")
        trip_tracker_service.add_profile(name)
        self._print_profiles()

    def _del_btn_click(self, profile_id):
        trip_tracker_service.remove_profile(profile_id)
        self._print_profiles()
