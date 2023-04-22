CREATE TABLE IF NOT EXISTS doctor (
  username VARCHAR(50) PRIMARY KEY,
  password VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS patient (
  username VARCHAR(50) PRIMARY KEY,
  password VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS patient_profile (
    username VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    dob varchar(10) NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    address VARCHAR(100) NOT NULL


);
