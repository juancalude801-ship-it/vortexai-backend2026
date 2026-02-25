import asyncio
from app.jobs.worker import run_cycle

if __name__ == "__main__":
    asyncio.run(run_cycle())
