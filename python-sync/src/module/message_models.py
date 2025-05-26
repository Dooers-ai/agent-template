from pydantic import BaseModel
from typing import List, Optional, Literal, Union


class Image(BaseModel):
    name: str
    type: Literal["image"]
    size: Optional[int] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None


class Video(BaseModel):
    name: str
    type: Literal["video"]
    size: Optional[int] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None


class Audio(BaseModel):
    name: str
    type: Literal["audio"]
    size: Optional[int] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None


class Document(BaseModel):
    name: str
    type: Literal["document"]
    size: Optional[int] = None
    base64: Optional[str] = None
    url: Optional[str] = None
    mime_type: Optional[str] = None


MessageChunkEvent = Literal[
    "started",
    "text-chunk",
    "reasoning-chunk",
    "image-chunk",
    "video-chunk",
    "audio-chunk",
    "document-chunk",
    "step",
    "loading",
    "finished",
    "error",
    "interrupted",
]


class MessageChunkStarted(BaseModel):
    event: Literal["started"]
    id_team_agent: str
    id_team: str
    id_task: str
    created_at: str


class MessageChunkText(BaseModel):
    event: Literal["text-chunk"]
    content: str


class MessageChunkReasoning(BaseModel):
    event: Literal["reasoning-chunk"]
    content: str


class MessageChunkImage(BaseModel):
    event: Literal["image-chunk"]
    name: str
    is_base64: bool
    is_url: bool
    mime_type: str
    content: str


class MessageChunkVideo(BaseModel):
    event: Literal["video-chunk"]
    name: str
    is_base64: bool
    is_url: bool
    mime_type: str
    content: str


class MessageChunkAudio(BaseModel):
    event: Literal["audio-chunk"]
    name: str
    is_base64: bool
    is_url: bool
    mime_type: str
    content: str


class MessageChunkDocument(BaseModel):
    event: Literal["document-chunk"]
    name: str
    is_base64: bool
    is_url: bool
    mime_type: str
    content: str


class MessageChunkStep(BaseModel):
    event: Literal["step"]
    step: int
    content: str


class MessageChunkLoading(BaseModel):
    event: Literal["loading"]
    progress: Optional[int] = None


class MessageChunkFinished(BaseModel):
    event: Literal["finished"]


class MessageChunkError(BaseModel):
    event: Literal["error"]
    error: str


class MessageChunkInterrupted(BaseModel):
    event: Literal["interrupted"]
    reason: str


MessageChunk = Union[
    MessageChunkStarted,
    MessageChunkText,
    MessageChunkReasoning,
    MessageChunkImage,
    MessageChunkVideo,
    MessageChunkAudio,
    MessageChunkDocument,
    MessageChunkStep,
    MessageChunkLoading,
    MessageChunkFinished,
    MessageChunkError,
    MessageChunkInterrupted,
]


class MessageRequest(BaseModel):
    id_team_agent: str
    id_team: str
    id_task: Optional[str] = None
    text: str
    images: Optional[List[Image]] = None
    videos: Optional[List[Video]] = None
    audios: Optional[List[Audio]] = None
    documents: Optional[List[Document]] = None


class MessageResponse(BaseModel):
    id_team_agent: str
    id_team: str
    id_task: str
    created_at: str
    text: str
    reasoning: Optional[str] = None
    images: Optional[List[Image]] = None
    videos: Optional[List[Video]] = None
    audios: Optional[List[Audio]] = None
    documents: Optional[List[Document]] = None
    event: Optional[MessageChunkEvent] = None
    is_finished: Optional[bool] = None
    is_error: Optional[bool] = None
    is_interrupted: Optional[bool] = None
    error: Optional[str] = None
    reason: Optional[str] = None


# settings schema


class SelectOption(BaseModel):
    value: str
    label: str


class BaseField(BaseModel):
    id: str
    element: Literal["input", "textarea", "select", "image", "image-input", "button"]
    label: str
    required: bool = False
    readonly: bool = False


class InputField(BaseField):
    element: Literal["input"]
    type: Literal[
        "text", "password", "email", "tel", "checkbox", "file", "number", "date"
    ]
    placeholder: Optional[str] = None
    value: Optional[str] = None
    checked: Optional[bool] = None
    accept: Optional[str] = None
    min: Optional[Union[int, str]] = None
    max: Optional[Union[int, str]] = None
    step: Optional[int] = None
    maxlength: Optional[int] = None
    align: Optional[Literal["left", "center", "right"]] = None


class TextareaField(BaseField):
    element: Literal["textarea"]
    placeholder: Optional[str] = None
    value: Optional[str] = None
    rows: Optional[int] = None
    cols: Optional[int] = None
    maxlength: Optional[int] = None


class SelectField(BaseField):
    element: Literal["select"]
    options: List[SelectOption]
    value: Optional[str] = None
    multiple: Optional[bool] = None


class ImageField(BaseField):
    element: Literal["image"]
    src: str
    format: Literal["base64", "url"]
    alt: Optional[str] = None
    width: int
    height: int
    align: Optional[Literal["left", "center", "right"]] = None


class ImageInputField(BaseField):
    element: Literal["image-input"]
    value: Optional[str] = None
    format: Literal["base64", "url"]
    alt: Optional[str] = None
    width: int
    height: int
    align: Optional[Literal["left", "center", "right"]] = None


class ButtonField(BaseField):
    element: Literal["button"]
    label: str
    style: Optional[Literal["solid", "outline"]] = None
    variant: Optional[Literal["primary", "secondary"]] = None


FormField = Union[
    InputField, TextareaField, SelectField, ImageField, ImageInputField, ButtonField
]


class FormCategory(BaseModel):
    id: str
    label: str
    order: int
    is_collapsed: bool
    fields: List[FormField]


class Settings(BaseModel):
    version: str
    categories: List[FormCategory]
