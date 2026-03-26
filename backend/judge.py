"""
判题引擎 - 安全执行用户代码并比对输出
"""
import subprocess
import sys
import os
import tempfile
import time
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class CaseResult:
    case_id: int
    status: str        # AC / WA / TLE / RE / PE
    time_ms: float
    input: str
    expected: str
    actual: str
    error: str = ""


@dataclass
class JudgeResult:
    status: str            # Accepted / Wrong Answer / Time Limit Exceeded / Runtime Error
    total_time_ms: float
    passed_cases: int
    total_cases: int
    detail: List[dict]


def normalize_output(text: str) -> str:
    """标准化输出：去除行尾空格和末尾空行"""
    lines = text.rstrip().split('\n')
    return '\n'.join(line.rstrip() for line in lines)


def run_code(code: str, input_data: str, timeout: float = 5.0) -> tuple:
    """
    运行用户代码
    返回: (stdout, stderr, time_ms, timed_out)
    """
    # 写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='/tmp') as f:
        f.write(code)
        tmp_path = f.name

    try:
        start = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, '-u', tmp_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={
                'PATH': os.environ.get('PATH', ''),
                'HOME': '/tmp',
                'PYTHONIOENCODING': 'utf-8',
            }
        )
        elapsed = (time.perf_counter() - start) * 1000
        return proc.stdout, proc.stderr, elapsed, False
    except subprocess.TimeoutExpired:
        elapsed = (time.perf_counter() - start) * 1000
        return "", "Time Limit Exceeded", elapsed, True
    except Exception as e:
        return "", str(e), 0, False
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def judge(code: str, test_cases: list, timeout: float = 5.0,
          mode: str = 'acm', lc_wrapper: str = '') -> JudgeResult:
    """
    判题主函数
    code: 用户提交的代码
    test_cases: [{"id": ..., "input": ..., "expected_output": ...}, ...]
    timeout: 每个用例的超时时间(秒)
    mode: 'acm' 或 'core'
    lc_wrapper: LeetCode 模式下的驱动代码（拼接在用户代码之后）
    返回: JudgeResult
    """
    if mode == 'core' and lc_wrapper:
        code = code + '\n' + lc_wrapper
    results = []
    passed = 0
    total_time = 0
    overall_status = "Accepted"

    for tc in test_cases:
        case_id = tc.get('id', 0)
        input_data = tc.get('input', '')
        expected = tc.get('expected_output', '')

        stdout, stderr, time_ms, timed_out = run_code(code, input_data, timeout)
        total_time += time_ms

        if timed_out:
            status = "TLE"
            if overall_status == "Accepted":
                overall_status = "Time Limit Exceeded"
            results.append(asdict(CaseResult(
                case_id=case_id, status=status, time_ms=time_ms,
                input=input_data, expected=expected, actual="", error="超时"
            )))
            continue

        if stderr and not stdout:
            status = "RE"
            if overall_status == "Accepted":
                overall_status = "Runtime Error"
            # 清理 traceback，只保留关键错误信息
            error_lines = stderr.strip().split('\n')
            short_error = error_lines[-1] if error_lines else stderr
            results.append(asdict(CaseResult(
                case_id=case_id, status=status, time_ms=time_ms,
                input=input_data, expected=expected, actual="",
                error=short_error
            )))
            continue

        actual = normalize_output(stdout)
        exp_normalized = normalize_output(expected)

        if actual == exp_normalized:
            status = "AC"
            passed += 1
        else:
            status = "WA"
            if overall_status == "Accepted":
                overall_status = "Wrong Answer"

        results.append(asdict(CaseResult(
            case_id=case_id, status=status, time_ms=time_ms,
            input=input_data, expected=expected, actual=actual,
            error=stderr.strip() if stderr else ""
        )))

    return JudgeResult(
        status=overall_status,
        total_time_ms=total_time,
        passed_cases=passed,
        total_cases=len(test_cases),
        detail=results
    )
