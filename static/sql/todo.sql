SET FOREIGN_KEY_CHECKS=0;
-- ---------------------------
-- Table structure for cover
-- ---------------------------
CREATE database IF NOT EXISTS `cover`;

CREATE TABLE `cover_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL,
  `last_change` timestamp NOT NULL,
  `name` varchar(256) NOT NULL,
  `album_name` varchar(64) NOT NULL,
  `artist` varchar(64) NOT NULL,
  `year_record` char(32) NOT NULL,
  `music_contain` varchar(512) NOT NULL,
  `type` char(32) NOT NULL,
  `type_id` int(11) NOT NULL,
  `cover_path` varchar(512) NOT NULL,
  `width` smallint(5) NOT NULL,
  `height` smallint(5) NOT NULL,
  `file_size` int(11) NOT NULL,
  `kind` char(16) NOT NULL,
  `des` varchar(1024),
  `read_num` int(11) DEFAULT '0',
  `like_num` int(11) DEFAULT '0',
  `star` int(11) DEFAULT '0',

  `print_num` int(11) DEFAULT '0',
  `other_num` int(11) DEFAULT '0',
  `other_str` char(32) DEFAULT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
-- ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;


-- ---------------------------
-- Records
-- ---------------------------
-- INSERT INTO `cover` VALUES ('4', 'title4', '0', '2011-06-03 06:08:10');
-- INSERT INTO `cover` VALUES ('5', 'title5', '1', '2011-06-04 23:01:31');
