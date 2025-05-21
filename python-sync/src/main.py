import uvicorn

from src.common.helpers import logger
from src.common.exceptions import ServerException
from src.infra.web_server import create_server
from src.settings import settings

app = create_server()


def run_server():
    try:
        logger.info(f"{settings.APP_TITLE} {settings.APP_VERSION} - {settings.APP_ENV}")
        logger.info("http web server service started")
        uvicorn.run(
            "src.main:app",
            host=settings.WEB_SERVER_HOST,
            port=settings.WEB_SERVER_PORT,
            reload=settings.IS_DEVELOPMENT,
            reload_dirs=["src"] if settings.IS_DEVELOPMENT else None,
            reload_delay=1 if settings.IS_DEVELOPMENT else None,
            log_level="debug" if settings.IS_DEVELOPMENT else "info",
        )
        logger.info("http web server service stopped")
    except Exception as err:
        logger.error(f"error starting http web server: {err}")
        raise ServerException(
            "INTERNAL_SERVER_ERROR", 500, "Application error", str(err)
        )


if __name__ == "__main__":
    try:
        run_server()
    except Exception as err:
        logger.error(f"application error: {err}")
