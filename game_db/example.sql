-- Entities definition
CREATE TABLE Entities (
	id INT PRIMARY KEY auto_increment,
	uid TEXT,
	ent_type TEXT,
	name TEXT,	
	surname TEXT,
	gender TEXT,
	race TEXT,
	height INT,
	weight INT,
	nsfw INT,
	description TEXT,
	backstory TEXT,
	char_role BLOB,
	char_level INT DEFAULT (1),
	role_level INT DEFAULT (1),
	mhp INT DEFAULT (0),
	mmp INT DEFAULT (0),
	msp INT DEFAULT (0),
	hp INT DEFAULT (0),
	mp INT DEFAULT (0),
	sp INT DEFAULT (0),
	ac INT DEFAULT (10),
	cur_exp INT DEFAULT (0),
	req_exp INT DEFAULT (0),
	raw_stats TEXT,
	stat_point INT DEFAULT (0),
	stats TEXT,
	skills TEXT,
	abilities TEXT,
	inventory TEXT
);


-- Abilities definition
CREATE TABLE Abilities (
	id INT PRIMARY KEY auto_increment,
	role_id INT,
	role_name TEXT,
	name TEXT,
	description TEXT,
	description_ext TEXT,
	usage_line_cast TEXT,
	usage_line_success TEXT,
	usage_line_fail TEXT,
	req_role TEXT,
	req_level INT,
	req_hp INT,
	req_mp INT,
	req_sp INT,
	positive_effects TEXT,
	negative_effects TEXT
);


-- Roles definition
CREATE TABLE Roles (
	id INT PRIMARY KEY auto_increment,
	name TEXT,
	hit_dice TEXT,
	magic_dice TEXT,
	special_dice TEXT
);