from fastapi import FastAPI, APIRouter, Response, Request
from typing import Callable

from app.cmd.di.container import Container


def create_router( container:Container )->FastAPI:
    
    app = FastAPI(debug=True)
    from fastapi.exceptions import RequestValidationError
    import logging
    import traceback
    logger = logging.getLogger("uvicorn.error")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        from fastapi.responses import JSONResponse
        body = await request.body()
        tb = "".join(traceback.format_exception(None, exc, exc.__traceback__))
        logger.error(
            "ValidationError on %s %s\nBody: %s\nErrors: %s\nTraceback:\n%s",
            request.method,
            request.url.path,
            body.decode(errors="replace"),
            exc.errors(),
            tb,
        )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    set_api_route( router=app, path="/auth", endpoint=container.auth_controller.test, methods=["GET"])
    set_api_route( router=app, path="/users/register", endpoint=container.auth_controller.create, methods=["POST"], response_hook=set_auth_cookie)
    
    return app


def set_api_route(
    router: APIRouter,
    path: str,
    endpoint: Callable,
    methods: list[str],
    response_hook: Callable | None = None,
):
    import inspect
    from pydantic import BaseModel, ValidationError
    from fastapi import Request
    from fastapi.exceptions import RequestValidationError

    async def wrapper(
        response: Response,
        request: Request,
    ):
        sig = inspect.signature(endpoint)
        call_kwargs = {}

        for name, param in sig.parameters.items():
            # skip bound 'self' if present
            if name == "self":
                continue

            ann = param.annotation
            # If the endpoint expects a Pydantic model, parse the incoming body
            if inspect.isclass(ann) and issubclass(ann, BaseModel):
                body_bytes = await request.body()
                try:
                    model_instance = ann.parse_raw(body_bytes or b"{}")
                except ValidationError as e:  # pydantic validation error
                    raise RequestValidationError(e.errors())
                call_kwargs[name] = model_instance
            # If the endpoint explicitly wants the Request, pass it through
            elif ann is Request:
                call_kwargs[name] = request

        # include any path params and query params
        call_kwargs.update(request.path_params)
        call_kwargs.update(dict(request.query_params))

        result = await endpoint(**call_kwargs)

        if response_hook:
            response_hook(
                response=response,
                result=result,
            )

        return result

    router.add_api_route(
        path,
        wrapper,
        methods=methods,
    )

def set_auth_cookie( response: Response, result)-> None:

    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
