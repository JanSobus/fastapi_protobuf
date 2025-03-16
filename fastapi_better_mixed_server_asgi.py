"""FastApi server accepting both JSON and Protobuf requests using translating middleware."""

import json
from typing import get_type_hints

import betterproto
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRoute
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from betterproto_pb.school import Classroom, ClassStats

app = FastAPI()


class ProtobufToJsonMiddleware:
    """ASGI middleware to translate Protobuf requests to JSON."""

    start_message: Message

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the middleware with the ASGI app."""
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:  # noqa: C901
        """Call the middleware."""
        is_protobuf = False
        json_body = b""
        return_object = None

        # Define new_receive outside the if block
        async def new_receive() -> Message:
            if not is_protobuf:
                return await receive()
            return {
                "type": "http.request",
                "body": json_body,
                "more_body": False,  # Important: indicate this is the complete body
            }

        async def new_send(message: Message) -> None:
            if is_protobuf:
                if message["type"] == "http.response.start":
                    # Store the start message but don't send it yet
                    self.start_message = message
                    return
                if message["type"] == "http.response.body":
                    json_body = message["body"]
                    response_data = json.loads(json_body.decode("utf-8"))
                    proto_response = return_object(**response_data)  # type: ignore[arg-type]
                    proto_body = proto_response.SerializeToString()

                    # Preserve original headers and update only content-type and content-length
                    headers = [
                        (k, v)
                        for k, v in self.start_message["headers"]
                        if k.lower() not in [b"content-type", b"content-length"]
                    ]
                    headers.extend(
                        [
                            (b"content-length", str(len(proto_body)).encode("utf-8")),
                            (b"content-type", b"application/x-protobuf"),
                        ]
                    )

                    # Now send both messages in the correct order
                    await send({**self.start_message, "headers": headers})
                    await send(
                        {
                            "type": "http.response.body",
                            "body": proto_body,
                            "more_body": False,
                        }
                    )
                    return
            await send(message)

        if scope["type"] == "http" and scope["headers"]:
            headers_dict = dict(scope["headers"])
            content_type = headers_dict.get(b"content-type")
            if content_type and content_type == b"application/x-protobuf":
                is_protobuf = True
                # Read the body of the request
                body = b""
                more_body = True
                while more_body:
                    message = await receive()
                    body += message.get("body", b"")
                    more_body = message.get("more_body", False)
                # Determine protobuf object type
                for route in app.routes:
                    if isinstance(route, APIRoute) and route.path == scope["path"]:
                        route_func = route.endpoint
                        break
                else:
                    raise HTTPException(status_code=404, detail="Endpoint not found")
                type_hints = get_type_hints(route_func)
                return_object = type_hints.pop("return", None)
                if not return_object:
                    raise HTTPException(status_code=400, detail="Protobuf message type not found in endpoint signature")

                input_protobuf_class: betterproto.Message | None = next(
                    (hint for hint in type_hints.values() if hasattr(hint, "FromString")),
                    None,
                )
                if not input_protobuf_class:
                    raise HTTPException(status_code=400, detail="Protobuf message type not found in endpoint signature")

                # Deserialize the body into the protobuf object
                proto_object = input_protobuf_class.FromString(body)
                json_data = proto_object.to_dict(betterproto.Casing.SNAKE)  # type: ignore[arg-type]
                json_body = json.dumps(json_data).encode("utf-8")

                # Update scope headers
                scope["headers"] = [
                    (k, v) if k != b"content-type" else (k, b"application/json") for k, v in scope["headers"]
                ]

        # Always use new_send to handle both protobuf and non-protobuf cases
        await self.app(scope, new_receive, new_send)


app = FastAPI()
app.add_middleware(ProtobufToJsonMiddleware)


@app.post("/classroom")
async def summarize_classroom(classroom: Classroom) -> ClassStats:
    """Summarize the classroom."""
    return ClassStats(
        numstudents=len(classroom.students),
        grade=sum(student.avg_grade for student in classroom.students) / len(classroom.students),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
