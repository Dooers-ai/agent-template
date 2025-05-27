# Python Agent Template - Synchronous API

A FastAPI-based agent template that integrates with Google Gemini for AI-powered message processing. This template provides a RESTful API interface with synchronous request-response communication.

## Overview

This agent template is designed to handle AI conversations through a structured API that follows specific data models expected by frontend applications. The API supports multimodal inputs (text, images, videos, audio, documents) and returns structured responses through Google Gemini integration.

## API Structure

The API is organized with the following base URL pattern:
- **Base URL:** `/api/v1`
- **Documentation:** Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

## API Endpoints

### Message Processing

#### `POST /api/v1/messages`

Process a message through the AI agent and return a complete response.

**Request Format:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id_team_agent` | string | Yes | Unique identifier for the team agent |
| `id_team` | string | Yes | Team identifier |
| `id_task` | string | No | Task identifier where the message belongs (optional for new tasks) |
| `text` | string | Yes | The message text content |
| `images` | File[] | No | Array of image files |
| `videos` | File[] | No | Array of video files |
| `audios` | File[] | No | Array of audio files |
| `documents` | File[] | No | Array of document files |

**Response:** `MessageResponse` object

### Task Management

#### `GET /api/v1/tasks/{id_team_agent}`

List all tasks for a specific team agent.

**Parameters:**
- `id_team_agent` (path): Unique identifier for the team agent

**Response:** Array of `Task` objects

#### `GET /api/v1/tasks/{id_team_agent}/{id_task}`

Retrieve a specific task by ID.

**Parameters:**
- `id_team_agent` (path): Unique identifier for the team agent
- `id_task` (path): Task identifier

**Response:** `Task` object

#### `POST /api/v1/tasks/{id_team_agent}`

Create a new task.

**Parameters:**
- `id_team_agent` (path): Unique identifier for the team agent

**Request Format:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id_team` | string | Yes | Team identifier |
| `text` | string | Yes | Initial message text for the task |

**Response:** `Task` object

#### `DELETE /api/v1/tasks/{id_team_agent}/{id_task}`

Delete a specific task.

**Parameters:**
- `id_team_agent` (path): Unique identifier for the team agent
- `id_task` (path): Task identifier

**Response:** Success/error status

```json
{
  "status": "success",
  "message": "task deleted"
}
```

### Settings Management

#### `GET /api/v1/settings/{id_team_agent}`

Retrieve settings configuration for a specific team agent.

**Parameters:**
- `id_team_agent` (path): Unique identifier for the team agent

**Response:** `Settings` object with form configuration

#### `POST /api/v1/settings/{id_team_agent}`

Synchronize/update settings for a specific team agent.

**Parameters:**
- `id_team_agent` (path): Unique identifier for the team agent

**Request Format:** `multipart/form-data`

**Response:** Updated `Settings` object

## Message Chunk Events

The API supports various message chunk events for streaming responses:

| Event | Description |
|-------|-------------|
| `started` | Message processing has started |
| `text-chunk` | Text content chunk |
| `reasoning-chunk` | Reasoning content chunk |
| `image-chunk` | Image content chunk |
| `video-chunk` | Video content chunk |
| `audio-chunk` | Audio content chunk |
| `document-chunk` | Document content chunk |
| `step` | Processing step information |
| `loading` | Loading progress indicator |
| `finished` | Message processing completed |
| `error` | Error occurred during processing |
| `interrupted` | Processing was interrupted |

## Data Models

### MessageRequest

Represents a message sent to the agent.

```json
{
  "id_team_agent": "string",
  "id_team": "string", 
  "id_task": "string (optional)",
  "text": "string",
  "images": [
    {
      "name": "string",
      "type": "image",
      "size": "number (optional)",
      "base64": "string (optional)",
      "url": "string (optional)",
      "mime_type": "string (optional)"
    }
  ],
  "videos": [
    {
      "name": "string",
      "type": "video",
      "size": "number (optional)",
      "base64": "string (optional)",
      "url": "string (optional)",
      "mime_type": "string (optional)"
    }
  ],
  "audios": [
    {
      "name": "string",
      "type": "audio",
      "size": "number (optional)",
      "base64": "string (optional)",
      "url": "string (optional)",
      "mime_type": "string (optional)"
    }
  ],
  "documents": [
    {
      "name": "string",
      "type": "document",
      "size": "number (optional)",
      "base64": "string (optional)",
      "url": "string (optional)",
      "mime_type": "string (optional)"
    }
  ]
}
```

### MessageResponse

Represents the agent's response to a message.

```json
{
  "id_team_agent": "string",
  "id_team": "string",
  "id_task": "string",
  "created_at": "string (ISO timestamp)",
  "text": "string",
  "reasoning": "string (optional)",
  "images": [
    {
      "name": "string",
      "type": "image",
      "size": "number (optional)",
      "base64": "string (optional)",
      "url": "string (optional)",
      "mime_type": "string (optional)"
    }
  ],
  "videos": "array (optional)",
  "audios": "array (optional)",
  "documents": "array (optional)",
  "event": "string (optional)",
  "is_finished": "boolean (optional)",
  "is_error": "boolean (optional)",
  "is_interrupted": "boolean (optional)",
  "error": "string (optional)",
  "reason": "string (optional)"
}
```

