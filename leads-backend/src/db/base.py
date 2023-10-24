import os

from databases import Database
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()


lead = Table(
    "lead",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("email", String(50)),
    Column("address", String(50)),
    Column("phone", String(50)),
    Column("inscription_year", DateTime, nullable=True),
    Column("career_id", Integer, ForeignKey("career.id"), nullable=False),
    Column("number_of_times_taken", Integer, nullable=False),
    Column("created_date", DateTime, nullable=True),
)

career = Table(
    "career",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
)

course = Table(
    "course",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("lead_id", ForeignKey("lead.id", ondelete="CASCADE")),
    Column("career_id", ForeignKey("career.id", ondelete="CASCADE")),
)


# databases query builder
database = Database(DATABASE_URL)
