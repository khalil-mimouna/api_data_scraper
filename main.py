import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

start = int(os.getenv("START_PHONE"))
end = int(os.getenv("END_PHONE"))
concurrent_requests = int(os.getenv("CONCURRENT_REQUESTS"))
api_base_url = os.getenv("API_BASE_URL")
results_file = os.getenv("RESULTS_FILE", "valid_results.jsonl")
log_file = os.getenv("LOG_FILE", "processed_phones.log")

sem = asyncio.Semaphore(concurrent_requests)

# Load already processed phone numbers
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        processed = set(int(line.strip()) for line in f)
else:
    processed = set()

async def fetch(session, phone):
    url = f"{api_base_url}?phone={phone}"
    async with sem:
        try:
            async with session.get(url, timeout=5) as response:
                text = await response.text()
                if "Resource not found" not in text:
                    print(f"[FOUND] {phone}")
                    data = await response.json()
                    data["phone"] = phone
                    with open(results_file, "a", encoding="utf-8") as rf:
                        rf.write(json.dumps(data, ensure_ascii=False) + "\n")
                else:
                    print(f"[NOT FOUND] {phone}")
        except Exception as e:
            print(f"[ERROR] {phone}: {e}")
        finally:
            with open(log_file, "a") as lf:
                lf.write(str(phone) + "\n")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch(session, phone)
            for phone in range(start, end + 1)
            if phone not in processed
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
