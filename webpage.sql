

CREATE TABLE `webpage` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) DEFAULT NULL,
  `code` int(10) unsigned default 0,
  `head` text NULL, 
  `content` text NULL, 
  `error` varchar(512) NULL,
  `text` text NULL,
  `title` varchar(2048) NULL,
  `status` int(11) DEFAULT NULL,
  `score` float DEFAULT NULL,
  `outlinks` text NULL,
  `modified_time` int(10) unsigned NULL,
  `prev_modified_time` int(10) unsigned NULL,
  `fetch_interval` int(10) unsigned NULL,
  `prev_fetch_time` int(10) unsigned NULL,
  `fetch_time` int(10) unsigned NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM   DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;
