from sqlalchemy import create_engine
from datamodel import Base

engine = create_engine('sqlite:///webBrowser.db')
Base.metadata.create_all(engine)