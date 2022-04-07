import tkinter as tk
from functools import partial
from services.trip_tracker_service import trip_tracker_service


class ProfileView():
    def __init__(self, root, handle_profile_select):
        self._root = root
        self._handle_profile_select = handle_profile_select
        self._frame = tk.Frame(self._root)
        self._user_frame = tk.Frame(self._frame)

        self._new_user_frame = tk.Frame(self._frame, pady=5)
        self._new_name_lbl = tk.Label(
            self._new_user_frame, text="Nimi:", padx=5)
        self._new_name_entry = tk.Entry(self._new_user_frame)
        self._new_name_entry.bind(
            "<Return>", lambda event: self._handle_add_btn())
        self._new_user_btn = tk.Button(
            self._new_user_frame, text="Lisää", command=self._handle_add_btn, padx=5)

        self._new_name_lbl.grid(row=0, column=0)
        self._new_name_entry.grid(row=0, column=1)
        self._new_user_btn.grid(row=0, column=2)
        self._new_user_frame.pack(fill=tk.constants.BOTH, expand=True)

        self._print_profiles()

    def pack(self):
        self._frame.pack(fill=tk.constants.BOTH, expand=True)
        self._root.update()
        self._root.resizable(False, False)

    def destroy(self):
        self._frame.destroy()
        self._root.resizable(True, True)

    def _print_profiles(self):
        if self._user_frame:
            self._user_frame.destroy()

        users = trip_tracker_service.get_profiles()
        if users:
            self._user_frame = tk.Frame(self._frame)

            for i in range(len(users)):
                text = users[i][1]
                name_btn = tk.Button(self._user_frame, text=text, anchor=tk.constants.W,
                                     activebackground="grey", bg="lightgrey", highlightbackground="black", relief=tk.constants.FLAT,
                                     command=partial(self._handle_profile_select, users[i][1]))
                name_btn.grid(row=i, column=0, sticky=tk.constants.EW)

                del_btn = tk.Button(self._user_frame, text="X", anchor=tk.constants.W,
                                    activebackground="grey", bg="lightgrey", highlightbackground="black", relief=tk.constants.FLAT,
                                    command=partial(self._del_btn_click, users[i][1]))
                del_btn.grid(row=i, column=1, sticky=tk.constants.EW)

            self._user_frame.pack(fill=tk.constants.BOTH, expand=True)

    def _handle_add_btn(self):
        name = self._new_name_entry.get()
        self._new_name_entry.delete(0, "end")
        trip_tracker_service.add_profile(name)
        self._print_profiles()

    def _del_btn_click(self, name):
        trip_tracker_service.remove_profile(name)
        self._print_profiles()
