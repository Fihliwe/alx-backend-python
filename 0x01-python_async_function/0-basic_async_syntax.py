#!/usr/bin/env python3

'''
Module for asynchronous coroutine
'''
import asyncio
import random

async def wait_random(max_delay=10) -> float:
    delay = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
    