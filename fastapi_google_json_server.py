"""FastAPI server for Google protobuf messages with JSON serialization."""

import uvicorn
from fastapi import FastAPI

from fastapi_google_json_models import Classroom, ClassStats

app = FastAPI()


@app.post("/classroom")
async def summarize_classroom(classroom: Classroom) -> ClassStats:
    """Summarize the classroom."""
    avg_grade = sum(student.avg_grade for student in classroom.students) / len(classroom.students)
    return ClassStats(numstudents=len(classroom.students), grade=avg_grade)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
