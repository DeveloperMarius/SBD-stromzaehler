from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os


class Database:

    def __init__(self):
        print(f"sqlite://{os.path.dirname(os.path.realpath(__file__))}/../res/messstellenbetreiber.db")
        engine = create_engine(f"sqlite:///{os.path.dirname(os.path.realpath(__file__))}/../res/messstellenbetreiber.db", echo=True)
        self.session = Session(engine)



