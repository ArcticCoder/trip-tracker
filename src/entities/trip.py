class Trip:
    def __init__(self, trip_id: int, name: str, start_time: str, end_time: str,
                 duration: int, length: int):
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
