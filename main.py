import tables
from database import engine
from bot import start_bot

tables.Base.metadata.create_all(bind=engine)
start_bot()