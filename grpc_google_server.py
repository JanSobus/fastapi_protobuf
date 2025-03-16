"""Server implementation of the gRPC Classroom service using Google's protobuf library."""

import logging
import sys
from concurrent import futures

import grpc

sys.path.append("./google_pb")

from google_pb.grpc_service_pb2_grpc import ClassroomSummaryServicer, add_ClassroomSummaryServicer_to_server
from google_pb.messages_pb2 import Classroom, ClassStats

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ClassroomSummary(ClassroomSummaryServicer):
    """Classroom service implementation."""

    def SummarizeClassroom(self, request: Classroom, context: grpc.ServicerContext) -> ClassStats:  # noqa: N802, ARG002
        """Summarize the classroom."""
        logger.info("Summarizing classroom: %s", request)
        average_grade = sum(student.avg_grade for student in request.students) / len(request.students)
        num_students = len(request.students)

        return ClassStats(grade=average_grade, numstudents=num_students)


def serve(port: int = 50051) -> None:
    """Start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ClassroomSummaryServicer_to_server(ClassroomSummary(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("Server started on port %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
