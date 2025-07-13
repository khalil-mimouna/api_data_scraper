# 📞 ClassQuiz API Phone Audit

This script uses Python `asyncio` and `aiohttp` to scan a range of phone numbers against the ClassQuiz public API to identify valid accounts and get their data.

- Asynchronous parallel scanning with concurrency control
- Logs all processed numbers
- Stores valid results in JSONL format