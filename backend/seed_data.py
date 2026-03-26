"""
示例题目数据 - 首次运行时自动插入，后续启动自动补充新题
"""
import database as db

# ==================== LeetCode 模式辅助代码片段 ====================

_LIST_HELPERS = """\
import sys
input = sys.stdin.readline

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def _build_list(arr):
    dummy = ListNode(0)
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def _print_list(head):
    res = []
    while head:
        res.append(str(head.val))
        head = head.next
    print(' '.join(res) if res else '')
"""

_TREE_HELPERS = """\
import sys
from collections import deque
input = sys.stdin.readline

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def _build_tree(vals):
    if not vals or vals[0] == -1:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] != -1:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] != -1:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root

def _find_node(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return _find_node(root.left, val) or _find_node(root.right, val)
"""

# ==================== 题目数据 ====================

SAMPLE_PROBLEMS = [
    # ---- 1. 两数之和 ----
    {
        "title": "两数之和",
        "difficulty": "Easy",
        "tags": ["数组", "哈希表"],
        "source": "LeetCode #1",
        "source_url": "https://leetcode.cn/problems/two-sum/",
        "description": """## 题目描述

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出 **和为目标值** 的那 **两个** 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

### 示例

```
输入: nums = [2,7,11,15], target = 9
输出: [0,1]
```

### 约束

- `2 <= nums.length <= 10^4`
- 只会存在一个有效答案
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n, target = map(int, input().split())\n    nums = list(map(int, input().split()))\n    # 在这里写你的解法\n    pass\n\nsolve()\n",
        "lc_template": "def twoSum(nums, target):\n    # 返回两个下标的列表\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn, target = map(int, input().split())\nnums = list(map(int, input().split()))\nprint(*twoSum(nums, target))\n",
        "test_cases": [
            {"input": "4 9\n2 7 11 15", "expected_output": "0 1"},
            {"input": "3 6\n3 2 4", "expected_output": "1 2"},
            {"input": "2 6\n3 3", "expected_output": "0 1"},
        ]
    },
    # ---- 2. 最长递增子序列 ----
    {
        "title": "最长递增子序列",
        "difficulty": "Medium",
        "tags": ["动态规划", "二分查找"],
        "source": "LeetCode #300",
        "source_url": "https://leetcode.cn/problems/longest-increasing-subsequence/",
        "description": """## 题目描述

给你一个整数数组 `nums`，找到其中最长严格递增子序列的长度。

### 示例

```
输入: nums = [10,9,2,5,3,7,101,18]
输出: 4
解释: 最长递增子序列是 [2,3,7,101]
```

### 约束

- `1 <= nums.length <= 2500`
- `-10^4 <= nums[i] <= 10^4`
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    nums = list(map(int, input().split()))\n    pass\n\nsolve()\n",
        "lc_template": "def lengthOfLIS(nums):\n    # 返回最长递增子序列的长度\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nnums = list(map(int, input().split()))\nprint(lengthOfLIS(nums))\n",
        "test_cases": [
            {"input": "8\n10 9 2 5 3 7 101 18", "expected_output": "4"},
            {"input": "6\n0 1 0 3 2 3", "expected_output": "4"},
            {"input": "1\n7", "expected_output": "1"},
            {"input": "8\n7 7 7 7 7 7 7 7", "expected_output": "1"},
        ]
    },
    # ---- 3. 接雨水 ----
    {
        "title": "接雨水",
        "difficulty": "Hard",
        "tags": ["栈", "数组", "双指针", "单调栈"],
        "source": "LeetCode #42",
        "source_url": "https://leetcode.cn/problems/trapping-rain-water/",
        "description": """## 题目描述

给定 `n` 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

### 示例

```
输入: height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出: 6
```

### 约束

- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    height = list(map(int, input().split()))\n    pass\n\nsolve()\n",
        "lc_template": "def trap(height):\n    # 返回能接的雨水量\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nheight = list(map(int, input().split()))\nprint(trap(height))\n",
        "test_cases": [
            {"input": "12\n0 1 0 2 1 0 1 3 2 1 2 1", "expected_output": "6"},
            {"input": "6\n4 2 0 3 2 5", "expected_output": "9"},
            {"input": "3\n1 0 1", "expected_output": "1"},
        ]
    },
    # ---- 4. 合并区间 ----
    {
        "title": "合并区间",
        "difficulty": "Medium",
        "tags": ["排序", "数组"],
        "source": "LeetCode #56",
        "source_url": "https://leetcode.cn/problems/merge-intervals/",
        "description": """## 题目描述

以数组 `intervals` 表示若干个区间的集合，请你合并所有重叠的区间，并返回一个不重叠的区间数组。

### 示例

```
输入: intervals = [[1,3],[2,6],[8,10],[15,18]]
输出: [[1,6],[8,10],[15,18]]
```

### 约束

- `1 <= intervals.length <= 10^4`
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    intervals = []\n    for _ in range(n):\n        a, b = map(int, input().split())\n        intervals.append([a, b])\n    pass\n\nsolve()\n",
        "lc_template": "def merge(intervals):\n    # 返回合并后的区间列表\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nintervals = [list(map(int, input().split())) for _ in range(n)]\nresult = merge(intervals)\nfor a, b in result:\n    print(a, b)\n",
        "test_cases": [
            {"input": "4\n1 3\n2 6\n8 10\n15 18", "expected_output": "1 6\n8 10\n15 18"},
            {"input": "2\n1 4\n4 5", "expected_output": "1 5"},
        ]
    },
    # ---- 5. 岛屿数量 ----
    {
        "title": "岛屿数量",
        "difficulty": "Medium",
        "tags": ["BFS", "DFS", "并查集"],
        "source": "LeetCode #200",
        "source_url": "https://leetcode.cn/problems/number-of-islands/",
        "description": """## 题目描述

给你一个由 `'1'`（陆地）和 `'0'`（水）组成的二维网格，请你计算网格中岛屿的数量。

### 示例

```
输入: grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]
输出: 3
```

### 约束

- `1 <= m, n <= 300`
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    m, n = map(int, input().split())\n    grid = [list(input().split()) for _ in range(m)]\n    pass\n\nsolve()\n",
        "lc_template": "def numIslands(grid):\n    # 返回岛屿数量\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nm, n = map(int, input().split())\ngrid = [list(input().split()) for _ in range(m)]\nprint(numIslands(grid))\n",
        "test_cases": [
            {"input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "expected_output": "1"},
            {"input": "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1", "expected_output": "3"},
        ]
    },
    # ---- 6. 移掉K位数字 ----
    {
        "title": "移掉K位数字",
        "difficulty": "Medium",
        "tags": ["栈", "贪心", "单调栈"],
        "source": "LeetCode #402",
        "source_url": "https://leetcode.cn/problems/remove-k-digits/",
        "description": """## 题目描述

给你一个以字符串表示的非负整数 `num` 和一个整数 `k`，移除这个数中的 `k` 位数字，使得剩下的数字最小。请你以字符串形式返回这个最小的数字。

### 示例

```
输入: num = "1432219", k = 3
输出: "1219"
解释: 移除掉三个数字 4, 3, 和 2 形成一个新的最小的数字 1219
```

```
输入: num = "10200", k = 1
输出: "200"
```

```
输入: num = "10", k = 2
输出: "0"
```

### 约束

- `1 <= k <= num.length <= 10^5`
- `num` 仅由若干位数字（0-9）组成
- 除了 0 本身之外，`num` 不含任何前导零

### 提示

使用单调栈：遍历数字，当栈顶元素大于当前数字时弹出栈顶（相当于移除），直到移除 k 个数字。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    num = input().strip()\n    k = int(input())\n    # 输出移除k位后的最小数字字符串\n    pass\n\nsolve()\n",
        "lc_template": "def removeKdigits(num, k):\n    # 返回移除k位后的最小数字字符串\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nnum = input().strip()\nk = int(input())\nprint(removeKdigits(num, k))\n",
        "test_cases": [
            {"input": "1432219\n3", "expected_output": "1219"},
            {"input": "10200\n1", "expected_output": "200"},
            {"input": "10\n2", "expected_output": "0"},
            {"input": "9\n1", "expected_output": "0"},
        ]
    },
    # ---- 7. 累加数 ----
    {
        "title": "累加数",
        "difficulty": "Medium",
        "tags": ["字符串", "回溯"],
        "source": "LeetCode #306",
        "source_url": "https://leetcode.cn/problems/additive-number/",
        "description": """## 题目描述

**累加数** 是一个字符串，组成它的数字可以形成累加序列。一个有效的累加序列必须 **至少** 包含 3 个数。除了最开始的两个数以外，序列中的每个后续数字必须是它之前两个数字之和。

给你一个只包含数字 `'0'-'9'` 的字符串，编写一个算法来判断给定输入是否是 **累加数**。

**说明**：累加序列里的数，除数字 0 之外，不会以 0 开头。

### 示例

```
输入: "112358"
输出: true
解释: 1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8
```

```
输入: "199100199"
输出: true
解释: 1 + 99 = 100, 99 + 100 = 199
```

### 约束

- `1 <= num.length <= 35`

### 提示

回溯枚举前两个数的分割位置，然后验证后续是否满足累加关系。注意大数相加。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    num = input().strip()\n    # 输出 true 或 false\n    pass\n\nsolve()\n",
        "lc_template": "def isAdditiveNumber(num):\n    # 返回 True 或 False\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nnum = input().strip()\nprint('true' if isAdditiveNumber(num) else 'false')\n",
        "test_cases": [
            {"input": "112358", "expected_output": "true"},
            {"input": "199100199", "expected_output": "true"},
            {"input": "1203", "expected_output": "false"},
            {"input": "101", "expected_output": "true"},
        ]
    },
    # ---- 8. 目标和 ----
    {
        "title": "目标和",
        "difficulty": "Medium",
        "tags": ["动态规划", "回溯", "背包"],
        "source": "LeetCode #494",
        "source_url": "https://leetcode.cn/problems/target-sum/",
        "description": """## 题目描述

给你一个非负整数数组 `nums` 和一个整数 `target`。

向数组中的每个整数前添加 `+` 或 `-`，然后串联起所有整数，可以构造一个 **表达式**。返回可以通过上述方法构造的、运算结果等于 `target` 的不同表达式的数目。

### 示例

```
输入: nums = [1,1,1,1,1], target = 3
输出: 5
解释: 共 5 种方法让最终目标和为 3:
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
```

### 约束

- `1 <= nums.length <= 20`
- `0 <= nums[i] <= 1000`
- `-1000 <= target <= 1000`

### 提示

可转化为 0-1 背包问题：设正数子集之和为 P，则 P = (sum + target) / 2，问题变为在 nums 中选取若干数使和为 P。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n, target = map(int, input().split())\n    nums = list(map(int, input().split()))\n    # 输出方案数\n    pass\n\nsolve()\n",
        "lc_template": "def findTargetSumWays(nums, target):\n    # 返回方案数\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn, target = map(int, input().split())\nnums = list(map(int, input().split()))\nprint(findTargetSumWays(nums, target))\n",
        "test_cases": [
            {"input": "5 3\n1 1 1 1 1", "expected_output": "5"},
            {"input": "1 1\n1", "expected_output": "1"},
            {"input": "5 5\n1 1 1 1 1", "expected_output": "1"},
        ]
    },
    # ---- 9. 分隔链表 (Partition List) ----
    {
        "title": "分隔链表",
        "difficulty": "Medium",
        "tags": ["链表", "双指针"],
        "source": "LeetCode #86",
        "source_url": "https://leetcode.cn/problems/partition-list/",
        "description": """## 题目描述

给你一个链表的头节点 `head` 和一个特定值 `x`，请你对链表进行分隔，使得所有 **小于** `x` 的节点都出现在 **大于或等于** `x` 的节点之前。

你应当保留两个分区中每个节点的初始相对顺序。

### 示例

```
输入: head = [1,4,3,2,5,2], x = 3
输出: [1,2,2,4,3,5]
```

```
输入: head = [2,1], x = 2
输出: [1,2]
```

### 约束

- 节点数目在 `[0, 200]` 范围内
- `-100 <= Node.val <= 100`
- `-200 <= x <= 200`

### 提示

创建两个哑节点分别收集小于 x 和大于等于 x 的节点，最后拼接。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n, x = map(int, input().split())\n    vals = list(map(int, input().split()))\n    # 模拟链表分隔，输出结果序列\n    pass\n\nsolve()\n",
        "lc_template": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef partition(head, x):\n    # 返回分隔后的链表头节点\n    pass\n",
        "lc_wrapper": _LIST_HELPERS + "\nn, x = map(int, input().split())\nvals = list(map(int, input().split()))\nhead = _build_list(vals)\nresult = partition(head, x)\n_print_list(result)\n",
        "test_cases": [
            {"input": "6 3\n1 4 3 2 5 2", "expected_output": "1 2 2 4 3 5"},
            {"input": "2 2\n2 1", "expected_output": "1 2"},
            {"input": "0 0", "expected_output": ""},
        ]
    },
    # ---- 10. 分隔链表 (Split Linked List in Parts) ----
    {
        "title": "分隔链表为k部分",
        "difficulty": "Medium",
        "tags": ["链表"],
        "source": "LeetCode #725",
        "source_url": "https://leetcode.cn/problems/split-linked-list-in-parts/",
        "description": """## 题目描述

给你一个头节点为 `head` 的单链表和一个整数 `k`，请你设计一个算法将链表分隔为 `k` 个连续的部分。

每部分的长度应该尽可能的相等：任意两部分的长度差距不能超过 1。前面的部分的长度应该大于或等于后面的部分的长度。

返回一个由上述 `k` 部分组成的数组。

### 示例

```
输入: head = [1,2,3], k = 5
输出: [[1],[2],[3],[],[]]
```

```
输入: head = [1,2,3,4,5,6,7,8,9,10], k = 3
输出: [[1,2,3,4],[5,6,7],[8,9,10]]
```

### 约束

- 节点数目在 `[0, 1000]` 范围内
- `1 <= k <= 50`

### 提示

先计算链表长度，然后 divmod(length, k) 得到每部分的基础长度和多出来几个，前 remainder 个部分多分一个节点。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n, k = map(int, input().split())\n    vals = list(map(int, input().split())) if n > 0 else []\n    # 每部分输出一行，空部分输出 empty\n    pass\n\nsolve()\n",
        "lc_template": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef splitListToParts(head, k):\n    # 返回包含 k 个链表头节点的列表\n    pass\n",
        "lc_wrapper": _LIST_HELPERS + "\nn, k = map(int, input().split())\nvals = list(map(int, input().split())) if n > 0 else []\nhead = _build_list(vals)\nparts = splitListToParts(head, k)\nfor part in parts:\n    if part is None:\n        print('empty')\n    else:\n        _print_list(part)\n",
        "test_cases": [
            {"input": "3 5\n1 2 3", "expected_output": "1\n2\n3\nempty\nempty"},
            {"input": "10 3\n1 2 3 4 5 6 7 8 9 10", "expected_output": "1 2 3 4\n5 6 7\n8 9 10"},
        ]
    },
    # ---- 11. 小于n的最大数 ----
    {
        "title": "小于n的最大数",
        "difficulty": "Medium",
        "tags": ["DFS", "贪心", "回溯"],
        "source": "面试高频",
        "source_url": "",
        "description": """## 题目描述

给定一个由数字组成的集合 `digits`（数字范围 1-9，不含 0）和一个正整数 `n`，从 `digits` 中选取数字（可重复选取），组成一个小于 `n` 的最大数。

### 示例

```
输入: digits = [1,2,9], n = 920
输出: 919
```

```
输入: digits = [5,9], n = 100
输出: 99
```

```
输入: digits = [2,3,8], n = 230
输出: 228
```

### 约束

- `1 <= digits.length <= 9`
- `1 <= digits[i] <= 9`，无重复
- `1 <= n <= 10^9`

### 提示

DFS + 回溯：逐位构建，维护 `is_smaller` 标记。当 `is_smaller=True` 时后续所有位取最大数字；否则尝试取小于当前位的最大数字，或相等数字（进入下一位递归）。如果所有位都相等无法变小，则减少一位，每位填最大数字。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    digits = list(map(int, input().split()))\n    n = int(input())\n    # 输出小于 n 的最大数\n    pass\n\nsolve()\n",
        "lc_template": "def largestSmaller(digits, n):\n    # 返回小于 n 的最大数\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\ndigits = list(map(int, input().split()))\nn = int(input())\nprint(largestSmaller(digits, n))\n",
        "test_cases": [
            {"input": "1 2 9\n920", "expected_output": "919"},
            {"input": "5 9\n100", "expected_output": "99"},
            {"input": "2 3 8\n230", "expected_output": "228"},
            {"input": "1 2\n21", "expected_output": "12"},
        ]
    },
    # ---- 12. 最小的n个因子的数 ----
    {
        "title": "恰好有n个因子的最小正整数",
        "difficulty": "Medium",
        "tags": ["数学", "质因数", "DFS"],
        "source": "面试高频",
        "source_url": "",
        "description": """## 题目描述

给定正整数 `n`，求恰好有 `n` 个因子（包括 1 和自身）的最小正整数。

### 示例

```
输入: 1
输出: 1
解释: 1 只有 1 个因子
```

```
输入: 4
输出: 6
解释: 6 的因子为 1,2,3,6 共 4 个
```

```
输入: 12
输出: 60
解释: 60 的因子为 1,2,3,4,5,6,10,12,15,20,30,60 共 12 个
```

### 约束

- `1 <= n <= 1000`

### 提示

因子个数公式：若 `x = p1^a1 * p2^a2 * ...`，则因子数 = `(a1+1)(a2+1)...`。将 n 质因数分解后，把指数降序排列分配给最小的质数 2, 3, 5, 7... 可得最小结果。用 DFS 枚举 n 的因式分解方式，取使结果最小的方案。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    # 输出恰好有 n 个因子的最小正整数\n    pass\n\nsolve()\n",
        "lc_template": "def smallestWithNDivisors(n):\n    # 返回恰好有 n 个因子的最小正整数\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nprint(smallestWithNDivisors(n))\n",
        "test_cases": [
            {"input": "1", "expected_output": "1"},
            {"input": "4", "expected_output": "6"},
            {"input": "12", "expected_output": "60"},
            {"input": "24", "expected_output": "360"},
        ]
    },
    # ---- 13. 两两交换链表中的节点 ----
    {
        "title": "两两交换链表中的节点",
        "difficulty": "Medium",
        "tags": ["链表", "递归"],
        "source": "LeetCode #24",
        "source_url": "https://leetcode.cn/problems/swap-nodes-in-pairs/",
        "description": """## 题目描述

给你一个链表，两两交换其中相邻的节点，并返回交换后链表的头节点。你必须在不修改节点内部的值的情况下完成本题（即只能进行节点交换）。

### 示例

```
输入: head = [1,2,3,4]
输出: [2,1,4,3]
```

```
输入: head = [1]
输出: [1]
```

### 约束

- 节点数目在 `[0, 100]` 范围内
- `0 <= Node.val <= 100`
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    vals = list(map(int, input().split())) if n > 0 else []\n    # 两两交换后输出\n    pass\n\nsolve()\n",
        "lc_template": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\ndef swapPairs(head):\n    # 返回交换后的链表头节点\n    pass\n",
        "lc_wrapper": _LIST_HELPERS + "\nn = int(input())\nvals = list(map(int, input().split())) if n > 0 else []\nhead = _build_list(vals)\nresult = swapPairs(head)\n_print_list(result)\n",
        "test_cases": [
            {"input": "4\n1 2 3 4", "expected_output": "2 1 4 3"},
            {"input": "1\n1", "expected_output": "1"},
            {"input": "5\n1 2 3 4 5", "expected_output": "2 1 4 3 5"},
        ]
    },
    # ---- 14. 二叉树的最近公共祖先 ----
    {
        "title": "二叉树的最近公共祖先",
        "difficulty": "Medium",
        "tags": ["树", "DFS", "递归"],
        "source": "LeetCode #236",
        "source_url": "https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/",
        "description": """## 题目描述

给定一个二叉树，找到该树中两个指定节点的最近公共祖先（LCA）。

最近公共祖先的定义为：对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。

### 示例

```
输入: root = [3,5,1,6,2,0,8,-1,-1,7,4], p = 5, q = 1
输出: 3
```

```
输入: root = [3,5,1,6,2,0,8,-1,-1,7,4], p = 5, q = 4
输出: 5
```

### 约束

- 树中节点数目在 `[2, 10^5]` 范围内
- 所有节点的值都是唯一的
- `p != q`
- p 和 q 均存在于给定的二叉树中

### 输入格式 (ACM)

第一行：节点数 n，然后 n 个值（层序遍历，-1 表示 null），最后一行两个值 p q。
""",
        "template_code": "import sys\nfrom collections import deque\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    vals = list(map(int, input().split()))\n    p, q = map(int, input().split())\n    # 构建树并求 LCA，输出 LCA 的值\n    pass\n\nsolve()\n",
        "lc_template": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef lowestCommonAncestor(root, p, q):\n    # p, q 是 TreeNode 节点，返回 LCA 节点\n    pass\n",
        "lc_wrapper": _TREE_HELPERS + "\nn = int(input())\nvals = list(map(int, input().split()))\npv, qv = map(int, input().split())\nroot = _build_tree(vals)\np = _find_node(root, pv)\nq = _find_node(root, qv)\nresult = lowestCommonAncestor(root, p, q)\nprint(result.val)\n",
        "test_cases": [
            {"input": "11\n3 5 1 6 2 0 8 -1 -1 7 4\n5 1", "expected_output": "3"},
            {"input": "11\n3 5 1 6 2 0 8 -1 -1 7 4\n5 4", "expected_output": "5"},
        ]
    },
    # ---- 15. 二叉树的最大宽度 ----
    {
        "title": "二叉树的最大宽度",
        "difficulty": "Medium",
        "tags": ["树", "BFS"],
        "source": "LeetCode #662",
        "source_url": "https://leetcode.cn/problems/maximum-width-of-binary-tree/",
        "description": """## 题目描述

给你一棵二叉树的根节点 `root`，返回树的 **最大宽度**。

树的最大宽度是所有层中最大的宽度。每一层的宽度被定义为该层最左和最右的非空节点之间的长度（包含 null 节点）。

### 示例

```
输入: root = [1,3,2,5,3,-1,9]
输出: 4
解释: 第 3 层宽度为 4 (5,3,null,9)
```

```
输入: root = [1,3,2,5,-1,-1,-1]
输出: 2
```

### 约束

- 树中节点数目范围是 `[1, 3000]`

### 提示

BFS 层序遍历，给每个节点编号（根为 1，左子 2i，右子 2i+1），每层宽度 = 最右编号 - 最左编号 + 1。
""",
        "template_code": "import sys\nfrom collections import deque\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    vals = list(map(int, input().split()))\n    # 构建树并求最大宽度\n    pass\n\nsolve()\n",
        "lc_template": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\ndef widthOfBinaryTree(root):\n    # 返回最大宽度\n    pass\n",
        "lc_wrapper": _TREE_HELPERS + "\nn = int(input())\nvals = list(map(int, input().split()))\nroot = _build_tree(vals)\nprint(widthOfBinaryTree(root))\n",
        "test_cases": [
            {"input": "7\n1 3 2 5 3 -1 9", "expected_output": "4"},
            {"input": "5\n1 3 2 5 -1", "expected_output": "2"},
            {"input": "1\n1", "expected_output": "1"},
        ]
    },
    # ---- 16. 字典序的第K小数字 ----
    {
        "title": "字典序的第K小数字",
        "difficulty": "Hard",
        "tags": ["字典树", "数学"],
        "source": "LeetCode #440",
        "source_url": "https://leetcode.cn/problems/k-th-smallest-in-lexicographical-order/",
        "description": """## 题目描述

给定整数 `n` 和 `k`，返回 `[1, n]` 中字典序第 `k` 小的数字。

### 示例

```
输入: n = 13, k = 2
输出: 10
解释: 字典序排列为 [1,10,11,12,13,2,3,4,5,6,7,8,9]，第 2 小是 10
```

```
输入: n = 1, k = 1
输出: 1
```

### 约束

- `1 <= k <= n <= 10^9`

### 提示

将 1~n 看作十叉字典树。关键函数 `count(prefix, n)` 计算以 prefix 为前缀的数字个数。从 prefix=1 开始，如果 count <= k-1 则跳到下一个兄弟节点 prefix+1（k 减去 count），否则深入 prefix*10（k 减 1）。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n, k = map(int, input().split())\n    # 输出字典序第 k 小的数字\n    pass\n\nsolve()\n",
        "lc_template": "def findKthNumber(n, k):\n    # 返回字典序第 k 小的数字\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn, k = map(int, input().split())\nprint(findKthNumber(n, k))\n",
        "test_cases": [
            {"input": "13 2", "expected_output": "10"},
            {"input": "1 1", "expected_output": "1"},
            {"input": "100 10", "expected_output": "17"},
        ]
    },
    # ---- 17. 序列切分使方差和最大 ----
    {
        "title": "序列切分使两部分方差和最大",
        "difficulty": "Medium",
        "tags": ["数学", "前缀和", "枚举"],
        "source": "面试高频",
        "source_url": "",
        "description": """## 题目描述

给定一个长度为 n 的正整数序列，将其切分为两个非空的连续部分，使得两部分的方差之和最大。输出这个最大方差之和（保留 4 位小数）。

方差公式：`Var(X) = E(X^2) - E(X)^2 = (sum_sq / cnt) - (sum / cnt)^2`

### 示例

```
输入: 4
1 2 3 4
输出: 0.5000
解释: 切分为 [1] 和 [2,3,4]，方差分别为 0 和 2/3，和为 0.6667
或切分为 [1,2,3] 和 [4]，方差分别为 2/3 和 0，和为 0.6667
或切分为 [1,2] 和 [3,4]，方差分别为 0.25 和 0.25，和为 0.5
最大为 0.6667
```

### 约束

- `2 <= n <= 10^5`
- `1 <= a[i] <= 10^6`

### 提示

枚举切分点，动态维护左右两部分的 sum 和 sum_sq，用化简后的方差公式 O(1) 计算每个切分方案的方差和。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    a = list(map(int, input().split()))\n    # 输出最大方差和，保留 4 位小数\n    pass\n\nsolve()\n",
        "lc_template": "def maxVarianceSum(a):\n    # 返回最大方差和 (float)\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\na = list(map(int, input().split()))\nprint(f'{maxVarianceSum(a):.4f}')\n",
        "test_cases": [
            {"input": "4\n1 2 3 4", "expected_output": "0.6667"},
            {"input": "2\n1 1", "expected_output": "0.0000"},
            {"input": "3\n1 1 100", "expected_output": "2178.0000"},
        ]
    },
    # ---- 18. LRU 缓存 ----
    {
        "title": "LRU 缓存",
        "difficulty": "Medium",
        "tags": ["哈希表", "链表", "设计"],
        "source": "LeetCode #146",
        "source_url": "https://leetcode.cn/problems/lru-cache/",
        "description": """## 题目描述

请你设计并实现一个满足 LRU（最近最少使用）缓存约束的数据结构。

实现 `LRUCache` 类：

- `LRUCache(int capacity)` 以正整数作为容量初始化 LRU 缓存
- `int get(int key)` 如果关键字存在于缓存中，则返回其值，否则返回 -1
- `void put(int key, int value)` 如果关键字已经存在，则变更其值；如果不存在，则插入。当缓存容量达到上限时，在写入新数据前删除最久未使用的数据值。

`get` 和 `put` 必须以 O(1) 的时间复杂度运行。

### 示例

```
输入:
capacity = 2
put 1 1
put 2 2
get 1      -> 1
put 3 3    (淘汰 key 2)
get 2      -> -1
put 4 4    (淘汰 key 1)
get 1      -> -1
get 3      -> 3
get 4      -> 4
```

### 约束

- `1 <= capacity <= 3000`
- `0 <= key <= 10^4`

### 输入格式 (ACM)

第一行：容量 capacity 和操作数 m。后续 m 行：`get key` 或 `put key value`。对 get 操作输出结果。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    cap, m = map(int, input().split())\n    # 实现 LRU 缓存\n    # 对每个 get 操作输出结果\n    for _ in range(m):\n        line = input().split()\n        pass\n\nsolve()\n",
        "lc_template": "class LRUCache:\n    def __init__(self, capacity):\n        pass\n\n    def get(self, key):\n        # 返回值或 -1\n        pass\n\n    def put(self, key, value):\n        pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\ncap, m = map(int, input().split())\ncache = LRUCache(cap)\nfor _ in range(m):\n    line = input().split()\n    if line[0] == 'get':\n        print(cache.get(int(line[1])))\n    else:\n        cache.put(int(line[1]), int(line[2]))\n",
        "test_cases": [
            {"input": "2 9\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nput 4 4\nget 1\nget 3\nget 4", "expected_output": "1\n-1\n-1\n3\n4"},
            {"input": "1 5\nput 1 10\nget 1\nput 2 20\nget 1\nget 2", "expected_output": "10\n-1\n20"},
        ]
    },
    # ---- 19. 实现前缀树 (Trie) ----
    {
        "title": "实现前缀树",
        "difficulty": "Medium",
        "tags": ["字典树", "设计", "哈希表"],
        "source": "LeetCode #208",
        "source_url": "https://leetcode.cn/problems/implement-trie-prefix-tree/",
        "description": """## 题目描述

实现 Trie（前缀树）类：

- `Trie()` 初始化前缀树对象
- `void insert(String word)` 向前缀树中插入字符串 word
- `boolean search(String word)` 如果字符串 word 在前缀树中，返回 true；否则返回 false
- `boolean startsWith(String prefix)` 如果之前已经插入的字符串中有以 prefix 为前缀的，返回 true；否则返回 false

### 示例

```
insert("apple")
search("apple")     -> true
search("app")       -> false
startsWith("app")   -> true
insert("app")
search("app")       -> true
```

### 约束

- `1 <= word.length, prefix.length <= 2000`
- `word` 和 `prefix` 仅由小写英文字母组成

### 提示

每个 TrieNode 维护一个 `children` 哈希表（char -> TrieNode）和 `is_end` 标记。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    m = int(input())\n    # 实现 Trie\n    for _ in range(m):\n        line = input().split()\n        # insert word / search word / startsWith prefix\n        pass\n\nsolve()\n",
        "lc_template": "class Trie:\n    def __init__(self):\n        # children: dict[char, TrieNode], is_end: bool\n        pass\n\n    def insert(self, word):\n        pass\n\n    def search(self, word):\n        # 返回 bool\n        pass\n\n    def startsWith(self, prefix):\n        # 返回 bool\n        pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nm = int(input())\ntrie = Trie()\nfor _ in range(m):\n    parts = input().split()\n    op = parts[0]\n    arg = parts[1]\n    if op == 'insert':\n        trie.insert(arg)\n    elif op == 'search':\n        print('true' if trie.search(arg) else 'false')\n    elif op == 'startsWith':\n        print('true' if trie.startsWith(arg) else 'false')\n",
        "test_cases": [
            {"input": "6\ninsert apple\nsearch apple\nsearch app\nstartsWith app\ninsert app\nsearch app", "expected_output": "true\nfalse\ntrue\ntrue"},
            {"input": "4\ninsert hello\nsearch hell\nstartsWith hell\nsearch hello", "expected_output": "false\ntrue\ntrue"},
        ]
    },
    # ---- 20. 寻找峰值 ----
    {
        "title": "寻找峰值",
        "difficulty": "Medium",
        "tags": ["数组", "二分查找"],
        "source": "LeetCode #162",
        "source_url": "https://leetcode.cn/problems/find-peak-element/",
        "description": """## 题目描述

峰值元素是指其值严格大于左右相邻值的元素。

给你一个整数数组 `nums`，找到峰值元素并返回其索引。数组可能包含多个峰值，在这种情况下，返回 **任何一个** 峰值所在位置即可。

你可以假设 `nums[-1] = nums[n] = -∞`。

你必须实现时间复杂度为 `O(log n)` 的算法来解决此问题。

### 示例

```
输入: nums = [1,2,3,1]
输出: 2
解释: 3 是峰值元素，返回其索引 2
```

```
输入: nums = [1,2,1,3,5,6,4]
输出: 5
解释: 返回索引 1 或 5 均可
```

### 约束

- `1 <= nums.length <= 1000`
- `nums[i] != nums[i + 1]`

### 提示

二分查找：比较 nums[mid] 和 nums[mid+1]，如果 nums[mid] < nums[mid+1] 则峰值在右半边，否则在左半边。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    nums = list(map(int, input().split()))\n    # 输出峰值的索引\n    pass\n\nsolve()\n",
        "lc_template": "def findPeakElement(nums):\n    # 返回峰值元素的索引\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nnums = list(map(int, input().split()))\nidx = findPeakElement(nums)\nprint(idx)\n",
        "test_cases": [
            {"input": "4\n1 2 3 1", "expected_output": "2"},
            {"input": "1\n1", "expected_output": "0"},
        ]
    },
    # ---- 21. 最长连续序列 ----
    {
        "title": "最长连续序列",
        "difficulty": "Medium",
        "tags": ["数组", "哈希表"],
        "source": "LeetCode #128",
        "source_url": "https://leetcode.cn/problems/longest-consecutive-sequence/",
        "description": """## 题目描述

给定一个未排序的整数数组 `nums`，找出数字连续的最长序列（不要求数组中的元素在原始位置上连续）的长度。

请你设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

### 示例

```
输入: nums = [100,4,200,1,3,2]
输出: 4
解释: 最长数字连续序列是 [1,2,3,4]，长度为 4
```

```
输入: nums = [0,3,7,2,5,8,4,6,0,1]
输出: 9
```

### 约束

- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

### 提示

将所有数放入 HashSet。遍历每个数 num，若 num-1 不在 set 中（说明 num 是连续序列的起点），则向后扩展计数。
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    nums = list(map(int, input().split())) if n > 0 else []\n    # 输出最长连续序列的长度\n    pass\n\nsolve()\n",
        "lc_template": "def longestConsecutive(nums):\n    # 返回最长连续序列的长度\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nnums = list(map(int, input().split())) if n > 0 else []\nprint(longestConsecutive(nums))\n",
        "test_cases": [
            {"input": "6\n100 4 200 1 3 2", "expected_output": "4"},
            {"input": "10\n0 3 7 2 5 8 4 6 0 1", "expected_output": "9"},
            {"input": "0", "expected_output": "0"},
        ]
    },
    # ---- 22. 最小的n ----
    {
        "title": "最小的n",
        "difficulty": "Medium",
        "tags": ["数学", "质因数分解"],
        "source": "字节跳动面试真题",
        "source_url": "",
        "description": """## 题目描述

给定一个正整数 $n$，你可以对这个正整数进行两种操作：

1. 将 $n$ 乘以任意一个正整数
2. 将 $n$ 开方变成 $\\sqrt{n}$，注意如果要执行开方操作，$n$ 必须是完全平方数

你可以执行上述两个操作任意多次，求可能得到的最小的 $n$ 是多少？若实现最小的 $n$，最少需要执行几次操作？

输出两个整数，分别为最小值和最少操作次数，空格分隔。

### 示例

```
输入: 256
输出: 2 3
解释: 256=2^8 → sqrt→16=2^4 → sqrt→4=2^2 → sqrt→2   (3 次开方)
```

```
输入: 72
输出: 6 3
解释: 72=2^3*3^2 → *18→1296=2^4*3^4 → sqrt→36=2^2*3^2 → sqrt→6   (1 次乘法 + 2 次开方)
```

### 约束

- `1 <= n <= 10^9`

### 提示

1. 对 n 做质因数分解，最小值 = 各质因子的乘积（无平方因子核）
2. 设最大指数为 e_max，需要 k = ceil(log2(e_max)) 次开方
3. 如果所有指数恰好都等于 2^k，则不需要乘法操作，总次数 = k；否则需要 1 次乘法将所有指数补齐到 2^k，总次数 = k + 1
""",
        "template_code": "import sys\ninput = sys.stdin.readline\n\ndef solve():\n    n = int(input())\n    # 输出最小值和最少操作次数\n    pass\n\nsolve()\n",
        "lc_template": "def minN(n):\n    # 返回 (最小值, 最少操作次数)\n    pass\n",
        "lc_wrapper": "import sys\ninput = sys.stdin.readline\nn = int(input())\nval, ops = minN(n)\nprint(val, ops)\n",
        "test_cases": [
            {"input": "256", "expected_output": "2 3"},
            {"input": "72", "expected_output": "6 3"},
            {"input": "36", "expected_output": "6 1"},
            {"input": "12", "expected_output": "6 2"},
            {"input": "1", "expected_output": "1 0"},
            {"input": "7", "expected_output": "7 0"},
        ]
    },
]


# ==================== 核心代码模式输入格式模板 ====================
# 语法: {N} 整行, {N:M} 第N行第M个token, {N[]} 第N行格式化为数组, {N..mat} 第N行起每行作为子数组
_INPUT_FMT = {
    "两数之和":             "nums = {2[]}, target = {1:2}",
    "最长递增子序列":       "nums = {2[]}",
    "接雨水":               "height = {2[]}",
    "合并区间":             "intervals = {2..mat}",
    "岛屿数量":             "grid = {2..mat}",
    "移掉K位数字":          'num = "{1}", k = {2}',
    "累加数":               'num = "{1}"',
    "目标和":               "nums = {2[]}, target = {1:2}",
    "分隔链表":             "head = {2[]}, x = {1:2}",
    "分隔链表为k部分":      "head = {2[]}, k = {1:2}",
    "小于n的最大数":        "digits = {1[]}, n = {2}",
    "恰好有n个因子的最小正整数": "n = {1}",
    "两两交换链表中的节点": "head = {2[]}",
    "二叉树的最近公共祖先": "tree = {2[]}, p = {3:1}, q = {3:2}",
    "二叉树的最大宽度":     "tree = {2[]}",
    "字典序的第K小数字":    "n = {1:1}, k = {1:2}",
    "序列切分使两部分方差和最大": "a = {2[]}",
    "LRU 缓存":            "capacity = {1:1}\n{2..}",
    "实现前缀树":           "{2..}",
    "寻找峰值":             "nums = {2[]}",
    "最长连续序列":         "nums = {2[]}",
    "最小的n":              "n = {1}",
}

# 将格式模板注入到题目数据中
for _p in SAMPLE_PROBLEMS:
    if _p['title'] in _INPUT_FMT:
        _p['lc_input_fmt'] = _INPUT_FMT[_p['title']]


def seed():
    """插入示例数据（按标题去重，支持增量添加新题 + 补充字段）"""
    existing = {p['title']: p for p in db.list_problems()}
    count = 0
    for p in SAMPLE_PROBLEMS:
        if p['title'] in existing:
            # 补充已有题目缺失的字段
            ep = existing[p['title']]
            updates = {}
            if not ep.get('lc_template') and p.get('lc_template'):
                updates['lc_template'] = p['lc_template']
                updates['lc_wrapper'] = p.get('lc_wrapper', '')
            if not ep.get('lc_input_fmt') and p.get('lc_input_fmt'):
                updates['lc_input_fmt'] = p['lc_input_fmt']
            if updates:
                db.update_problem(ep['id'], **updates)
            continue
        pid = db.create_problem(
            title=p["title"],
            description=p["description"],
            difficulty=p["difficulty"],
            tags=p["tags"],
            source=p["source"],
            source_url=p["source_url"],
            template_code=p["template_code"],
            lc_template=p.get("lc_template", ""),
            lc_wrapper=p.get("lc_wrapper", ""),
            lc_input_fmt=p.get("lc_input_fmt", ""),
        )
        for tc in p["test_cases"]:
            db.add_test_case(pid, tc["input"], tc["expected_output"])
        count += 1
    return count


if __name__ == "__main__":
    db.init_db()
    n = seed()
    print(f"已插入 {n} 道示例题目")
