from datetime import date, datetime, time

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

from consts import ZONNESTANDEN


Base = declarative_base()


class DictSerializable(object):
    def _asdict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            value = getattr(self, key)
            if (
                isinstance(value, datetime)
                or isinstance(value, time)
                or isinstance(value, date)
            ):
                value = value.isoformat()
            result[key] = value
        return result


""" MODELS """


class Melding(Base, DictSerializable):
    __tablename__ = "melding"
    id = Column(Integer, primary_key=True, autoincrement=True)
    datum = Column(DateTime, nullable=False, default=datetime.now())
    soort_weg = Column(String, nullable=False)
    wegnummer = Column(String, nullable=False)
    zijde = Column(String, nullable=False)
    hm_paal = Column(String, nullable=False)
    type_controle = Column(String, nullable=False)
    tijd_van_melden = Column(Time, nullable=False)
    details = Column(String)
    laatste_activiteit = Column(DateTime)
    locatie = Column(String)
    locatie_lat = Column(Float)
    locatie_lon = Column(Float)
    weer_type = Column(String)
    weer_beschrijving = Column(String)
    weer_temp = Column(Float)
    weer_temp_max = Column(Float)
    weer_temp_min = Column(Float)
    weer_luchtdruk_hpa = Column(Integer)
    weer_luchtvochtigheid_procent = Column(Integer)
    weer_windsnelheid_m_per_sec = Column(Float)
    weer_windrichting_graden = Column(Integer)
    weer_bewolking_procent = Column(Integer)
    weer_regen_mm = Column(Float)
    weer_sneeuw_mm = Column(Float)
    weer_zonnestand = Column(Enum(*ZONNESTANDEN))
    weer_locatie_naam = Column(String)


class Town(Base):
    __tablename__ = "town"
    code = Column(Integer, primary_key=True)
    name = Column(String)
    municipality = Column(String)
    province = Column(String)


# create db with above classes as tables
# Base.metadata.create_all(engine)
