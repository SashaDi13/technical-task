import asyncio

from celery import shared_task

from .services import run_scraper_async


@shared_task
def run_scraper_task_async():
    asyncio.run(run_scraper_async())