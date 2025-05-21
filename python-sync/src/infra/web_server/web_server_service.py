from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from src.settings import settings
from src.common.helpers import logger
from src.infra.web_server.web_server_routes import router


def create_server() -> FastAPI:
    server = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )

    server.add_middleware(
        CORSMiddleware,
        allow_origins=settings.WEB_SERVER_CORS_ORIGINS,
        allow_credentials=settings.WEB_SERVER_CORS_CREDENTIALS,
        allow_methods=settings.WEB_SERVER_CORS_METHODS,
        allow_headers=settings.WEB_SERVER_CORS_HEADERS,
    )

    server.add_middleware(GZipMiddleware)

    if settings.WEB_SERVER_TRUSTED_HOSTS and settings.WEB_SERVER_TRUSTED_HOSTS != ["*"]:
        server.add_middleware(
            TrustedHostMiddleware, allowed_hosts=settings.WEB_SERVER_TRUSTED_HOSTS
        )

    if settings.WEB_SERVER_ENFORCE_HTTPS:
        server.add_middleware(HTTPSRedirectMiddleware)

    @server.exception_handler(Exception)
    async def server_exception_handler(request: Request, exc: Exception):
        logger.error(f"unhandled exception: {exc}", exc_info=True)

    server.include_router(router)

    return server
