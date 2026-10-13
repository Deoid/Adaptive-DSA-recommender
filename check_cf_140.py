import httpx
from bs4 import BeautifulSoup
import re

handle = "hardikjha0011"
url = f"https://codeforces.com/profile/{handle}"
headers = {"User-Agent": "Mozilla/5.0"}

res = httpx.get(url, headers=headers)
print("Codeforces profile page status:", res.status_code)

soup = BeautifulSoup(res.text, "html.parser")
for elem in soup.find_all(string=re.compile(r"problem|solved", re.I)):
    parent_text = elem.parent.text.strip().replace("\n", " ")
    print("Found text:", parent_text)

# Also check all _UserActivityFrame or similar sections
activity = soup.find_all("div", class_=re.compile("activity|profile", re.I))
for a in activity:
    if "solved" in a.text.lower():
        print("Activity block:", a.text[:300].strip().replace("\n", " "))
