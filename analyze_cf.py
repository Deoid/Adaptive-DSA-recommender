import httpx

res = httpx.get("https://codeforces.com/api/user.status?handle=hardikjha0011&from=1&count=1000")
data = res.json()["result"]
print("Total submissions returned by user.status:", len(data))

# Group by contestId
contests = set()
for s in data:
    p = s.get("problem", {})
    if p.get("contestId"):
        contests.add(p.get("contestId"))
print(f"Submissions span {len(contests)} unique contest IDs.")

# Check problem IDs with OK or other verdicts
ac_problems = {}
for s in data:
    p = s.get("problem", {})
    pid = f"{p.get('contestId')}{p.get('index')}"
    v = s.get("verdict")
    if pid not in ac_problems:
        ac_problems[pid] = []
    ac_problems[pid].append(v)

ac_count = sum(1 for pid, vlist in ac_problems.items() if "OK" in vlist)
print("Unique problems with at least one OK:", ac_count)
print("Unique problems attempted:", len(ac_problems))
