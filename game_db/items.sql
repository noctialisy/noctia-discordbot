CREATE TABLE `Items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text DEFAULT NULL,
  `item_type` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `item_price` int(11) DEFAULT NULL,
  `attack_type` text DEFAULT NULL,
  `dice_roll` text DEFAULT NULL,
  `base_drop_rate` float DEFAULT NULL,
  `map_drop_rate` float DEFAULT NULL,
  `effects` text DEFAULT NULL,
  PRIMARY KEY (`id`)
);