ALTER TABLE melding RENAME COLUMN zijde TO rijrichting;
ALTER TABLE melding ALTER COLUMN type_controle DROP NOT NULL;
