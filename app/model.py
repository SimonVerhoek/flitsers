from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Melding(Base):
	__tablename__ = 'melding'
	id = Column(Integer, primary_key=True, nullable=False)
	datum = Column(Date, nullable=False, default=datetime.now())
	soort_weg = Column(String, nullable=False)
	wegnummer = Column(String, nullable=False)
	zijde = Column(String, nullable=False)
	hm_paal = Column(Float, nullable=False)
	type_controle = Column(String, nullable=False)
	tijd_van_melden = Column(Time, nullable=False)
	details = Column(String)

engine = create_engine('sqlite:///flitsers.db')

# create db with above classes as tables
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)