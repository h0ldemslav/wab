from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TravelPlan(_message.Message):
    __slots__ = ("id", "title", "location_name", "location_lat", "location_long", "arrival_date", "departure_date", "user_email")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_LAT_FIELD_NUMBER: _ClassVar[int]
    LOCATION_LONG_FIELD_NUMBER: _ClassVar[int]
    ARRIVAL_DATE_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_DATE_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    location_name: str
    location_lat: float
    location_long: float
    arrival_date: int
    departure_date: int
    user_email: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., location_name: _Optional[str] = ..., location_lat: _Optional[float] = ..., location_long: _Optional[float] = ..., arrival_date: _Optional[int] = ..., departure_date: _Optional[int] = ..., user_email: _Optional[str] = ...) -> None: ...

class TravelPlanResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[TravelPlan]
    def __init__(self, data: _Optional[_Iterable[_Union[TravelPlan, _Mapping]]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...
