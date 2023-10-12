from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, field_serializer


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MeldingSchema(BaseSchema):
    id: int
    datum: date
    soort_weg: str
    wegnummer: str
    zijde: str
    hm_paal: str
    type_controle: str
    tijd_van_melden: time
    details: str
    laatste_activiteit: time | None
    locatie: str | None
    locatie_lat: float | None
    locatie_lon: float | None
    weer_type: str | None
    weer_beschrijving: str | None
    weer_temp: float | None
    weer_temp_max: float | None
    weer_temp_min: float | None
    weer_luchtdruk_hpa: int | None
    weer_luchtvochtigheid_procent: int | None
    weer_windsnelheid_m_per_sec: float | None
    weer_windrichting_graden: int | None
    weer_bewolking_procent: int | None
    weer_regen_mm: float | None
    weer_sneeuw_mm: float | None
    weer_zonnestand: str | None
    weer_locatie_naam: str | None

    @field_serializer("datum")
    def serialize_datum(self, datum: date):
        return datetime.strftime(datum, "%Y-%m-%d")

    @field_serializer("tijd_van_melden")
    def serialize_tijd_van_melden(self, tijd_van_melden: time):
        return time.strftime(tijd_van_melden, "%H:%M:%S")

    @field_serializer("laatste_activiteit")
    def serialize_laatste_activiteit(self, laatste_activiteit: time):
        return (
            time.strftime(laatste_activiteit, "%H:%M:%S") if laatste_activiteit else ""
        )
