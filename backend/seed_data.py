from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.problem import ProblemCatalog
from backend.services.platforms.codeforces import codeforces_client
from backend.services.canonical_topics import normalize_tags_to_canonical

DEFAULT_PROBLEM_POOL = [
    # Dynamic Programming
    {
        "platform": "codeforces",
        "problem_id": "455A",
        "title": "Boredom",
        "url": "https://codeforces.com/problemset/problem/455/A",
        "canonical_topic": "Dynamic Programming",
        "tags": "dp, greedy",
        "difficulty": 1500,
        "acceptance_rate": 0.42,
    },
    {
        "platform": "codeforces",
        "problem_id": "118D",
        "title": "Caesar's Legions",
        "url": "https://codeforces.com/problemset/problem/118/D",
        "canonical_topic": "Dynamic Programming",
        "tags": "dp",
        "difficulty": 1600,
        "acceptance_rate": 0.38,
    },
    {
        "platform": "leetcode",
        "problem_id": "coin-change",
        "title": "Coin Change",
        "url": "https://leetcode.com/problems/coin-change/",
        "canonical_topic": "Dynamic Programming",
        "tags": "Dynamic Programming, Breadth-First Search",
        "difficulty": 1450,
        "acceptance_rate": 0.44,
    },
    {
        "platform": "leetcode",
        "problem_id": "longest-increasing-subsequence",
        "title": "Longest Increasing Subsequence",
        "url": "https://leetcode.com/problems/longest-increasing-subsequence/",
        "canonical_topic": "Dynamic Programming",
        "tags": "Dynamic Programming, Binary Search",
        "difficulty": 1650,
        "acceptance_rate": 0.53,
    },
    {
        "platform": "atcoder",
        "problem_id": "dp_a",
        "title": "Frog 1 (Educational DP Contest)",
        "url": "https://atcoder.jp/contests/dp/tasks/dp_a",
        "canonical_topic": "Dynamic Programming",
        "tags": "dp",
        "difficulty": 1100,
        "acceptance_rate": 0.72,
    },
    {
        "platform": "atcoder",
        "problem_id": "dp_d",
        "title": "Knapsack 1",
        "url": "https://atcoder.jp/contests/dp/tasks/dp_d",
        "canonical_topic": "Dynamic Programming",
        "tags": "dp",
        "difficulty": 1350,
        "acceptance_rate": 0.58,
    },

    # Graph Algorithms
    {
        "platform": "codeforces",
        "problem_id": "20C",
        "title": "Dijkstra?",
        "url": "https://codeforces.com/problemset/problem/20/C",
        "canonical_topic": "Graph Algorithms",
        "tags": "shortest paths, graphs",
        "difficulty": 1900,
        "acceptance_rate": 0.35,
    },
    {
        "platform": "codeforces",
        "problem_id": "520B",
        "title": "Two Buttons",
        "url": "https://codeforces.com/problemset/problem/520/B",
        "canonical_topic": "Graph Algorithms",
        "tags": "dfs and similar, graphs, greedy",
        "difficulty": 1400,
        "acceptance_rate": 0.52,
    },
    {
        "platform": "leetcode",
        "problem_id": "course-schedule-ii",
        "title": "Course Schedule II",
        "url": "https://leetcode.com/problems/course-schedule-ii/",
        "canonical_topic": "Graph Algorithms",
        "tags": "Graph, Topological Sort, BFS, DFS",
        "difficulty": 1550,
        "acceptance_rate": 0.50,
    },
    {
        "platform": "leetcode",
        "problem_id": "network-delay-time",
        "title": "Network Delay Time",
        "url": "https://leetcode.com/problems/network-delay-time/",
        "canonical_topic": "Graph Algorithms",
        "tags": "Graph, Shortest Path, Dijkstra",
        "difficulty": 1600,
        "acceptance_rate": 0.54,
    },

    # Trees & Binary Search Trees
    {
        "platform": "codeforces",
        "problem_id": "580C",
        "title": "Kefa and Park",
        "url": "https://codeforces.com/problemset/problem/580/C",
        "canonical_topic": "Trees & Binary Search Trees",
        "tags": "dfs and similar, trees, graphs",
        "difficulty": 1500,
        "acceptance_rate": 0.44,
    },
    {
        "platform": "leetcode",
        "problem_id": "lowest-common-ancestor-of-a-binary-tree",
        "title": "Lowest Common Ancestor of a Binary Tree",
        "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
        "canonical_topic": "Trees & Binary Search Trees",
        "tags": "Tree, Depth-First Search, Binary Tree",
        "difficulty": 1450,
        "acceptance_rate": 0.61,
    },
    {
        "platform": "codechef",
        "problem_id": "TREE2",
        "title": "A Problem on Trees",
        "url": "https://www.codechef.com/problems/TREE2",
        "canonical_topic": "Trees & Binary Search Trees",
        "tags": "trees, data structures",
        "difficulty": 1300,
        "acceptance_rate": 0.48,
    },

    # Binary Search & Two Pointers
    {
        "platform": "codeforces",
        "problem_id": "279B",
        "title": "Books",
        "url": "https://codeforces.com/problemset/problem/279/B",
        "canonical_topic": "Binary Search & Two Pointers",
        "tags": "binary search, two pointers",
        "difficulty": 1400,
        "acceptance_rate": 0.46,
    },
    {
        "platform": "leetcode",
        "problem_id": "find-minimum-in-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "url": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
        "canonical_topic": "Binary Search & Two Pointers",
        "tags": "Binary Search, Array",
        "difficulty": 1350,
        "acceptance_rate": 0.51,
    },
    {
        "platform": "leetcode",
        "problem_id": "container-with-most-water",
        "title": "Container With Most Water",
        "url": "https://leetcode.com/problems/container-with-most-water/",
        "canonical_topic": "Binary Search & Two Pointers",
        "tags": "Two Pointers, Greedy",
        "difficulty": 1400,
        "acceptance_rate": 0.55,
    },

    # Greedy Algorithms
    {
        "platform": "codeforces",
        "problem_id": "158B",
        "title": "Taxi",
        "url": "https://codeforces.com/problemset/problem/158/B",
        "canonical_topic": "Greedy Algorithms",
        "tags": "greedy, special problem",
        "difficulty": 1100,
        "acceptance_rate": 0.60,
    },
    {
        "platform": "codeforces",
        "problem_id": "1360E",
        "title": "Polygon",
        "url": "https://codeforces.com/problemset/problem/1360/E",
        "canonical_topic": "Greedy Algorithms",
        "tags": "greedy, implementation",
        "difficulty": 1300,
        "acceptance_rate": 0.52,
    },
    {
        "platform": "leetcode",
        "problem_id": "jump-game-ii",
        "title": "Jump Game II",
        "url": "https://leetcode.com/problems/jump-game-ii/",
        "canonical_topic": "Greedy Algorithms",
        "tags": "Greedy, Dynamic Programming",
        "difficulty": 1500,
        "acceptance_rate": 0.45,
    },

    # Data Structures (Stack, Queue, Heap, DSU)
    {
        "platform": "codeforces",
        "problem_id": "25D",
        "title": "Roads not only in Berland",
        "url": "https://codeforces.com/problemset/problem/25/D",
        "canonical_topic": "Data Structures (Stack, Queue, Heap, DSU)",
        "tags": "dsu, trees, graphs",
        "difficulty": 1700,
        "acceptance_rate": 0.39,
    },
    {
        "platform": "leetcode",
        "problem_id": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "url": "https://leetcode.com/problems/trapping-rain-water/",
        "canonical_topic": "Data Structures (Stack, Queue, Heap, DSU)",
        "tags": "Monotonic Stack, Two Pointers, Dynamic Programming",
        "difficulty": 1750,
        "acceptance_rate": 0.61,
    },
    {
        "platform": "leetcode",
        "problem_id": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "url": "https://leetcode.com/problems/top-k-frequent-elements/",
        "canonical_topic": "Data Structures (Stack, Queue, Heap, DSU)",
        "tags": "Heap, Hash Table, Bucket Sort",
        "difficulty": 1350,
        "acceptance_rate": 0.63,
    },

    # Math & Number Theory
    {
        "platform": "codeforces",
        "problem_id": "230B",
        "title": "T-primes",
        "url": "https://codeforces.com/problemset/problem/230/B",
        "canonical_topic": "Math & Number Theory",
        "tags": "math, number theory, binary search",
        "difficulty": 1300,
        "acceptance_rate": 0.49,
    },
    {
        "platform": "codeforces",
        "problem_id": "472A",
        "title": "Design Tutorial: Learn from Math",
        "url": "https://codeforces.com/problemset/problem/472/A",
        "canonical_topic": "Math & Number Theory",
        "tags": "math, number theory",
        "difficulty": 900,
        "acceptance_rate": 0.77,
    },

    # Strings & Tries
    {
        "platform": "leetcode",
        "problem_id": "implement-trie-prefix-tree",
        "title": "Implement Trie (Prefix Tree)",
        "url": "https://leetcode.com/problems/implement-trie-prefix-tree/",
        "canonical_topic": "Strings & Tries",
        "tags": "Trie, String, Design",
        "difficulty": 1400,
        "acceptance_rate": 0.64,
    },
    {
        "platform": "codeforces",
        "problem_id": "126B",
        "title": "Password",
        "url": "https://codeforces.com/problemset/problem/126/B",
        "canonical_topic": "Strings & Tries",
        "tags": "strings, string suffix structures",
        "difficulty": 1700,
        "acceptance_rate": 0.32,
    },

    # Bit Manipulation
    {
        "platform": "codeforces",
        "problem_id": "484A",
        "title": "Bits",
        "url": "https://codeforces.com/problemset/problem/484/A",
        "canonical_topic": "Bit Manipulation",
        "tags": "bitmasks, greedy, math",
        "difficulty": 1600,
        "acceptance_rate": 0.41,
    },
    {
        "platform": "leetcode",
        "problem_id": "single-number-ii",
        "title": "Single Number II",
        "url": "https://leetcode.com/problems/single-number-ii/",
        "canonical_topic": "Bit Manipulation",
        "tags": "Bit Manipulation, Array",
        "difficulty": 1400,
        "acceptance_rate": 0.60,
    },

    # Backtracking & Recursion
    {
        "platform": "leetcode",
        "problem_id": "n-queens",
        "title": "N-Queens",
        "url": "https://leetcode.com/problems/n-queens/",
        "canonical_topic": "Backtracking & Recursion",
        "tags": "Backtracking, Array",
        "difficulty": 1800,
        "acceptance_rate": 0.68,
    },
    {
        "platform": "leetcode",
        "problem_id": "subsets",
        "title": "Subsets",
        "url": "https://leetcode.com/problems/subsets/",
        "canonical_topic": "Backtracking & Recursion",
        "tags": "Backtracking, Bit Manipulation",
        "difficulty": 1250,
        "acceptance_rate": 0.77,
    },
]

