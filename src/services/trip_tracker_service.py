import datetime
import re
from repositories.profile_repository import profile_repository as default_profile_repository
from repositories.trip_repository import trip_repository as default_trip_repository


class TripTrackerService:
    """Ohjelman sovelluslogiikasta vastaa luokka.
    Kaikki toiminnallisuuden käyttäminen tapahtuu tämän luokan kautta.
    """

    def __init__(self, profile_repository=default_profile_repository,
                 trip_repository=default_trip_repository):
        """Luokan konstruktori."""
        self._profile_id = -1
        self._start_time = None
        self._end_time = None
        self._cache_invalid = True
        self._selected_trips = []
        self._profile_repository = profile_repository
        self._trip_repository = trip_repository

    def get_profiles(self):
        """Listaa kaikki profiilit.

        Returns:
            Lista tupleja, jotka edustavat profiileja muodossa (id, nimi)
        """
        return self._profile_repository.list_all()

    def add_profile(self, name: str):
        """Lisää uuden profiilin, jos nimi on saatavilla.

        Args:
            name:
                Uuden profiilin nimi merkkijonona.
        """
        self._profile_repository.add(name)

    def remove_profile(self, profile_id: int):
        """Poistaa profiilin ja siihen liittyvät matkat.

        Args:
            profile_id:
                Profiilin id tietokannassa kokonaislukuna.
        """
        self._trip_repository.remove_by_profile(profile_id)
        self._profile_repository.remove(profile_id)

    def select_profile(self, profile_id: int):
        """Valitsee uuden profiilin aktiiviseksi.

        Args:
            profile_id:
                Profiilin id tietokannassa kokonaislukuna.
        """
        if self._profile_id != profile_id:
            if self._profile_repository.exists(profile_id) or profile_id == -1:
                self._profile_id = profile_id
                self.select_time_range()
                self._cache_invalid = True

    def select_time_range(self, start_time: str = None, end_time: str = None):
        """Rajaa matkojen valinnan tietylle aikavälille.

        Args:
            start_time:
                Valinnainen, aikaisinta haluttua aikaa edustava merkkijono muodossa
                YYYY(-MM-DD HH:MM:SS), suluissa olevat valinnaisia.
            end_time:
                Valinnainen, viimeisintä haluttua aikaa edustava merkkijono muodossa
                YYYY(-MM-DD HH:MM:SS), suluissa olevat valinnaisia.
        """
        if self._start_time != start_time:
            if not start_time or self.valid_date_time(start_time):
                self._start_time = start_time
                self._cache_invalid = True
        if self._end_time != end_time:
            if not end_time:
                self._end_time = end_time
                self._cache_invalid = True
            elif self.valid_date_time(end_time):
                self._end_time = self.adjust_end_time(end_time)
                self._cache_invalid = True

    def get_trips(self):
        """Palauttaa valitut matkat.

        Returns:
            Lista Trip-olioita aikajärjestyksessä.
        """
        self._update_cache()
        return self._selected_trips

    # Pylint virheiden poistaminen, koska funktio on helppo seurata nykyisessä tilassa
    # ja muut ratkaisut olisivat pylintin miellyttämistä, eikä koodin parantamista.
    def get_statistics(self):  # pylint: disable=too-many-locals, too-many-statements
        """Laskee valituista matkoista erinnäisiä tilastoja.

        Returns:
            Matkojen keskivertonopeus m/s
            Matkojen keskivertokesto s
            Matkojen keskivertopituus m
            Matkojen keskinopeudet listana m/s
            Matkojen kestot listana s
            Matkojen pituudet listana m
            Matkojen alkamisajat merkkijonoina
        """
        self._update_cache()
        count = len(self._selected_trips)

        if count > 0:
            speed_sum = 0
            duration_sum = 0
            length_sum = 0
            speeds = []
            durations = []
            lengths = []
            dates = []

            for trip in self._selected_trips:
                speed = trip.speed
                duration = trip.duration
                length = trip.length

                speed_sum += speed
                duration_sum += duration
                length_sum += length

                speeds.append(speed)
                durations.append(duration)
                lengths.append(length)
                dates.append(trip.start_time)

            avg_speed = speed_sum/count
            avg_duration = duration_sum/count
            avg_length = length_sum/count
            return avg_speed, avg_duration, avg_length, speeds, durations, lengths, dates

        return 0, 0, 0, [], [], [], []

    def add_trip(self, name: str, start_time: str, end_time: str, length: int):
        """Lisää uuden matkan.

        Args:
            name:
                Matkan nimi merkkijonona.
            start_time:
                Matkan alkamisen aikaa edustava merkkijono muodossa
                YYYY-MM-DD HH:MM(:SS), suluissa olevat valinnaisia.
            end_time:
                Matkan lopumisen aikaa edustava merkkijono muodossa
                YYYY-MM-DD HH:MM(:SS), suluissa olevat valinnaisia.
            length:
                Matkan pituus metreinä kokonaislukuna.
        """
        if not self.valid_time(start_time) or not self.valid_time(end_time):
            return

        # Lisätään yhtenäisyyden vuoksi sekuntit, jos ne puuttuvat
        if len(start_time.split(" ")[1].split(":")) == 2:
            start_time = start_time + ":00"
        if len(end_time.split(" ")[1].split(":")) == 2:
            end_time = end_time + ":00"

        self._trip_repository.add(self._profile_id, name,
                                  start_time, end_time, length)
        self._cache_invalid = True

    def remove_trip(self, trip_id: int):
        """Poistaa halutun matkan tietokannasta.

        Args:
            trip_id:
                Matkan id tietokannassa kokonaislukuna.
        """
        self._trip_repository.remove(trip_id)
        self._cache_invalid = True

    def seconds_to_string(self, seconds: int):
        """Muuntaa sekuntien määrän aikaa edustavaksi merkkijonoksi.

        Args:
            seconds:
                Sekuntien määrä kokonaislukuna.

        Returns:
            Sekuntien määrää vastaava merkkijono muotoa HH:MM:SS.
        """
        hours = seconds // 3600
        seconds -= hours*3600
        minutes = seconds // 60
        seconds -= minutes*60
        return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"

    def valid_date_time(self, time: str):
        """Tarkistaa onko annettu merkkijono oikeassa muodossa ajanjakson alku/loppupisteeksi.
        Hyväksytyt:
        YYYY
        YYYY-MM
        YYYY-MM-DD
        YYYY-MM-DD HH
        YYYY-MM-DD HH:MM
        YYYY-MM-DD HH:MM:SS

        Args:
            time:
                Tarkistettava merkkijono.

        Returns:
            True, jos merkkijono validi. False muutoin.
        """
        pattern = re.compile(
            r"^\d{4}(|-\d{2}(|-\d{2}(| \d{2}(|:\d{2}(|:\d{2})))))$")
        if pattern.match(time):
            return self._datetime_checker(time)
        return False

    def valid_time(self, time: str):
        """Tarkistaa onko annettu merkkijono oikeassa muodossa matkan alku/loppuajaksi.
        Hyväksytyt:
        YYYY-MM-DD HH:MM
        YYYY-MM-DD HH:MM:SS

        Args:
            time:
                Tarkistettava merkkijono.

        Returns:
            True, jos merkkijono validi. False muutoin.
        """

        pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(|:\d{2})$")
        if pattern.match(time):
            return self._datetime_checker(time)
        return False

    def adjust_end_time(self, end_time: str):
        """Muuntaa annetun loppuajan muotoon, joka tekee valinnasta intuitiivisempaa.
        LOPPUTULOKSENA EI OLE TODELLISTA PÄIVÄMÄÄRÄÄ EDUSTAVA MERKKIJONO!

        Args:
            end_time:
                Muokattava merkkijono.

        Returns:
            Muokattu merkkijono, jos alkuperäinen oli validi valid_time metodin mukaan.
            Muussa tapauksessa tyhjä merkkijono.
        """
        if self.valid_date_time(end_time):
            date_time_arr = end_time.split(" ")

            date_arr = date_time_arr[0].split("-")
            while len(date_arr) < 3:
                date_arr.append(99)

            if len(date_time_arr) == 1:
                time_arr = []
            else:
                time_arr = date_time_arr[1].split(":")
            while len(time_arr) < 3:
                time_arr.append(99)

            return f"{date_arr[0]}-{date_arr[1]}-{date_arr[2]} "\
                f"{time_arr[0]}:{time_arr[1]}:{time_arr[2]}"
        return ""

    def _update_cache(self):
        if self._cache_invalid:
            self._selected_trips = self._trip_repository.find_by_profile(
                self._profile_id, self._start_time, self._end_time)
            self._cache_invalid = False

    # Yhdistää kahden julkisen tarkistus funktion yhteiset piirteet
    def _datetime_checker(self, time: str):
        negative_pattern = re.compile(r"^0000.*$")
        if negative_pattern.match(time):
            return False

        date_time_arr = time.split(" ")
        date_arr = date_time_arr[0].split("-")
        while len(date_arr) < 3:
            date_arr.append("01")

        if len(date_time_arr) == 1:
            time_arr = []
        else:
            time_arr = date_time_arr[1].split(":")
        while len(time_arr) < 3:
            time_arr.append("00")

        year = int(date_arr[0])
        month = int(date_arr[1])
        day = int(date_arr[2])

        hour = int(time_arr[0])
        minute = int(time_arr[1])
        second = int(time_arr[2])

        try:
            datetime.datetime(year, month, day, hour, minute, second)
            return True
        except ValueError:
            return False


trip_tracker_service = TripTrackerService()
