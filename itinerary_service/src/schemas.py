class TravelPlan:
    def __init__(
        self, 
        id: str = "",
        title: str = "", 
        description: str = "", 
        location_name: str | None = None,
        location_lat: float | None = None, 
        location_long: float | None = None, 
        arrival_date: int | None = None,
        departure_date: int | None = None, 
        user_email: str = ""
    ):
        self.id = id
        self.title = title
        self.description = description
        self.location_name = location_name
        self.location_lat = location_lat
        self.location_long = location_long
        self.arrival_date = arrival_date
        self.departure_date = departure_date
        self.user_email = user_email