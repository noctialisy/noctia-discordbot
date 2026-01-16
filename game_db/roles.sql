CREATE TABLE `Roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text DEFAULT NULL,
  `hit_dice` text DEFAULT NULL,
  `magic_dice` text DEFAULT NULL,
  `special_dice` text DEFAULT NULL,
  `main_stat` text DEFAULT NULL,
  `sub_stat` text DEFAULT NULL,
  PRIMARY KEY (`id`)
);