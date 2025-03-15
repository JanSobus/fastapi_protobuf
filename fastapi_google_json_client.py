"""Client implementation for FastAPI using google protobuf JSON serialization."""

import datetime
import logging
import sys
from datetime import datetime as dt
from time import perf_counter

import requests
from google.protobuf import json_format
from google.protobuf.timestamp_pb2 import Timestamp

from google_pb.messages_pb2 import Classroom, ClassStats, Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main() -> None:
    """Run the client."""
    timestamp = Timestamp()
    timestamp.FromDatetime(dt(1990, 1, 15, tzinfo=datetime.UTC))
    student_1 = Student(name="John", avg_grade=95.5, dob=timestamp)
    timestamp.FromDatetime(dt(1995, 2, 20, tzinfo=datetime.UTC))
    student_2 = Student(name="Jane", avg_grade=90.0, dob=timestamp)
    timestamp.FromDatetime(dt(1992, 3, 10, tzinfo=datetime.UTC))
    student_3 = Student(name="Jim", avg_grade=88.0, dob=timestamp)
    classroom = Classroom(profile="Math", students=[student_1, student_2, student_3])

    message_size = sys.getsizeof(json_format.MessageToDict(classroom, preserving_proto_field_name=True))
    logger.info("JSON message size from vanilla protobuf: %s bytes", message_size)

    t0 = perf_counter()
    classroom_json = json_format.MessageToDict(classroom, preserving_proto_field_name=True)
    response = requests.post("http://127.0.0.1:8000/classroom", json=classroom_json, timeout=10)
    logger.info("Response status code: %s", response.status_code)
    logger.info("Response JSON: %s", response.json())
    result_msg = json_format.ParseDict(response.json(), ClassStats())
    t1 = perf_counter()
    logger.info("Time to receive response: %s seconds. Result message: %s", t1 - t0, result_msg)


if __name__ == "__main__":
    main()
