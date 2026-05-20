from jiwer import wer as _wer


def word_error_rate(reference: str, hypothesis: str) -> float:
    """WER in range [0, 1]. Use in offline benchmarks with reference transcripts."""
    return _wer(reference, hypothesis)
