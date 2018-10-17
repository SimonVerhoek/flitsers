CREATE TABLE melding(
	id INTEGER PRIMARY KEY,
	datum DATE NOT NULL,
	soort_weg VARCHAR NOT NULL,
	wegnummer VARCHAR NOT NULL,
	zijde VARCHAR NOT NULL,
	hm_paal VARCHAR NOT NULL,
	type_controle VARCHAR NOT NULL,
	tijd_van_melden VARCHAR NOT NULL,
	details VARCHAR,
	laatste_activiteit TIME WITHOUT TIME ZONE
);
	
