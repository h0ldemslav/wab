from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LastRatingRequest(_message.Message):
    __slots__ = ["coffee_shop_id", "amount"]
    COFFEE_SHOP_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    coffee_shop_id: str
    amount: int
    def __init__(self, coffee_shop_id: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class RatingMessage(_message.Message):
    __slots__ = ["date", "value"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    date: str
    value: float
    def __init__(self, date: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...

class LastRatingResponse(_message.Message):
    __slots__ = ["ratings"]
    RATINGS_FIELD_NUMBER: _ClassVar[int]
    ratings: _containers.RepeatedCompositeFieldContainer[RatingMessage]
    def __init__(self, ratings: _Optional[_Iterable[_Union[RatingMessage, _Mapping]]] = ...) -> None: ...
