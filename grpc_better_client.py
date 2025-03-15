"""Client implementation for gRPC service using betterproto objects."""

import asyncio
import datetime
import logging
import sys
from datetime import datetime as dt
from time import perf_counter

from grpclib.client import Channel

from betterproto_pb.school import Classroom, ClassroomSummaryStub, Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def main(port: int = 50051) -> None:
    """Run the client."""
    student_1 = Student(name="John", avg_grade=95.5, dob=dt(1990, 1, 15, tzinfo=datetime.UTC))
    student_2 = Student(name="Jane", avg_grade=92.3, dob=dt(1995, 2, 20, tzinfo=datetime.UTC))
    student_3 = Student(name="Jim", avg_grade=88.0, dob=dt(1992, 3, 10, tzinfo=datetime.UTC))
    classroom = Classroom(profile="Math", students=[student_1, student_2, student_3])

    # Calculate request size in bytes
    request_size = sys.getsizeof(classroom)
    logger.info("Request size: %s bytes", request_size)

    async with Channel("127.0.0.1", port) as channel:
        client = ClassroomSummaryStub(channel)

        # Measure execution time
        start_time = perf_counter()
        response = await client.summarize_classroom(classroom)
        end_time = perf_counter()

        # Calculate response size in bytes
        response_size = sys.getsizeof(response.SerializeToString())

        # Print results
        logger.info("Response: %s", response)
        logger.info("Execution time: %s ms", (end_time - start_time) * 1000)
        logger.info("Response size: %s bytes", response_size)


if __name__ == "__main__":
    asyncio.run(main())
