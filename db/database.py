class Database:
    def __init__(self, conn):
        self.conn = conn

    async def sql_get_user_id(self, user_id):
        query = "SELECT user_id FROM user_info WHERE user_id = $1 LIMIT 1"
        return await self.conn.fetchval(query, user_id)

    async def sql_create_user(self, user_id, lexicon, datetime):
        query = "INSERT INTO user_info (user_id, lexicon, datetime) VALUES ($1, $2, $3)"
        await self.conn.execute(query, user_id, lexicon, datetime)
        return True

    async def sql_update_language(self, lexicon, user_id):
        query = "UPDATE user_info SET lexicon = $1 WHERE user_id = $2"
        await self.conn.execute(query, lexicon, user_id)
        return True
