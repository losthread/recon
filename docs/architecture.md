# RECON Architecture Flow

```
CLI Input
  ↓
Rate Limiter
  ↓
Fetchers (Reddit, X, Instagram)
  ↓
Data Cleaner (normalize, extract features)
  ↓
Heuristic Linker (rule-based scoring)
  ↓
LLM Disambiguator (for uncertain pairs)
  ↓
Identity Builder (group profiles into persons)
  ↓
Scorer & Ranker (confidence points)
  ↓
CLI Output (ranked list)
```