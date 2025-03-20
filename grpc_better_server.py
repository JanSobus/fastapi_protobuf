"""gRPC server using betterproto objects."""

from __future__ import annotations

import asyncio
import logging
import sys

from grpclib.server import Server

from betterproto_pb.school import Classroom, ClassroomSummaryBase, ClassStats

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


class ClassroomSummary(ClassroomSummaryBase):
    """Classroom summary service."""

    async def summarize_classroom(self, classroom: Classroom) -> ClassStats:
        """Summarize the classroom."""
        logger.info("Received classroom: %s", classroom)

        return ClassStats(
            numstudents=len(classroom.students),
            grade=sum(student.avg_grade for student in classroom.students) / len(classroom.students),
        )


async def main(port: int = 50051) -> None:
    """Run the server."""
    server = Server([ClassroomSummary()])
    await server.start("127.0.0.1", port)
    logger.info("Server started on 127.0.0.1:%s", port)
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
