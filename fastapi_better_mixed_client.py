"""Client for the FastAPI server that supports both JSON and Protobuf requests."""

import datetime
import logging
import sys
from datetime import datetime as dt
from time import perf_counter

import betterproto
import requests

from betterproto_pb.school import Classroom, ClassStats, Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def main() -> None:
    """Test server endpoint with both JSON and Protobuf requests."""
    student_1 = Student(name="John", avg_grade=95.5, dob=dt(1990, 1, 15, tzinfo=datetime.UTC))
    student_2 = Student(name="Jane", avg_grade=92.3, dob=dt(1995, 2, 20, tzinfo=datetime.UTC))
    student_3 = Student(name="Jim", avg_grade=88.0, dob=dt(1992, 3, 10, tzinfo=datetime.UTC))
    classroom = Classroom(profile="Math", students=[student_1, student_2, student_3])

    logger.info("Running JSON request...")
    message_size = sys.getsizeof(classroom.to_dict(betterproto.Casing.SNAKE))  # type: ignore[arg-type]
    logger.info("JSON message size: %s bytes", message_size)
    t0 = perf_counter()
    classroom_json = classroom.to_dict(betterproto.Casing.SNAKE)  # type: ignore[arg-type]
    response = requests.post("http://127.0.0.1:8000/classroom", json=classroom_json, timeout=10)
    logger.info("JSON response size: %s bytes", sys.getsizeof(response.content))
    logger.info("JSON response status code: %s", response.status_code)
    result_object = ClassStats(**response.json())
    logger.info("JSON request completed in %s miliseconds", (perf_counter() - t0) * 1000)
    logger.info("Response: %s", result_object)

    logger.info("Running Protobuf request...")
    message_size = sys.getsizeof(classroom.SerializeToString())
    logger.info("Protobuf message size: %s bytes", message_size)
    t0 = perf_counter()
    response = requests.post(
        "http://127.0.0.1:8000/classroom",
        headers={"Content-Type": "application/x-protobuf"},
        data=classroom.SerializeToString(),
        timeout=10,
    )
    logger.info("Protobuf response size: %s bytes", sys.getsizeof(response.content))
    logger.info("Protobuf response status code: %s", response.status_code)
    result_object = ClassStats().FromString(response.content)
    logger.info("Protobuf request completed in %s miliseconds", (perf_counter() - t0) * 1000)
    logger.info("Response: %s", result_object)


if __name__ == "__main__":
    main()