### Task

Represents a conversation task containing multiple message exchanges.

```json
{
  "id_task": "string",
  "id_team_agent": "string",
  "id_team": "string",
  "title": "string",
  "content": [
    {
      "request": "MessageRequest object",
      "response": "MessageResponse object (optional)"
    }
  ],
  "driver": "auto | agent | user",
  "created_at": "string (ISO timestamp)",
  "updated_at": "string (ISO timestamp)"
}
```

### Thread

Represents a single exchange within a task.

```json
{
  "request": "MessageRequest object",
  "response": "MessageResponse object (optional)"
}
```

### Settings

Represents the configuration settings for an agent, organized in form categories.

```json
{
  "version": "string",
  "categories": [
    {
      "id": "string",
      "label": "string",
      "order": "number",
      "is_collapsed": "boolean",
      "fields": [
        {
          "id": "string",
          "element": "input | textarea | select | image | image-input | button",
          "label": "string",
          "required": "boolean",
          "readonly": "boolean",
          // Additional properties based on element type
        }
      ]
    }
  ]
}
```

### Form Fields

The settings system supports various form field types:

#### InputField
```json
{
  "element": "input",
  "type": "text | password | email | tel | checkbox | file | number | date",
  "placeholder": "string (optional)",
  "value": "string (optional)",
  "checked": "boolean (optional)",
  "accept": "string (optional)",
  "min": "number | string (optional)",
  "max": "number | string (optional)",
  "step": "number (optional)",
  "maxlength": "number (optional)",
  "align": "left | center | right (optional)"
}
```

#### TextareaField
```json
{
  "element": "textarea",
  "placeholder": "string (optional)",
  "value": "string (optional)",
  "rows": "number (optional)",
  "cols": "number (optional)",
  "maxlength": "number (optional)"
}
```

#### SelectField
```json
{
  "element": "select",
  "options": [
    {
      "value": "string",
      "label": "string"
    }
  ],
  "value": "string (optional)",
  "multiple": "boolean (optional)"
}
```

#### ImageField
```json
{
  "element": "image",
  "src": "string",
  "format": "base64 | url",
  "alt": "string (optional)",
  "width": "number",
  "height": "number",
  "align": "left | center | right (optional)"
}
```

#### ButtonField
```json
{
  "element": "button",
  "label": "string",
  "style": "solid | outline (optional)",
  "variant": "primary | secondary (optional)"
}
```

### Media Objects

All media objects (images, videos, audios, documents) follow this structure:

```json
{
  "name": "string",
  "type": "image | video | audio | document",
  "size": "number (optional)",
  "base64": "string (optional)",
  "url": "string (optional)",
  "mime_type": "string (optional)"
}
```

## Environment Configuration

Create a `.env` file with the following variables:

```env
# Application Settings
APP_TITLE=dooers-agent-template-python-sync
APP_DESCRIPTION=dooers-agent-template-python-sync
APP_VERSION=0.1.0
APP_ENV=DEVELOPMENT

# Web Server
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8000

# CORS Configuration
WEB_SERVER_CORS_ORIGINS=*
WEB_SERVER_CORS_CREDENTIALS=false
WEB_SERVER_CORS_METHODS=*
WEB_SERVER_CORS_HEADERS=*

# Security Settings
WEB_SERVER_TRUSTED_HOSTS=*
WEB_SERVER_ENFORCE_HTTPS=false

# Google Gemini API
AI_GOOGLE_GEMINI_API_KEY=your_api_key_here
AI_GOOGLE_GEMINI_MODEL=gemini-2.0-flash
```

## Installation and Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv sync
   ```

2. **Configure environment variables:**
   - Copy `.env.default` to `.env`
   - Set your Google Gemini API key

3. **Run the application:**
   ```bash
   python -m src.main
   # or with uv
   uv run python -m src.main
   ```

The API will be available at `http://localhost:8000`

## Server Configuration

The application includes several middleware components:

- **CORS Middleware**: Configurable cross-origin resource sharing
- **GZip Middleware**: Response compression for better performance
- **Trusted Host Middleware**: Security layer for allowed hosts (when configured)
- **HTTPS Redirect Middleware**: Automatic HTTPS redirection (when enabled)

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

The API follows OpenAPI 3.0 specification and provides comprehensive documentation for all endpoints, request/response models, and error codes.


## Key Features

- **Multimodal Support**: The API accepts files alongside text messages (images, videos, audio, documents)
- **Task Management**: Complete CRUD operations for conversation tasks
- **Settings Configuration**: Dynamic form-based settings management with various field types
- **Structured Responses**: All responses follow consistent data models
- **Error Handling**: Comprehensive error handling with detailed error responses
- **CORS Support**: Configurable CORS settings for cross-origin requests
- **Security Features**: Trusted hosts and HTTPS enforcement options
- **API Documentation**: Auto-generated Swagger UI and ReDoc documentation

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `201`: Created (for new tasks)
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Error responses include details in the standard `MessageResponse` format with `is_error: true`.

