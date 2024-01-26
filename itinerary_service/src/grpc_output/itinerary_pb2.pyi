from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TravelPlan(_message.Message):
    __slots__ = ("id", "title", "description", "location_name", "location_lat", "location_long", "arrival_date", "departure_date", "user_email")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCATION_LAT_FIELD_NUMBER: _ClassVar[int]
    LOCATION_LONG_FIELD_NUMBER: _ClassVar[int]
    ARRIVAL_DATE_FIELD_NUMBER: _ClassVar[int]
    DEPARTURE_DATE_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    location_name: str
    location_lat: float
    location_long: float
    arrival_date: int
    departure_date: int
    user_email: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., location_name: _Optional[str] = ..., location_lat: _Optional[float] = ..., location_long: _Optional[float] = ..., arrival_date: _Optional[int] = ..., departure_date: _Optional[int] = ..., user_email: _Optional[str] = ...) -> None: ...

class TravelPlanResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[TravelPlan]
    def __init__(self, data: _Optional[_Iterable[_Union[TravelPlan, _Mapping]]] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ("access_token", "token_type", "id_token", "expires_at", "userinfo")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    USERINFO_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    token_type: str
    id_token: str
    expires_at: int
    userinfo: UserInfo
    def __init__(self, access_token: _Optional[str] = ..., token_type: _Optional[str] = ..., id_token: _Optional[str] = ..., expires_at: _Optional[int] = ..., userinfo: _Optional[_Union[UserInfo, _Mapping]] = ...) -> None: ...

class UserInfo(_message.Message):
    __slots__ = ("email", "name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class TokenWithTravelPlan(_message.Message):
    __slots__ = ("token", "travel_plan")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    TRAVEL_PLAN_FIELD_NUMBER: _ClassVar[int]
    token: Token
    travel_plan: TravelPlan
    def __init__(self, token: _Optional[_Union[Token, _Mapping]] = ..., travel_plan: _Optional[_Union[TravelPlan, _Mapping]] = ...) -> None: ...
