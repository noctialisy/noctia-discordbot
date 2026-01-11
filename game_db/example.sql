-- Entities definition
CREATE TABLE Entities (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid TEXT,
	ent_type TEXT,
	name TEXT,	
	surname TEXT,
	gender TEXT,
	race TEXT,
	height INTEGER,
	weight INTEGER,
	nsfw INTEGER,
	description TEXT,
	backstory TEXT,
	char_role BLOB,
	char_level INTEGER DEFAULT (1),
	role_level INTEGER DEFAULT (1),
	mhp INTEGER DEFAULT (0),
	mmp INTEGER DEFAULT (0),
	msp INTEGER DEFAULT (0),
	hp INTEGER DEFAULT (0),
	mp INTEGER DEFAULT (0),
	sp INTEGER DEFAULT (0),
	ac INTEGER DEFAULT (10),
	cur_exp INTEGER DEFAULT (0),
	req_exp INTEGER DEFAULT (0),
	raw_stats TEXT,
	stat_point INTEGER DEFAULT (0),
	stats TEXT,
	skills TEXT,
	abilities TEXT,
	inventory TEXT
);


-- Abilities definition
CREATE TABLE Abilities (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	role_id INTEGER,
	role_name TEXT,
	name TEXT,
	description TEXT,
	description_ext TEXT,
	usage_line_cast TEXT,
	usage_line_success TEXT,
	usage_line_fail TEXT,
	req_role TEXT,
	req_level INTEGER,
	req_hp INTEGER,
	req_mp INTEGER,
	req_sp INTEGER,
	positive_effects TEXT,
	negative_effects TEXT
);


-- Roles definition
CREATE TABLE Roles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	hit_dice TEXT,
	magic_dice TEXT,
	special_dice TEXT
);