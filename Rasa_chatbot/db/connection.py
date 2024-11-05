from sqlalchemy import create_engine

def connect (DATABASE_URI):
    engine = create_engine(DATABASE_URI)
    return engine
