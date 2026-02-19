from __future__ import annotations

def approx_tokens_from_text(text: str) -> int:
    # legacy heuristic: len/4
    return max(0, int(len(text) / 4))

def progress_pct(tokens: int, max_tokens: int) -> float:
    if max_tokens <= 0:
        return 0.0
    return min(1.0, tokens / max_tokens)
