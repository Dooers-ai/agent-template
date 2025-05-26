from pydantic import BaseModel
from typing import List, Optional, Literal, Union


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
