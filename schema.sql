CREATE TABLE IF NOT EXISTS rating(
  id serial primary key,
  usertoken varchar(255),
  item int,
  rate int,
  ratetype int
) DEFAULT CHARACTER SET=utf8;
 
CREATE TABLE IF NOT EXISTS item (
  id serial primary key,
  imgpath varchar(255), 
  category int
) DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS category (
  id serial primary key,
  categoryname varchar(255), 
  enabled boolean default 1
) DEFAULT CHARACTER SET=utf8;

CREATE TABLE IF NOT EXISTS webuser (
  id serial primary key,
  usertoken varchar(255),
  username varchar(255)
) DEFAULT CHARACTER SET=utf8;
 