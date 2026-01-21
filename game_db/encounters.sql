CREATE TABLE `Encounters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `encounter_id` int(11) DEFAULT NULL,
  `encounter_type` text DEFAULT NULL,
  `friendly_party` text DEFAULT NULL,
  `enemy_party` text DEFAULT NULL,
  `locked` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
);