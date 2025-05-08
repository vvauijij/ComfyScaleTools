#!/usr/bin/env python3
"""
async_load_test.py

Asynchronous load-testing script using aiohttp and asyncio.
- Generates N distinct prompts via PromptGenerator subclasses.
- Distributes equal load across a list of hosts.
- Fires all requests simultaneously using an asyncio barrier.

Usage:
    python async_load_test.py --workflow simple --hosts http://h1:8188 http://h2:8188 ... \
                              --requests 100 \
                              [--concurrency 50]
"""

import asyncio
import argparse
from typing import List
from aiohttp import ClientSession, TCPConnector

from generators.simple_generator import SimplePromptGenerator
from generators.network_generator import NetworkPromptGenerator
from generators.networkLoadSave_generator import NetworkLoadSavePromptGenerator
from generators.parallel_generator import ParallelPromptGenerator
from generators.tryOn_generator import TryOnPromptGenerator
from generators.video_generator import VideoPromptGenerator
from generators.design_generator import DesignPromptGenerator


WORKFLOW_REGISTRY = {
    SimplePromptGenerator.WORKFLOW_TYPE: SimplePromptGenerator,
    NetworkPromptGenerator.WORKFLOW_TYPE: NetworkPromptGenerator,
    NetworkLoadSavePromptGenerator.WORKFLOW_TYPE: NetworkLoadSavePromptGenerator,
    ParallelPromptGenerator.WORKFLOW_TYPE: ParallelPromptGenerator,
    TryOnPromptGenerator.WORKFLOW_TYPE: TryOnPromptGenerator,
    VideoPromptGenerator.WORKFLOW_TYPE: VideoPromptGenerator,
    DesignPromptGenerator.WORKFLOW_TYPE: DesignPromptGenerator,
}


async def worker(
    host: str, payload: dict, start_evt: asyncio.Event, session: ClientSession, idx: int
):
    """Wait for the start event, then POST payload to host/prompt."""
    await start_evt.wait()
    url = f"{host.rstrip('/')}/prompt"
    try:
        async with session.post(url, json=payload) as resp:
            await resp.text()
    except Exception as e:
        print(f"[{idx}] {host} -> ERROR: {e}")


async def run_load_test(
    hosts: List[str], requests_per_host: int, concurrency: int, workflow: str
):
    if workflow not in WORKFLOW_REGISTRY:
        raise ValueError(
            f"Unknown workflow '{workflow}'. "
            f"Choose from: {', '.join(WORKFLOW_REGISTRY)}"
        )
    gen_cls = WORKFLOW_REGISTRY[workflow]
    gen = gen_cls(requests_per_host)

    total_requests = requests_per_host * len(hosts)
    payloads = [gen.generate() for _ in range(total_requests)]

    # Round-robin assign payloads to hosts
    assignments = []
    idx = 0
    for host in hosts:
        for _ in range(requests_per_host):
            assignments.append((host, payloads[idx], idx))
            idx += 1

    # Barrier event to start all at once
    start_evt = asyncio.Event()

    connector = TCPConnector(limit=concurrency)
    async with ClientSession(connector=connector) as session:
        tasks = [
            asyncio.create_task(worker(h, p, start_evt, session, i))
            for i, (h, p, _) in enumerate(assignments)
        ]

        # brief pause to allow tasks to initialize
        await asyncio.sleep(1)
        start_evt.set()
        await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description="Async load test for ComfyUI API.")
    parser.add_argument(
        "--workflow",
        choices=list(WORKFLOW_REGISTRY.keys()),
        default="warmup",
        help="Which prompt workflow to use",
    )
    parser.add_argument(
        "--hosts",
        nargs="+",
        required=True,
        help="List of host URLs, e.g. http://h1:8188 http://h2:8188",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=100,
        help="Number of requests per host (default: 100)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=10,
        help="Max concurrent connections (default: 10)",
    )
    args = parser.parse_args()

    asyncio.run(
        run_load_test(args.hosts, args.requests, args.concurrency, args.workflow)
    )


if __name__ == "__main__":
    main()
