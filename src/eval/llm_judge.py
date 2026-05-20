import json
import logging
import time
from dataclasses import dataclass

from google import genai

from core.config import settings
from core.metrics import llm_calls_total, llm_judge_latency

logger = logging.getLogger(__name__)

_JUDGE_PROMPT = """
Evaluate the quality of AI-extracted meeting data. Score each dimension 1–5.

1 = very poor, 3 = acceptable, 5 = excellent

Dimensions:
- task_extraction: tasks are well-formed with title, description, and context
- speaker_identification: speakers have real names (not "Speaker 1/2")
- priority_accuracy: priority levels (high/medium/low) match the urgency signals in the data
- completeness: summary has topics, decisions, and key_points populated

Meeting data to evaluate:
{meeting_data}

Reply with ONLY valid JSON, no markdown fences:
{{"task_extraction": N, "speaker_identification": N, "priority_accuracy": N,
"completeness": N, "reasoning": "..."}}
"""


@dataclass
class EvalResult:
    task_extraction: int
    speaker_identification: int
    priority_accuracy: int
    completeness: int
    overall: float
    reasoning: str


async def evaluate_meeting_quality(meeting_data: dict) -> EvalResult | None:
    try:
        client = genai.Client(api_key=settings.google.api_key.get_secret_value())
        prompt = _JUDGE_PROMPT.format(
            meeting_data=json.dumps(meeting_data, ensure_ascii=False, indent=2)
        )

        start = time.perf_counter()
        response = await client.aio.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        latency = time.perf_counter() - start

        llm_judge_latency.observe(latency)
        llm_calls_total.labels(stage='llm_judge').inc()

        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].rsplit('```', 1)[0]

        scores = json.loads(text)
        result = EvalResult(
            task_extraction=scores['task_extraction'],
            speaker_identification=scores['speaker_identification'],
            priority_accuracy=scores['priority_accuracy'],
            completeness=scores['completeness'],
            overall=round(
                sum([
                    scores['task_extraction'],
                    scores['speaker_identification'],
                    scores['priority_accuracy'],
                    scores['completeness'],
                ]) / 4,
                2,
            ),
            reasoning=scores.get('reasoning', ''),
        )

        logger.info(
            'llm_judge_result',
            extra={
                'task_extraction': result.task_extraction,
                'speaker_identification': result.speaker_identification,
                'priority_accuracy': result.priority_accuracy,
                'completeness': result.completeness,
                'overall': result.overall,
                'reasoning': result.reasoning,
                'latency_seconds': round(latency, 3),
            },
        )
        return result

    except Exception as e:
        logger.error('[EVAL] LLM judge failed: %s', e, exc_info=True)
        return None
