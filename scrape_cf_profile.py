import httpx
from bs4 import BeautifulSoup
import re

url = "https://codeforces.com/profile/hardikjha0011"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

with httpx.Client(headers=headers, follow_redirects=True) as client:
    res = client.get(url)
    print("Codeforces profile page status:", res.status_code)
    if res.status_code == 200:
        matches = re.findall(r"(\d+)\s*problems?\s*solved", res.text, re.I)
        print("Matches for 'X problems solved':", matches)
        matches2 = re.findall(r"solved for all time:\s*(\d+)", res.text, re.I)
        print("Matches for 'solved for all time':", matches2)
        # Search for any occurrence of 140
        for m in re.finditer(r"(?:all time|problem|solved)[^<>\d]*(\d+)", res.text, re.I):
            print("Found nearby:", m.group(0))