async def seed_problems_catalog(db: AsyncSession):
    """Populates the database catalog with curated problems and live Codeforces problems."""
    # Check if catalog already populated
    check = await db.execute(select(ProblemCatalog).limit(1))
    if check.scalar_one_or_none() is not None:
        return

    # Add default pool
    for p in DEFAULT_PROBLEM_POOL:
        catalog_item = ProblemCatalog(
            platform=p["platform"],
            problem_id=p["problem_id"],
            title=p["title"],
            url=p["url"],
            canonical_topic=p["canonical_topic"],
            tags=p["tags"],
            difficulty=p["difficulty"],
            acceptance_rate=p.get("acceptance_rate", 0.5),
        )
        db.add(catalog_item)

    await db.commit()

    # Try fetching additional live problems via Codeforces API in the background
    try:
        cf_pool = await codeforces_client.fetch_problemset(count=60)
        for cp in cf_pool:
            canonical = normalize_tags_to_canonical(cp.get("tags", []), "codeforces")
            item = ProblemCatalog(
                platform="codeforces",
                problem_id=cp["problem_id"],
                title=cp["title"],
                url=cp["url"],
                canonical_topic=canonical,
                tags=", ".join(cp.get("tags", [])),
                difficulty=cp["difficulty"],
                acceptance_rate=0.45,
            )
            db.add(item)
        await db.commit()
    except Exception as e:
        print(f"[Seed] Note: Codeforces live problemset load skipped or completed: {e}")
