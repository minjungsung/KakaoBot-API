-- PostgreSQL dump

-- Host: localhost    Database: chatbot
-- ------------------------------------------------------
-- PostgreSQL version

-- Set standard_conforming_strings to on
SET standard_conforming_strings = on;

-- Drop tables if they exist
DROP TABLE IF EXISTS alembic_version CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS enhancement_game CASCADE;
DROP TABLE IF EXISTS enhancement_guiness CASCADE;
DROP TABLE IF EXISTS enhancement_history CASCADE;
DROP TABLE IF EXISTS menues CASCADE;
DROP TABLE IF EXISTS sentences CASCADE;

-- Table structure for table `alembic_version`
CREATE TABLE alembic_version (
  version_num varchar(32) NOT NULL,
  PRIMARY KEY (version_num)
);

-- Table structure for table `chats`
CREATE TABLE chats (
  id SERIAL PRIMARY KEY,
  room varchar(300),
  sender varchar(300),
  msg text,
  isGroupChat boolean DEFAULT NULL,
  create_date timestamp without time zone DEFAULT NULL,
  update_date timestamp without time zone DEFAULT NULL
);

-- Table structure for table `enhancement_game`
CREATE TABLE enhancement_game (
  id SERIAL PRIMARY KEY,
  "user" varchar(300) DEFAULT NULL,
  item_name varchar(300) DEFAULT NULL,
  item_level int DEFAULT NULL,
  room varchar(300) DEFAULT NULL,
  create_date timestamp without time zone DEFAULT NULL,
  update_date timestamp without time zone DEFAULT NULL
);

-- Table structure for table `enhancement_guiness`
CREATE TABLE enhancement_guiness (
  id SERIAL PRIMARY KEY,
  "user" varchar(300) DEFAULT NULL,
  item_name varchar(300) DEFAULT NULL,
  item_level int DEFAULT NULL,
  room varchar(300) DEFAULT NULL,
  create_date timestamp without time zone DEFAULT NULL,
  update_date timestamp without time zone DEFAULT NULL
);

-- Table structure for table `enhancement_history`
CREATE TABLE enhancement_history (
  id SERIAL PRIMARY KEY,
  "user" varchar(300) DEFAULT NULL,
  item_name varchar(300) DEFAULT NULL,
  room varchar(300) DEFAULT NULL,
  before_level int DEFAULT NULL,
  change_level int DEFAULT NULL,
  current_level int DEFAULT NULL,
  create_date timestamp without time zone DEFAULT NULL,
  update_date timestamp without time zone DEFAULT NULL
);

-- Table structure for table `menues`
CREATE TABLE menues (
  id SERIAL PRIMARY KEY,
  sep varchar(300) DEFAULT NULL,
  menu varchar(300) DEFAULT NULL,
  create_date timestamp without time zone DEFAULT NULL,
  update_date timestamp without time zone DEFAULT NULL
);

-- Table structure for table `sentences`
CREATE TABLE sentences (
  id SERIAL PRIMARY KEY,
  sep varchar(30) DEFAULT NULL,
  sentence text,
  create_date timestamp without time zone DEFAULT NULL,
  update_date timestamp without time zone DEFAULT NULL
);