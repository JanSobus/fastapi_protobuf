"""Client implementation for FastAPI using betterproto."""

import datetime
import logging
import sys
from datetime import datetime as dt
from time import perf_counter

import requests
from betterproto import Casing

from betterproto_pb.school import Classroom, ClassStats, Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def main() -> None:
    """Run the client."""
    student_1 = Student(name="John", avg_grade=95.5, dob=dt(1990, 1, 15, tzinfo=datetime.UTC))
    student_2 = Student(name="Jane", avg_grade=90.0, dob=dt(1995, 2, 20, tzinfo=datetime.UTC))
    student_3 = Student(name="Jim", avg_grade=88.0, dob=dt(1992, 3, 10, tzinfo=datetime.UTC))
    classroom = Classroom(profile="Math", students=[student_1, student_2, student_3])

    message_size = sys.getsizeof(classroom.to_dict(Casing.SNAKE))  # type: ignore[attr-defined]
    logger.info("JSON message size from betterproto PB: %s bytes", message_size)

    t0 = perf_counter()
    classroom_json = classroom.to_dict(Casing.SNAKE)  # type: ignore[attr-defined]
    response = requests.post("http://127.0.0.1:8000/classroom", json=classroom_json, timeout=10)
    logger.info("Response status code: %s", response.status_code)
    logger.info("Response JSON: %s", response.json())
    result_msg = ClassStats(**response.json())
    t1 = perf_counter()
    response_size = sys.getsizeof(response.content)
    logger.info("Response size: %s bytes", response_size)
    logger.info("Time to receive response: %s miliseconds. Result message: %s", (t1 - t0) * 1000, result_msg)


if __name__ == "__main__":
    main()
