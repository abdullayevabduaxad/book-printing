import aiosqlite

DATABASE = 'bot.db'

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                fullname TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                file_path TEXT,
                file_name TEXT,
                format TEXT,
                color TEXT,
                method TEXT,
                price REAL,
                copy_count INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')
        await db.commit()

async def add_user(user_id: int, fullname: str, phone: str):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''
            INSERT OR REPLACE INTO users (user_id, fullname, phone)
            VALUES (?, ?, ?)
        ''', (user_id, fullname, phone))
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('''
            SELECT fullname, phone FROM users WHERE user_id = ?
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row if row else None

async def add_order(user_id, file_path, file_name, format_choice, color_choice, method_choice, copy_count, total_cost):
    async with aiosqlite.connect('bot.db') as db:
        await db.execute('''
            INSERT INTO orders (user_id, file_path, file_name, format, color, method, copy_count, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, file_path, file_name, format_choice, color_choice, method_choice, copy_count, total_cost))
        await db.commit()

async def get_orders(user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('''
            SELECT file_name, format, color, method, price FROM orders WHERE user_id = ?
        ''', (user_id,)) as cursor:
            rows = await cursor.fetchall()
            return rows if rows else []
