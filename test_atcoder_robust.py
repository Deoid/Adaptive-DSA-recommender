import httpx
from bs4 import BeautifulSoup
import re

handle = "hardikjha0011"

# 1. Fetch Kenkoooo submissions
subs_url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={handle}&from_second=0"
r_subs = httpx.get(subs_url, timeout=10.0)
unique_ac = 0
if r_subs.status_code == 200:
    subs = r_subs.json()
    ac_problems = set(s.get("problem_id") for s in subs if s.get("result") == "AC")
    unique_ac = len(ac_problems)

# 2. Fetch AtCoder rating
profile_url = f"https://atcoder.jp/users/{handle}"
r_prof = httpx.get(profile_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10.0)
rating = 0
highest = 0
if r_prof.status_code == 200:
    m = re.search(r"Rating.*?(\d+)", r_prof.text, re.DOTALL)
    if m:
        rating = int(m.group(1))
    m_high = re.search(r"Highest Rating.*?(\d+)", r_prof.text, re.DOTALL)
    if m_high:
        highest = int(m_high.group(1))

print(f"AtCoder Results for '{handle}': Rating={rating}, Highest={highest}, Unique AC Solved={unique_ac}")
