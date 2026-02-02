"""
One-time script to normalize status values to lowercase.
Run with: python -m scripts.fix_status_case
"""

import asyncio
from sqlalchemy import text
from src.core.database import engine


async def fix_status_case():
    async with engine.begin() as conn:
        result = await conn.execute(
            text("UPDATE processes SET status = LOWER(status) WHERE status != LOWER(status)")
        )
        print(f"Updated {result.rowcount} processes")

        # Also fix process_type and automation fields if needed
        result2 = await conn.execute(
            text("UPDATE processes SET process_type = LOWER(process_type) WHERE process_type != LOWER(process_type)")
        )
        print(f"Updated {result2.rowcount} process_type values")

        result3 = await conn.execute(
            text("UPDATE processes SET current_automation = LOWER(current_automation) WHERE current_automation != LOWER(current_automation)")
        )
        print(f"Updated {result3.rowcount} current_automation values")


if __name__ == "__main__":
    asyncio.run(fix_status_case())
