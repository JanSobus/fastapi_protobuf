"""Client implementation for FastAPI using Google protobuf string serialization."""

import datetime
import logging
import sys
from datetime import datetime as dt
from time import perf_counter

import requests
from google.protobuf.timestamp_pb2 import Timestamp

from google_pb.messages_pb2 import Classroom, ClassStats, Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

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

    message_size = sys.getsizeof(classroom.SerializeToString())
    logger.info("Serialized (byte string) vanilla PB message size is %s bytes.", message_size)

    t0 = perf_counter()
    classroom_string = classroom.SerializeToString()
    response = requests.post("http://127.0.0.1:8000/classroom", data=classroom_string, timeout=10)
    logger.info("Response status code: %s", response.status_code)
    result_msg = ClassStats.FromString(response.content)
    t1 = perf_counter()
    response_size = sys.getsizeof(response.content)
    logger.info("Response size: %s bytes", response_size)
    logger.info("Time to receive response: %s miliseconds. Result message: %s", (t1 - t0) * 1000, result_msg)


if __name__ == "__main__":
    main()
