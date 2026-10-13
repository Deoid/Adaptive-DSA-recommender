from typing import List, Optional

CANONICAL_TOPICS = [
    "Dynamic Programming",
    "Graph Algorithms",
    "Trees & Binary Search Trees",
    "Binary Search & Two Pointers",
    "Greedy Algorithms",
    "Data Structures (Stack, Queue, Heap, DSU)",
    "Math & Number Theory",
    "Strings & Tries",
    "Bit Manipulation",
    "Backtracking & Recursion",
]

# Mapping Codeforces tags to canonical topics
CODEFORCES_TAG_MAP = {
    "dp": "Dynamic Programming",
    "greedy": "Greedy Algorithms",
    "graphs": "Graph Algorithms",
    "dfs and similar": "Graph Algorithms",
    "shortest paths": "Graph Algorithms",
    "flows": "Graph Algorithms",
    "trees": "Trees & Binary Search Trees",
    "binary search": "Binary Search & Two Pointers",
    "two pointers": "Binary Search & Two Pointers",
    "data structures": "Data Structures (Stack, Queue, Heap, DSU)",
    "dsu": "Data Structures (Stack, Queue, Heap, DSU)",
    "math": "Math & Number Theory",
    "number theory": "Math & Number Theory",
    "combinatorics": "Math & Number Theory",
    "probabilities": "Math & Number Theory",
    "strings": "Strings & Tries",
    "string suffix structures": "Strings & Tries",
    "bitmasks": "Bit Manipulation",
    "divide and conquer": "Backtracking & Recursion",
    "brute force": "Backtracking & Recursion",
    "games": "Math & Number Theory",
    "geometry": "Math & Number Theory",
}

# Mapping LeetCode tags to canonical topics
LEETCODE_TAG_MAP = {
    "dynamic programming": "Dynamic Programming",
    "greedy": "Greedy Algorithms",
    "graph": "Graph Algorithms",
    "depth-first search": "Graph Algorithms",
    "breadth-first search": "Graph Algorithms",
    "tree": "Trees & Binary Search Trees",
    "binary tree": "Trees & Binary Search Trees",
    "binary search tree": "Trees & Binary Search Trees",
    "binary search": "Binary Search & Two Pointers",
    "two pointers": "Binary Search & Two Pointers",
    "sliding window": "Binary Search & Two Pointers",
    "heap (priority queue)": "Data Structures (Stack, Queue, Heap, DSU)",
    "stack": "Data Structures (Stack, Queue, Heap, DSU)",
    "queue": "Data Structures (Stack, Queue, Heap, DSU)",
    "union find": "Data Structures (Stack, Queue, Heap, DSU)",
    "design": "Data Structures (Stack, Queue, Heap, DSU)",
    "monotonous stack": "Data Structures (Stack, Queue, Heap, DSU)",
    "math": "Math & Number Theory",
    "number theory": "Math & Number Theory",
    "geometry": "Math & Number Theory",
    "string": "Strings & Tries",
    "trie": "Strings & Tries",
    "bit manipulation": "Bit Manipulation",
    "backtracking": "Backtracking & Recursion",
    "recursion": "Backtracking & Recursion",
}

# Mapping AtCoder / Kenkoooo / CodeChef tags
GENERIC_TAG_MAP = {
    "dp": "Dynamic Programming",
    "dynamic-programming": "Dynamic Programming",
    "graph": "Graph Algorithms",
    "tree": "Trees & Binary Search Trees",
    "greedy": "Greedy Algorithms",
    "binary-search": "Binary Search & Two Pointers",
    "math": "Math & Number Theory",
    "strings": "Strings & Tries",
    "string": "Strings & Tries",
    "data-structures": "Data Structures (Stack, Queue, Heap, DSU)",
    "bit": "Bit Manipulation",
    "bitmask": "Bit Manipulation",
    "backtracking": "Backtracking & Recursion",
}

def map_tag_to_canonical(tag: str, platform: str = "generic") -> Optional[str]:
    clean_tag = tag.lower().strip()
    if platform.lower() == "codeforces":
        if clean_tag in CODEFORCES_TAG_MAP:
            return CODEFORCES_TAG_MAP[clean_tag]
    elif platform.lower() == "leetcode":
        if clean_tag in LEETCODE_TAG_MAP:
            return LEETCODE_TAG_MAP[clean_tag]
    
    # Generic fallback
    if clean_tag in CODEFORCES_TAG_MAP:
        return CODEFORCES_TAG_MAP[clean_tag]
    if clean_tag in LEETCODE_TAG_MAP:
        return LEETCODE_TAG_MAP[clean_tag]
    if clean_tag in GENERIC_TAG_MAP:
        return GENERIC_TAG_MAP[clean_tag]
    
    # Substring search
    for key, canonical in CODEFORCES_TAG_MAP.items():
        if key in clean_tag:
            return canonical
    for key, canonical in LEETCODE_TAG_MAP.items():
        if key in clean_tag:
            return canonical
            
    return None

def normalize_tags_to_canonical(tags: List[str], platform: str = "generic") -> str:
    for tag in tags:
        canonical = map_tag_to_canonical(tag, platform)
        if canonical:
            return canonical
    return "Data Structures (Stack, Queue, Heap, DSU)"
