from fastapi import UploadFile
from typing import Dict
import logging
import os
import json

settings_table: Dict[str, dict] = {}

logger = logging.getLogger("dooers-agent-template")


def load_schema_from_file() -> list:
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "settings.json"
    )
    with open(template_path, "r") as f:
        schema = json.load(f)
    return schema


async def read_settings_service(id_team_agent: str) -> dict:
    settings_schema = load_schema_from_file()
    settings = settings_table.get(id_team_agent)

    if not settings["values"]:
        settings = await create_settings_service(id_team_agent)

    settings_output = {"schema": settings_schema, "values": settings["values"]}

    logger.info(f"settings read {id_team_agent}")

    return settings_output


async def create_settings_service(id_team_agent: str) -> dict:
    settings = {"id_team_agent": id_team_agent, "values": {}}
    settings_table[id_team_agent] = settings
    logger.info(f"settings created {id_team_agent}")

    return settings


async def sync_settings_service(id_team_agent: str, form_data: dict) -> dict:
    for field_name, field_value in form_data.items():
        if isinstance(field_value, UploadFile):
            logger.info(
                f" settings_input: {field_name} → File: {field_value.filename or '(empty)'}"
            )
        else:
            logger.info(f" settings_input: {field_name} → {field_value}")

    settings_table[id_team_agent] = form_data
    logger.info(f"settings synced {id_team_agent}")

    return await read_settings_service(id_team_agent)
