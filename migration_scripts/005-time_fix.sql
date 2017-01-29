ALTER TABLE 
	melding 
ALTER COLUMN 
	tijd_van_melden TYPE time 
USING 
	tijd_van_melden::time without time zone;