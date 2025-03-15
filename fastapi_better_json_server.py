"""Server implementation for FastAPI using betterproto JSON serialization."""

import uvicorn
from fastapi import FastAPI

from betterproto_pb.school import Classroom, ClassStats

app = FastAPI()


@app.post("/classroom")
async def summarize_classroom(classroom: Classroom) -> ClassStats:
    """Summarize the classroom."""
    return ClassStats(
        numstudents=len(classroom.students),
        grade=sum(student.avg_grade for student in classroom.students) / len(classroom.students),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
