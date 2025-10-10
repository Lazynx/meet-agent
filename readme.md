# Meeting Protocol AI Agent (Google ADK)

Автоматизированный агент для протоколирования встреч (Teams/Zoom/Meet → Notion/TG).
Агент принимает аудиозапись встречи, выполняет транскрипцию, анализирует речь, структурирует данные и автоматически формирует отчет с задачами, решениями и ключевыми моментами.

---

## Основные возможности

* **Автоматическая транскрипция** аудио при помощи **Google Speech-to-Text**
* **LLM-анализ** с помощью **Google Gemini** (через Google ADK)
* **Создание страницы** встречи в **Notion** с темами, решениями и задачами
* **Отправка отчета в Telegram** (PDF + краткое summary)
* **Автоматическое уведомление об ошибках** в Telegram
* Поддержка **форматов аудио:** `.m4a`, `.mp3`, `.wav` и др.
* **Интеграция с GCP (Google Cloud Storage)** для хранения и передачи аудиофайлов

---

## Стек технологий

| Компонент                | Технология                          |
| ------------------------ | ----------------------------------- |
| Агентный фреймворк       | Google ADK (Agents Development Kit) |
| LLM / Анализ             | Gemini 2.0 Flash                    |
| ASR (Speech Recognition) | Google Speech-to-Text API           |
| Хранилище                | Google Cloud Storage (GCS)          |
| Backend                  | FastAPI                             |
| Формирование PDF         | ReportLab                           |
| Интеграции               | Aiogram API, Notion API             |
| Контейнеризация          | Docker & Docker Compose             |

---

## Локальный запуск

### Требования

* Docker & Docker Compose
* Google Cloud credentials (с доступом к Speech-to-Text и GCS)
* Токен Telegram-бота
* Notion интеграция с API key и parent page ID

### Установка и запуск

```bash
docker compose build
docker compose up -d
```

После запуска сервис будет доступен локально по адресу: `http://localhost:8000`

Загрузите аудиофайл через API или веб-интерфейс. Агент автоматически:

1. Конвертирует аудио в WAV (16kHz mono)
2. Загружает в GCS
3. Получает `gs://` URI
4. Транскрибирует речь через Google Speech-to-Text
5. Передает результат в Gemini для анализа и структурирования
6. Генерирует PDF-отчет и отправляет его в Telegram
7. Создает страницу в Notion с результатами встречи

При ошибке на любом этапе — Telegram получит уведомление с кодом ошибки.

---

## Пример JSON-структуры `meeting_data`

```json
{
  "meeting_type": "team_meeting",
  "participants": {
    "active_speakers": [
      {"name": "Аружан", "speaker_id": 0},
      {"name": "Влад", "speaker_id": 1}
    ],
    "mentioned": ["Артем", "Данияр"]
  },
  "summary": {
    "title": "Синк по задачам на неделю",
    "topics": [
      {"title": "Backend", "description": "Интеграция push-сервиса", "speakers": ["Влад"]}
    ],
    "decisions": [
      {"description": "Добавить ретраи и логирование для push-сервиса", "context": "Ошибка доставки уведомлений"}
    ],
    "key_points": ["Необходимо улучшить стабильность push-уведомлений"]
  },
  "tasks": [
    {
      "title": "Интеграция push-сервиса",
      "description": "Доработать push-сервис и логирование",
      "assignee": "Артем",
      "deadline": "2025-10-15",
      "priority": "high"
    }
  ]
}
```

---

## Пример флоу работы

1. Пользователь отправляет аудиофайл (`.m4a`, `.mp3` и т.д.) в API он его трансформирует в .wav и получает GCS uri
2. Пользователь отправляет uri в агента
3. Google Speech-to-Text выполняет распознавание речи
4. Gemini анализирует текст и извлекает ключевые темы, решения и задачи
5. Cоздается страница в Notion
6. Генерируется PDF-отчет и отправляется в Telegram с кратким summary и PDF


