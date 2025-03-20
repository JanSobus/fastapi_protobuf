"""gRPC client using Google protobuf objects."""

import asyncio
import datetime
import logging
import sys
from datetime import datetime as dt
from time import perf_counter

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

sys.path.append("./google_pb")

from google_pb.grpc_service_pb2_grpc import ClassroomSummaryStub
from google_pb.messages_pb2 import Classroom, Student

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


async def main(port: int = 50051) -> None:
    """Run the client."""
    timestamp = Timestamp()
    timestamp.FromDatetime(dt(1990, 1, 15, tzinfo=datetime.UTC))
    student_1 = Student(name="John", avg_grade=95.5, dob=timestamp)
    timestamp.FromDatetime(dt(1995, 2, 20, tzinfo=datetime.UTC))
    student_2 = Student(name="Jane", avg_grade=90.0, dob=timestamp)
    timestamp.FromDatetime(dt(1992, 3, 10, tzinfo=datetime.UTC))
    student_3 = Student(name="Jim", avg_grade=88.0, dob=timestamp)
    classroom = Classroom(profile="Math", students=[student_1, student_2, student_3])

    # Calculate request size in bytes
    request_size = sys.getsizeof(classroom)
    logger.info("Request size: %s bytes", request_size)

    # Create channel using grpcio
    channel = grpc.aio.insecure_channel(f"127.0.0.1:{port}")
    try:
        client = ClassroomSummaryStub(channel)
        start_time = perf_counter()
        response = await client.SummarizeClassroom(classroom)
        end_time = perf_counter()

        logger.info("Response: %s", response)
        logger.info("Execution time: %s ms", (end_time - start_time) * 1000)

        # Calculate response size in bytes
        response_size = sys.getsizeof(response.SerializeToString())
        logger.info("Response size: %s bytes", response_size)
    finally:
        await channel.close()


if __name__ == "__main__":
    asyncio.run(main())
