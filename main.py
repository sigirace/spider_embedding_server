from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import RawContextMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from interface.controller.router.app_router import router as app_router


from containers import Container
from middleware.logging import RequestLoggingMiddleware

prefix = ""


def create_app():
    app = FastAPI(
        title="Spider Embedding API",
        openapi_url=f"{prefix}/openapi.json",
        docs_url=None,
        redoc_url=None,
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    )
    app.openapi_version = "3.0.3"

    app.mount(
        f"{prefix}/static",
        StaticFiles(directory="static"),
        name="static",
    )

    api_router = APIRouter(prefix=f"{prefix}")
    app.include_router(api_router)
    app.include_router(app_router, tags=["APP"])
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
    app.add_middleware(RawContextMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    container = Container()
    app.container = container

    return app


app = create_app()


@app.get("/")
async def healthcheck():
    return {"ok": True}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )


@app.get(f"{prefix}/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=f"{prefix}/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=f"{prefix}/static/swagger-ui-bundle.js",
        swagger_css_url=f"{prefix}/static/swagger-ui.css",
        swagger_favicon_url=f"{prefix}/static/img/favicon.png",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get(f"{prefix}/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url=f"{prefix}/static/img/favicon.png",
        with_google_fonts=False,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
