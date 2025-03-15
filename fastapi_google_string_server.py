"""FastAPI server using Google protobuf string serialization."""

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response

from google_pb.messages_pb2 import Classroom, ClassStats

app = FastAPI()


@app.post("/classroom")
async def summarize_classroom(request: Request) -> Response:
    """Summarize the classroom."""
    try:
        classroom_string: bytes = await request.body()
        classroom = Classroom.FromString(classroom_string)
        avg_grade = sum(student.avg_grade for student in classroom.students) / len(classroom.students)
        classroom_stats_object = ClassStats(numstudents=len(classroom.students), grade=avg_grade)
        classroom_stats_string = classroom_stats_object.SerializeToString()
        return Response(status_code=200, content=classroom_stats_string)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Exception: {e!s}") from e


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
