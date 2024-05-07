#!/usr/bin/env python3

'''
Module for  four parallel comprehensions
'''

from asyncio import gather
from time import time

async_comprehension = __import__('1-async_comprehension').sync_comprehension


async  def measure_runtime():
    '''
    execute async_comprehension four times in parallel using asyncio.gather.
    '''
    start = time()
    tasks = [async_comprehension() for i in range(4)]
    await gather(*tasks)
    end = time()
    return (end - start)