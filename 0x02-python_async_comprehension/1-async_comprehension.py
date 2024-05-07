#!/usr/bin/env python3

'''
Module for Async Comprehensions
'''

import asyncio
async_generator = __import__('0-async_generator').async_generator

async def async_comprehension():
    '''
    collect 10 random numbers using an async comprehensing over async_generator
    '''
    number = [i async for i in async_generator()]
    
    return number
    