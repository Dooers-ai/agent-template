from typing import Dict, Any

from src.settings import settings
from src.common.common_models import Status, StatusOutputDTO
from src.common.constants import StatusCodes

STATUS_LIST: Dict[str, Dict[str, Any]] = {
    "1xx": {
        "type": "INFORMATION",
        "name": {
            100: "CONTINUE",
            101: "SWITCHING_PROTOCOL",
            102: "PROCESSING",
            103: "EARLY_HINTS",
        },
    },
    "2xx": {
        "type": "SUCCESS",
        "name": {
            200: "OK",
            201: "CREATED",
            202: "ACCEPTED",
            204: "NO_CONTENT",
        },
    },
    "3xx": {
        "type": "REDIRECTION",
        "name": {
            300: "MULTIPLE_CHOICE",
            301: "MOVED_PERMANENTLY",
            302: "FOUND",
            303: "SEE_OTHER",
            304: "NOT_MODIFIED",
            307: "TEMPORARY_REDIRECT",
            308: "PERMANENT_REDIRECT",
        },
    },
    "4xx": {
        "type": "CLIENT_ERROR",
        "name": {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            402: "PAYMENT_REQUIRED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            406: "NOT_ACCEPTABLE",
            407: "PROXY_AUTHENTICATION_REQUIRED",
            408: "REQUEST_TIMEOUT",
            409: "CONFLICT",
            410: "GONE",
            411: "LENGTH_REQUIRED",
            412: "PRECONDITION_FAILED",
            413: "PAYLOAD_TOO_LARGE",
            414: "URI_TOO_LONG",
            415: "UNSUPPORTED_MEDIA_TYPE",
            416: "RANGE_NOT_SATISFIABLE",
            417: "EXPECTATION_FAILED",
            418: "IM_A_TEAPOT",
            419: "AUTHENTICATION_TIMEOUT",
            426: "UPGRADE_REQUIRED",
            428: "PRECONDITION_REQUIRED",
            429: "TOO_MANY_REQUESTS",
        },
    },
    "5xx": {
        "type": "SERVER_ERROR",
        "name": {
            500: "INTERNAL_SERVER_ERROR",
            501: "NOT_IMPLEMENTED",
            502: "BAD_GATEWAY",
            503: "SERVICE_UNAVAILABLE",
            504: "GATEWAY_TIMEOUT",
        },
    },
}


def get_status_category_code(code: int) -> str:
    if 100 <= code < 200:
        return "1xx"
    if 200 <= code < 300:
        return "2xx"
    if 300 <= code < 400:
        return "3xx"
    if 400 <= code < 500:
        return "4xx"
    if 500 <= code < 600:
        return "5xx"
    return "unknown"


def get_status_category_info(code: StatusCodes) -> Dict[str, str]:
    category = get_status_category_code(code)
    category_info = STATUS_LIST.get(category, {})

    return {
        "type": category_info.get("type", "SERVER_ERROR"),
        "name": category_info.get("name", {}).get(code, "UNKNOWN_STATUS_NAME"),
    }


def create_status(status: Status) -> StatusOutputDTO:
    code = status.code or StatusCodes.INTERNAL_SERVER_ERROR
    description = status.description
    category_info = get_status_category_info(code)

    response: Dict[str, Any] = {
        "type": status.type or category_info["type"],
        "name": status.name or category_info["name"],
        "description": description,
        "code": code,
        "is_error": status.is_error or False,
    }

    if settings.IS_DEVELOPMENT:
        if status.message is not None:
            response["message"] = status.message
        if status.detail is not None:
            response["detail"] = status.detail
        if status.scope is not None:
            response["scope"] = status.scope

    return StatusOutputDTO(**response)
