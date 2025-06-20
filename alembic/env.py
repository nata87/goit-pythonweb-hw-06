import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv
from database.models import Base 

load_dotenv()
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)
fileConfig(config.config_file_name)
target_metadata = Base.metadata
