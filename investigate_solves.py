import httpx

handle = "hardikjha0011"
print(f"=== INVESTIGATING FOR HANDLE: {handle} ===")

# 1. Inspect Codeforces
cf_res = httpx.get(f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=5000")
cf_data = cf_res.json()
if cf_data.get("status") == "OK":
    subs = cf_data["result"]
    unique_standard = set()
    unique_all = set()
    gym_count = 0
    verdicts = {}
    for s in subs:
        v = s.get("verdict")
        verdicts[v] = verdicts.get(v, 0) + 1
        if v == "OK":
            p = s.get("problem", {})
            cid = p.get("contestId")
            idx = p.get("index")
            name = p.get("name")
            # All problems including gym
            key = f"{cid}_{idx}" if cid else f"name_{name}"
            unique_all.add(key)
            if cid and cid < 100000:
                unique_standard.add(f"{cid}{idx}")
            else:
                gym_count += 1
    print("CF Submissions verdict breakdown:", verdicts)
    print("CF Unique Standard Problems (contestId < 100000):", len(unique_standard))
    print("CF Unique All AC (including Gym / Mashup / Custom):", len(unique_all))
    print("CF Gym/Other problems:", gym_count)

# 2. Inspect AtCoder Kenkoooo API
print("\n--- Testing AtCoder Kenkoooo API ---")
for at_handle in [handle, "hardikjha", "hardik"]:
    url1 = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/info?user={at_handle}"
    url2 = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={at_handle}&from_second=0"
    try:
        r1 = httpx.get(url1, timeout=8.0)
        r2 = httpx.get(url2, timeout=8.0)
        print(f"Kenkoooo user/info for '{at_handle}': status={r1.status_code}, data={r1.text}")
        if r2.status_code == 200:
            subs = r2.json()
            ac_subs = [s for s in subs if s.get("result") == "AC"]
            unique_ac = len(set(s.get("problem_id") for s in ac_subs))
            print(f"Kenkoooo submissions for '{at_handle}': total={len(subs)}, AC={len(ac_subs)}, unique AC={unique_ac}")
    except Exception as e:
        print(f"Error for '{at_handle}': {e}")
