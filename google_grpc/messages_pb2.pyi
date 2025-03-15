from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Student(_message.Message):
    __slots__ = ("name", "avg_grade", "dob")
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVG_GRADE_FIELD_NUMBER: _ClassVar[int]
    DOB_FIELD_NUMBER: _ClassVar[int]
    name: str
    avg_grade: float
    dob: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., avg_grade: _Optional[float] = ..., dob: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Classroom(_message.Message):
    __slots__ = ("profile", "students")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    STUDENTS_FIELD_NUMBER: _ClassVar[int]
    profile: str
    students: _containers.RepeatedCompositeFieldContainer[Student]
    def __init__(self, profile: _Optional[str] = ..., students: _Optional[_Iterable[_Union[Student, _Mapping]]] = ...) -> None: ...

class ClassStats(_message.Message):
    __slots__ = ("numstudents", "grade")
    NUMSTUDENTS_FIELD_NUMBER: _ClassVar[int]
    GRADE_FIELD_NUMBER: _ClassVar[int]
    numstudents: int
    grade: float
    def __init__(self, numstudents: _Optional[int] = ..., grade: _Optional[float] = ...) -> None: ...
