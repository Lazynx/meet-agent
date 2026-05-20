# Meeting Protocol AI Agent (Google ADK)

An automated agent for meeting documentation (Teams/Zoom/Meet → Notion/Telegram).  
The agent receives a meeting audio recording, performs transcription, analyzes speech, structures the data, and automatically generates a report with tasks, decisions, and key highlights.

---

## Features

- **Automatic transcription** via **Google Speech-to-Text** with speaker diarization
- **LLM analysis** using **Google Gemini 2.0 Flash** (via Google ADK)
- **Notion page creation** with topics, decisions, and tasks
- **Telegram report delivery** (PDF + brief summary)
- **Automatic error notifications** via Telegram
- Supported **audio formats:** `.m4a`, `.mp3`, `.wav`, etc.
- **GCP integration (Google Cloud Storage)** for audio file storage and transfer

---

## Tech Stack

| Component                | Technology                          |
| ------------------------ | ----------------------------------- |
| Agent framework          | Google ADK (Agents Development Kit) |
| LLM / Analysis           | Gemini 2.0 Flash                    |
| ASR (Speech Recognition) | Google Speech-to-Text API           |
| Storage                  | Google Cloud Storage (GCS)          |
| Backend                  | FastAPI                             |
| PDF generation           | ReportLab                           |
| Integrations             | Aiogram (Telegram), Notion API      |
| Containerization         | Docker & Docker Compose             |

---

## Local Setup

### Prerequisites

- Docker & Docker Compose
- Google Cloud credentials (with access to Speech-to-Text and GCS)
- Telegram bot token
- Notion integration API key and parent page ID

### Installation & Run

```bash
docker compose build
docker compose up -d
```

The service will be available at `http://localhost:8000`

Upload an audio file via the API or web interface. The agent will automatically:

1. Convert audio to WAV (16kHz mono)
2. Upload to GCS
3. Obtain a `gs://` URI
4. Transcribe speech via Google Speech-to-Text
5. Pass the transcript to Gemini for analysis and structuring
6. Generate a PDF report and send it to Telegram with a brief summary
7. Create a Notion page with the meeting results

On any error, Telegram receives a notification with the error stage and message.

---

## Example `meeting_data` JSON

```json
{
  "meeting_type": "team_meeting",
  "participants": {
    "active_speakers": [
      {"name": "Aruzhan", "speaker_id": 0},
      {"name": "Vlad", "speaker_id": 1}
    ],
    "mentioned": ["Artem", "Daniyar"]
  },
  "summary": {
    "title": "Weekly task sync",
    "topics": [
      {"title": "Backend", "description": "Push service integration", "speakers": ["Vlad"]}
    ],
    "decisions": [
      {"description": "Add retries and logging for push service", "context": "Notification delivery failures"}
    ],
    "key_points": ["Push notification stability needs improvement"]
  },
  "tasks": [
    {
      "title": "Push service integration",
      "description": "Finalize push service and add logging",
      "assignee": "Artem",
      "deadline": "2025-10-15",
      "priority": "high"
    }
  ]
}
```

---

## Processing Flow

1. User sends an audio file (`.m4a`, `.mp3`, etc.) — the API converts it to `.wav` and returns a GCS URI
2. User sends the URI to the agent
3. Google Speech-to-Text performs speech recognition with speaker diarization
4. Gemini analyzes the transcript and extracts topics, decisions, and tasks
5. A Notion page is created with structured meeting data
6. A PDF report is generated and sent to Telegram with a summary