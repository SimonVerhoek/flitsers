CREATE TYPE zonnestanden AS ENUM ('voor_zonsopgang', 'na_zonsopgang', 'na_zonsondergang');

ALTER TABLE public.melding ADD COLUMN weer_type TEXT;
ALTER TABLE public.melding ADD COLUMN weer_beschrijving TEXT;
ALTER TABLE public.melding ADD COLUMN weer_temp REAL;
ALTER TABLE public.melding ADD COLUMN weer_temp_max REAL;
ALTER TABLE public.melding ADD COLUMN weer_temp_min REAL;
ALTER TABLE public.melding ADD COLUMN weer_luchtdruk_hpa INTEGER;
ALTER TABLE public.melding ADD COLUMN weer_luchtvochtigheid_procent INTEGER;
ALTER TABLE public.melding ADD COLUMN weer_windsnelheid_m_per_sec REAL;
ALTER TABLE public.melding ADD COLUMN weer_windrichting_graden INTEGER;
ALTER TABLE public.melding ADD COLUMN weer_bewolking_procent INTEGER;
ALTER TABLE public.melding ADD COLUMN weer_regen_mm REAL;
ALTER TABLE public.melding ADD COLUMN weer_sneeuw_mm REAL;
ALTER TABLE public.melding ADD COLUMN weer_zonnestand zonnestanden;
ALTER TABLE public.melding ADD COLUMN weer_locatie_naam TEXT;
