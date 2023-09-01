import asyncio
from logging.config import fileConfig
from alembic import context
from src.database.sql.postgres_conn import database
from sqlalchemy import engine_from_config, pool
from src.database.sql.alchemy_models import Base

# Об'єкт конфігурації Alembic, який надає доступ до значень у використовуваному .ini файлі.
config = context.config

# Інтерпретація конфігураційного файлу для Python логування. Цей рядок налаштовує логери.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Додайте об'єкт MetaData вашої моделі тут для підтримки 'autogenerate'.
target_metadata = Base.metadata

# Ініціалізуйте асинхронне підключення до бази даних.
database_url = config.get_main_option("sqlalchemy.url")
db = database(database_url)

async def run_migrations_async():
    # Налаштування пула підключення до бази даних та ініціалізація об'єкту engine.
    async with db.transaction():  # Замість database.transaction()
        engine = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    async with engine.begin() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            # Використовуйте asyncio.run() для виконання міграцій асинхронно.
            await asyncio.run(context.run_migrations())

async def run_migrations_offline_async():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        # Використовуйте asyncio.run() для виконання міграцій асинхронно.
        await asyncio.run(context.run_migrations())

# Перевірте, чи Alembic працює в автономному режимі (offline mode).
if context.is_offline_mode():
    asyncio.run(run_migrations_offline_async())
else:
    asyncio.run(run_migrations_async())
