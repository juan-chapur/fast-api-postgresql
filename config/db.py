from sqlalchemy import create_engine, MetaData

# connection special to postgresql
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/storedb")

meta = MetaData()

conn = engine.connect()