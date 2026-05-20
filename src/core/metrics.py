from prometheus_client import Counter, Histogram

transcription_latency = Histogram(
    'transcription_latency_seconds',
    'Google Speech-to-Text end-to-end latency',
)

pipeline_failures = Counter(
    'pipeline_failures_total',
    'Pipeline stage failures',
    ['stage'],
)

llm_judge_latency = Histogram(
    'llm_judge_latency_seconds',
    'LLM-as-judge evaluation call latency',
)

llm_calls_total = Counter(
    'llm_calls_total',
    'Total LLM API calls by stage',
    ['stage'],
)
