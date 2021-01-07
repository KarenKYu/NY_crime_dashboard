DROP TABLE IF EXISTS complaints CASCADE;
DROP TABLE IF EXISTS locations CASCADE;
DROP TABLE IF EXISTS incidents;

CREATE TABLE IF NOT EXISTS complaints (
  id serial PRIMARY KEY,
  desc_offense VARCHAR(255),
  level_offense VARCHAR(255),
  dept_juris VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS locations (
  id serial PRIMARY KEY,
  borough VARCHAR(255),
  latitude DECIMAL,
  longitude DECIMAL,
  setting VARCHAR(255),
  precinct INTEGER
);

CREATE TABLE IF NOT EXISTS incidents (
  id serial PRIMARY KEY,
  incident_num INTEGER UNIQUE,
  complaint_id INTEGER NOT NULL,
  incident_date DATE,
  incident_time TIME,
  location_id INTEGER NOT NULL,
  CONSTRAINT fk_location
  FOREIGN KEY (location_id) 
  REFERENCES locations(id)
  ON DELETE CASCADE,
  CONSTRAINT fk_complaint
  FOREIGN KEY (complaint_id) 
  REFERENCES complaints(id)
  ON DELETE CASCADE
);