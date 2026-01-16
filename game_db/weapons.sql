CREATE TABLE `Weapons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `attack_type` text DEFAULT NULL,
  `dice_roll` text DEFAULT NULL,
  PRIMARY KEY (`id`)
);