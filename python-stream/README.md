# Python Agent Template - Streaming API

A FastAPI-based agent template that integrates with Google Gemini for AI-powered message processing. This template provides a RESTful API interface with **real-time streaming** communication using Server-Sent Events (SSE).

## Overview

This agent template is designed to handle AI conversations through a structured API that follows specific data models expected by frontend applications. The API supports multimodal inputs (text, images, videos, audio, documents) and returns structured responses through Google Gemini integration with **real-time streaming capabilities**.

## API Endpoints

### Message Processing (Streaming)

#### `POST /messages`

Process a message through the AI agent and return a **streaming response** using Server-Sent Events.

**Request Format:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id_team_agent` | string | Yes | Unique identifier for the team agent |
| `id_team` | string | Yes | Team identifier |
| `id_task` | string | Yes | Task identifier where the message belongs |
| `text` | string | Yes | The message text content |
| `images` | File[] | No | Array of image files |
| `videos` | File[] | No | Array of video files |
| `audios` | File[] | No | Array of audio files |
| `documents` | File[] | No | Array of document files |

**Headers:**
- `Accept: text/event-stream` (Required for streaming)

**Response:** Server-Sent Event stream of `MessageChunk` objects

**Stream Format:**
```
data: {"event": "started", "id_team_agent": "...", "id_team": "...", "id_task": "...", "created_at": "..."}

data: {"event": "text-chunk", "content": "Hello"}

data: {"event": "text-chunk", "content": " world!"}

data: {"event": "finished"}

data: [DONE]
```

### Task Management

#### `GET /tasks/{id_team_agent}`

List all tasks for a specific team agent.

**Response:** Array of `Task` objects

#### `GET /tasks/{id_team_agent}/{id_task}`

Retrieve a specific task by ID.

**Response:** `Task` object

#### `POST /tasks/{id_team_agent}`

Create a new task.

**Request Format:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id_team` | string | Yes | Team identifier |
| `text` | string | Yes | Initial message text for the task |

**Response:** `Task` object

#### `DELETE /tasks/{id_team_agent}/{id_task}`

Delete a specific task.

**Response:** Success/error status

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

Represents the agent's response to a message (used for task storage after streaming completes).

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

### Streaming Event Models

#### MessageChunkStarted
```json
{
  "event": "started",
  "id_team_agent": "string",
  "id_team": "string",
  "id_task": "string",
  "created_at": "string (ISO timestamp)"
}
```

#### MessageChunkText
```json
{
  "event": "text-chunk",
  "content": "string"
}
```

#### MessageChunkReasoning
```json
{
  "event": "reasoning-chunk",
  "content": "string"
}
```

#### MessageChunkImage
```json
{
  "event": "image-chunk",
  "name": "string",
  "is_base64": "boolean",
  "is_url": "boolean",
  "mime_type": "string",
  "content": "string"
}
```

#### MessageChunkVideo
```json
{
  "event": "video-chunk",
  "name": "string",
  "is_base64": "boolean",
  "is_url": "boolean",
  "mime_type": "string",
  "content": "string"
}
```

#### MessageChunkAudio
```json
{
  "event": "audio-chunk",
  "name": "string",
  "is_base64": "boolean",
  "is_url": "boolean",
  "mime_type": "string",
  "content": "string"
}
```

#### MessageChunkDocument
```json
{
  "event": "document-chunk",
  "name": "string",
  "is_base64": "boolean",
  "is_url": "boolean",
  "mime_type": "string",
  "content": "string"
}
```

#### MessageChunkStep
```json
{
  "event": "step",
  "step": "number",
  "content": "string"
}
```

#### MessageChunkLoading
```json
{
  "event": "loading",
  "progress": "number (optional)"
}
```

#### MessageChunkFinished
```json
{
  "event": "finished"
}
```

#### MessageChunkError
```json
{
  "event": "error",
  "error": "string"
}
```

#### MessageChunkInterrupted
```json
{
  "event": "interrupted",
  "reason": "string"
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

## Environment Configuration

Create a `.env` file with the following variables:

```env
# Application Settings
APP_TITLE=dooers-agent-template-python-stream
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

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


### Key Integration Points

- **Real-time Streaming**: Responses are delivered as they're generated
- **Event-based Architecture**: Different event types for different content
- **Multimodal Support**: The API accepts files alongside text messages
- **Task Persistence**: Conversations are automatically saved to tasks after streaming
- **Structured Responses**: All events follow the expected data models
- **Error Handling**: Errors are streamed as events in real-time

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success (including streaming responses)
- `201`: Created (for new tasks)
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Streaming errors are delivered as `MessageChunkError` events within the stream, allowing for real-time error feedback.

## Streaming vs Synchronous

This template implements **streaming-only** communication for the `/messages` endpoint. Unlike the synchronous version:

- Responses are delivered in real-time as they're generated
- Frontend can display content progressively
- Better user experience for long-running AI responses
- Requires Server-Sent Events support in the frontend
- Must include `Accept: text/event-stream` header for message processing

