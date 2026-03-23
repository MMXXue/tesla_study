import asyncio
import argparse
import statistics
import time
from collections import Counter

import httpx


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    idx = int((len(values_sorted) - 1) * q)
    return values_sorted[idx]


async def run_once(url: str, total: int, concurrency: int, connect_timeout: float, read_timeout: float, pool_timeout: float):
    sem = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(
        max_connections=concurrency,
        max_keepalive_connections=concurrency,
    )
    timeout = httpx.Timeout(
        connect=connect_timeout,
        read=read_timeout,
        write=read_timeout,
        pool=pool_timeout,
    )

    async def one(client: httpx.AsyncClient, index: int):
        payload = {
            "level": "INFO",
            "message": f"perf-log-{index}",
        }
        async with sem:
            started = time.perf_counter()
            try:
                resp = await client.post(url, json=payload)
                elapsed_ms = (time.perf_counter() - started) * 1000
                return resp.status_code == 200, elapsed_ms, None if resp.status_code == 200 else f"HTTP_{resp.status_code}"
            except Exception as exc:
                elapsed_ms = (time.perf_counter() - started) * 1000
                return False, elapsed_ms, type(exc).__name__

    async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
        begin = time.perf_counter()
        results = await asyncio.gather(*[one(client, i) for i in range(total)])
        end = time.perf_counter()

    success_lat = [lat for ok, lat, _ in results if ok]
    errors = [err for ok, _, err in results if not ok and err is not None]
    success = len(success_lat)
    duration = end - begin
    tps = success / duration if duration > 0 else 0.0

    return {
        "total": total,
        "concurrency": concurrency,
        "success": success,
        "failed": total - success,
        "success_rate": (success / total) * 100 if total else 0,
        "duration_s": duration,
        "tps": tps,
        "avg_ms": statistics.mean(success_lat) if success_lat else 0.0,
        "p50_ms": percentile(success_lat, 0.50),
        "p95_ms": percentile(success_lat, 0.95),
        "p99_ms": percentile(success_lat, 0.99),
        "errors": Counter(errors),
    }


def print_report(result: dict):
    print("\n" + "=" * 60)
    print(f"并发: {result['concurrency']} | 请求: {result['total']}")
    print(f"成功: {result['success']} | 失败: {result['failed']} | 成功率: {result['success_rate']:.2f}%")
    print(f"总耗时: {result['duration_s']:.2f}s | TPS: {result['tps']:.2f}")
    print(
        f"延迟(ms): avg={result['avg_ms']:.2f}, p50={result['p50_ms']:.2f}, "
        f"p95={result['p95_ms']:.2f}, p99={result['p99_ms']:.2f}"
    )
    if result["errors"]:
        print("错误分布:")
        for name, count in result["errors"].most_common():
            print(f"  - {name}: {count}")
    print("=" * 60)


def print_summary(all_results: list[dict]):
    print("\n最佳并发建议（按 TPS 最大且成功率=100% 优先）：")
    complete = [r for r in all_results if r["success_rate"] == 100.0]
    candidates = complete if complete else all_results
    best = max(candidates, key=lambda r: r["tps"])
    print(
        f"  建议并发={best['concurrency']}, TPS={best['tps']:.2f}, "
        f"avg={best['avg_ms']:.2f}ms, p95={best['p95_ms']:.2f}ms"
    )


async def main():
    parser = argparse.ArgumentParser(description="Week2 一键性能基准脚本")
    parser.add_argument("--url", default="http://127.0.0.1:8000/log")
    parser.add_argument("--total", type=int, default=1000)
    parser.add_argument("--concurrency", type=int, nargs="+", default=[10, 20, 30, 40, 50])
    parser.add_argument("--connect-timeout", type=float, default=5.0)
    parser.add_argument("--read-timeout", type=float, default=10.0)
    parser.add_argument("--pool-timeout", type=float, default=30.0)
    args = parser.parse_args()

    print("开始性能扫频...")
    print(f"目标URL: {args.url}")
    print(f"请求总数: {args.total}")
    print(f"并发列表: {args.concurrency}")

    all_results = []
    for c in args.concurrency:
        result = await run_once(
            url=args.url,
            total=args.total,
            concurrency=c,
            connect_timeout=args.connect_timeout,
            read_timeout=args.read_timeout,
            pool_timeout=args.pool_timeout,
        )
        all_results.append(result)
        print_report(result)

    print_summary(all_results)


if __name__ == "__main__":
    asyncio.run(main())
