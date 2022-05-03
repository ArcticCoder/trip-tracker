class Trip:
    """Yksittäistä matkaa edustava luokka."""

    def __init__(self, trip_id: int, name: str, start_time: str, end_time: str,
                 duration: int, length: int):
        """Luokan konstruktori.

        Args:
            trip_id:
                Matkan id tietokannassa kokonaislukuna.
            name:
                Matkan nimi merkkijonona.
            start_time:
                Matkan alkamisen aikaa edustava merkkijono muodossa
                YYYY-MM-DD HH:MM(:SS), suluissa olevat valinnaisia.
            end_time:
                Matkan lopumisen aikaa edustava merkkijono muodossa
                YYYY-MM-DD HH:MM(:SS), suluissa olevat valinnaisia.
            duratin:
                Matkan kesto sekunteina kokonaislukuna.
            length:
                Matkan pituus metreinä kokonaislukuna.
        """
        self.id = trip_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.length = length
        if self.duration != 0:
            self.speed = self.length / self.duration
        else:
            self.speed = 0
