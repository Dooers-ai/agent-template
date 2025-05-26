from fastapi import UploadFile
from typing import List
from google import genai
import io
import logging

from src.settings import settings

model_client = genai.Client(api_key=settings.AI_GOOGLE_GEMINI_API_KEY)

logger = logging.getLogger("dooers-agent-template")


async def generate_title(message_text: str) -> str:
    system_prompt = f"""
    Based on the following message, generate a concise and informative title (max 6 words) that captures its main topic or intent.
    The title should be in the same language as the message.
    
    Message: {message_text}
    
    Title:
    """

    response = model_client.models.generate_content(
        model=settings.AI_GOOGLE_GEMINI_MODEL, contents=system_prompt
    )

    title = response.text.strip()

    return title


async def prepare_content(
    text: str,
    images: List[UploadFile] = None,
    videos: List[UploadFile] = None,
    audios: List[UploadFile] = None,
    documents: List[UploadFile] = None,
) -> List:
    model_content = []

    system_prompt = "You are a helpful assistant. You are given a task to help the user with their request."

    model_content.append(system_prompt)
    model_content.append(text)

    uploaded_files = []

    # google gemini requires files to be uploaded before the model be able to process them
    if images and len(images) > 0:
        for image in images:
            try:
                content = await image.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content), config=dict(mime_type=image.content_type)
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading image file: {str(e)}")

    if videos and len(videos) > 0:
        for video in videos:
            try:
                content = await video.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content), config=dict(mime_type=video.content_type)
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading video file: {str(e)}")

    if audios and len(audios) > 0:
        for audio in audios:
            try:
                content = await audio.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content), config=dict(mime_type=audio.content_type)
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading audio file: {str(e)}")

    if documents and len(documents) > 0:
        for document in documents:
            try:
                content = await document.read()
                file = model_client.files.upload(
                    file=io.BytesIO(content),
                    config=dict(mime_type=document.content_type),
                )
                uploaded_files.append(file)
            except Exception as e:
                logger.error(f"error uploading document file: {str(e)}")

    if uploaded_files:
        model_content = uploaded_files + model_content

    return model_content


async def process_content(model_content) -> str:
    response = model_client.models.generate_content(
        model=settings.AI_GOOGLE_GEMINI_MODEL, contents=model_content
    )

    response_text = response.text

    return response_text
