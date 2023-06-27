async def create_table(pool):
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_info (
                user_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                lexicon TEXT,
                datetime TEXT
            )
        """)
