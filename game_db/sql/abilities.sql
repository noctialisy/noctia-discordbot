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
)