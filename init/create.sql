CREATE TABLE cognnectuser (
  username VARCHAR NOT NULL, 
  email VARCHAR NOT NULL, 
  password VARCHAR NOT NULL, 
  pastrecords VARCHAR NOT NULL, 
  dorp VARCHAR NOT NULL
);

CREATE TABLE stroop (
  username VARCHAR NOT NULL, 
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  compatibleTime INT NOT NULL,
  incompatibleTime INT NOT NULL,
  timeDifference INT NOT NULL
);

CREATE TABLE tilt (
  username VARCHAR NOT NULL,
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  leftAngle FLOAT NOT NULL,
  rightAngle FLOAT NOT NULL
);

CREATE TABLE chats (
    patient VARCHAR NOT NULL,
    doctor VARCHAR NOT NULL,
    uuid VARCHAR NOT NULL UNIQUE
);


-- CREATE TABLE <uuid> (
--     user VARCHAR NOT NULL,
--     line TEXT NOT NULL,
--     ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );