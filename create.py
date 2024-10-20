from database import engine, Base
from models import Item

print("creating database...")

Base.metadata.create_all(engine)
