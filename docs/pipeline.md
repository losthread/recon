# Pipeline Overview

## Stage Breakdown

### 1. CLI Input
User provides search parameters:
- `--username` (compulsory)
- `--email` (optional)
- `--name` (optional)

**Example:**
```bash
recon --username john_doe --email john@gmail.com
```

### 2. Rate Limiter
Prevents abuse and DDoS:
- Track requests per IP
- Enforce cooldown between requests
- Block IPs exceeding threshold

**Actions:**
- ✓ Allow: Continue to fetchers
- ✗ Block: Reject request

### 3. Fetchers (Reddit, X, Instagram)
Parallel API calls to fetch user data:
- Fetch profiles by username/email
- Extract bios, post history, metadata
- Standardize output to Profile object

**Output:**
```json
{
  "platform": "reddit",
  "username": "john_doe",
  "bio": "Python developer, hiking enthusiast",
  "posts": ["Just deployed FastAPI...", "Went hiking..."],
  "account_age": "3 years"
}
```

### 4. Data Cleaner
Normalize and extract features:
- Lowercase usernames
- Remove special characters
- Extract keywords (job, interests, location)
- De-duplicate text
- Parse dates

**Output:**
```json
{
  "platform": "reddit",
  "username": "john_doe",
  "keywords": ["python", "developer", "hiking"],
  "bio_clean": "python developer hiking enthusiast"
}
```

### 5. Heuristic Linker
Rule-based scoring to link profiles (same person):

**Heuristics:**
- Exact username match: +x points
- Email domain inference: +x points
- Name similarity: +x points
- Bio overlap: +x points
- Account age proximity: +x points
- Location consistency: +x points

**Output:**

### 6. LLM Disambiguator
For ambiguous cases (50-80 score), feed info to LLM and let it further classify the ranking:

**Input to LLM:**