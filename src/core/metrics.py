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
