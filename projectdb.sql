/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50719
Source Host           : localhost:3306
Source Database       : projectdb

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2018-06-10 10:28:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `admin`
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `absent_std` int(11) DEFAULT NULL,
  `absent_level_warn` int(11) DEFAULT NULL,
  `late_absent` datetime DEFAULT NULL,
  `notice` varchar(200) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `last_modify_time` (`last_modify_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------

-- ----------------------------
-- Table structure for `callname`
-- ----------------------------
DROP TABLE IF EXISTS `callname`;
CREATE TABLE `callname` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `checkin_time` datetime DEFAULT NULL,
  `checkin_type` int(11) DEFAULT NULL,
  `checkin_notes` varchar(60) DEFAULT NULL,
  `checkin_grade` float DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  `course_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `checkin_time` (`checkin_time`),
  UNIQUE KEY `last_modify_time` (`last_modify_time`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `callname_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of callname
-- ----------------------------

-- ----------------------------
-- Table structure for `classes`
-- ----------------------------
DROP TABLE IF EXISTS `classes`;
CREATE TABLE `classes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `class_name` varchar(32) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  `profession_id` int(11) DEFAULT NULL,
  `uuid` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profession_id` (`profession_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`profession_id`) REFERENCES `profession` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of classes
-- ----------------------------
INSERT INTO `classes` VALUES ('1', '17专硕1班', '2018-05-14 17:33:28', '5', '33671071-8166-4615-8554-945a150804bf');
INSERT INTO `classes` VALUES ('2', '17专硕2班', '2018-05-14 17:33:28', '6', '97421f36-ff38-4272-a1b2-d15a809a75bd');
INSERT INTO `classes` VALUES ('3', '17电子1班', '2018-05-14 17:33:47', '11', '000b2dfc-da66-4566-9e4a-a3758a32e464');
INSERT INTO `classes` VALUES ('4', '17光电1班', '2018-05-14 17:33:47', '12', '6591f853-85ac-47a4-a5e7-629a747fb8ab');
INSERT INTO `classes` VALUES ('5', '17电子2班', '2018-05-14 17:33:47', '11', '0583cb3a-a3fd-4880-ada6-1bc572fcca00');
INSERT INTO `classes` VALUES ('6', '17光电2班', '2018-05-14 17:33:47', '12', '6e6baa93-a55a-46c9-86ca-7f6428867c97');
INSERT INTO `classes` VALUES ('7', '17英语1班', '2018-06-01 10:20:59', '38', '21434474-c214-4018-8768-4f4a63026e37');
INSERT INTO `classes` VALUES ('8', '17德语1班', '2018-06-01 10:20:59', '40', '1788fffc-7446-401e-b118-ffd30a3ef870');
INSERT INTO `classes` VALUES ('9', '17英语2班', '2018-06-01 10:20:59', '38', '8bf6221d-dab3-4077-a2f1-3962bc468629');
INSERT INTO `classes` VALUES ('10', '17德语2班', '2018-06-01 10:20:59', '40', '78a154ed-505c-4d68-b201-36995677650f');
INSERT INTO `classes` VALUES ('11', '17日语1班', '2018-06-01 10:20:59', '39', '790f31c9-398f-4130-bbdb-9c6ca05e59d5');
INSERT INTO `classes` VALUES ('12', '17日语2班', '2018-06-01 10:20:59', '39', '30af17d1-9a9c-44a5-9154-9a1e5c25f045');
INSERT INTO `classes` VALUES ('13', '17离散1班', '2018-06-01 10:34:21', '7', '8bb0e306-e48d-452b-8b4c-4396b86d058c');
INSERT INTO `classes` VALUES ('14', '17应数1班', '2018-06-01 10:34:21', '8', '97a49cc7-1ba3-4f1a-be7a-a6b04d139e59');
INSERT INTO `classes` VALUES ('15', '17离散2班', '2018-06-01 10:34:21', '7', 'af4e5614-31a8-492f-be6d-6dac6758f341');
INSERT INTO `classes` VALUES ('16', '17应数2班', '2018-06-01 10:34:21', '8', '177c552e-7702-4736-b687-528501c52f4d');
INSERT INTO `classes` VALUES ('17', '17通信1班', '2018-06-01 10:34:21', '9', 'c53f7b52-efff-4f4e-b540-511d1339efd1');
INSERT INTO `classes` VALUES ('18', '17通信2班', '2018-06-01 10:34:21', '9', '776994dc-21f2-44b2-a066-cba3bf4ed97b');
INSERT INTO `classes` VALUES ('19', '17电信1班', '2018-06-01 10:34:21', '10', '40e2ef94-8d0b-4fea-9cdd-572477f5c8b0');
INSERT INTO `classes` VALUES ('20', '17电信2班', '2018-06-01 10:34:21', '10', 'ede9c838-fc33-4350-9321-86c2f5d2bc22');
INSERT INTO `classes` VALUES ('21', '17管科1班', '2018-06-01 10:34:21', '17', '16e5c477-9575-4402-b79e-64993e5606e7');
INSERT INTO `classes` VALUES ('22', '17管科2班', '2018-06-01 10:34:21', '17', '3a8db953-6a05-4832-9616-31852dc675db');
INSERT INTO `classes` VALUES ('23', '17工管1班', '2018-06-01 10:34:21', '18', '5964827c-b460-4c8e-b490-2ef00da622d2');
INSERT INTO `classes` VALUES ('24', '17工管2班', '2018-06-01 10:34:21', '18', '2dfaef31-619d-4bb9-8cbf-b67040d67dbe');
INSERT INTO `classes` VALUES ('25', '17会计1班', '2018-06-01 10:34:21', '22', 'd0d44b70-efe0-4a2e-8bfa-bf8a397b3a1e');
INSERT INTO `classes` VALUES ('26', '17会计2班', '2018-06-01 10:34:21', '22', 'f09dd982-db21-4c99-9398-c8f9a96c7b4f');
INSERT INTO `classes` VALUES ('27', '17建筑1班', '2018-06-01 10:34:21', '27', '9256c2f8-cce3-409e-8cff-f1da30fc2da5');
INSERT INTO `classes` VALUES ('28', '17建筑2班', '2018-06-01 10:34:21', '27', 'ce668c9a-08cd-41af-b285-648e62045975');
INSERT INTO `classes` VALUES ('29', '17城规1班', '2018-06-01 10:34:21', '28', '5918e738-cb7e-4314-a5f3-138379199ec9');
INSERT INTO `classes` VALUES ('30', '17城规2班', '2018-06-01 10:34:21', '28', 'ce5c5cbd-ad7c-435f-8275-050f65c88ea2');
INSERT INTO `classes` VALUES ('31', '17风圆1班', '2018-06-01 10:34:21', '29', 'f60a3624-4b28-4cda-a36b-317aef9a8f30');
INSERT INTO `classes` VALUES ('32', '17风圆2班', '2018-06-01 10:34:21', '29', 'f9da780f-1101-4233-9b66-a4f7d00322db');
INSERT INTO `classes` VALUES ('33', '17电工1班', '2018-06-01 10:34:21', '31', 'f8506426-7906-4b75-a43a-72e1cb58f004');
INSERT INTO `classes` VALUES ('34', '17电工2班', '2018-06-01 10:34:21', '31', '3da63490-4b2c-4977-a237-242516813e41');
INSERT INTO `classes` VALUES ('35', '17应电1班', '2018-06-01 10:34:21', '32', '0b729b97-b95f-488b-aa42-46dee08efa55');
INSERT INTO `classes` VALUES ('36', '17应电2班', '2018-06-01 10:34:21', '32', '40df19e5-c61a-4477-842b-b0c96993a57b');
INSERT INTO `classes` VALUES ('37', '17自动1班', '2018-06-01 10:34:21', '33', 'c15af521-187b-412d-b60a-44be58cc3376');
INSERT INTO `classes` VALUES ('38', '17自动2班', '2018-06-01 10:34:21', '33', 'bc3310b2-270f-435b-8dfe-88790293e8de');
INSERT INTO `classes` VALUES ('39', '17建工1班', '2018-06-01 10:34:21', '34', '8f9c916c-6081-4590-9ac5-872f3669ae60');
INSERT INTO `classes` VALUES ('40', '17建工2班', '2018-06-01 10:34:21', '34', '49c47857-3498-4249-a00b-37d17c7d95e0');
INSERT INTO `classes` VALUES ('41', '17道桥1班', '2018-06-01 10:34:21', '35', 'cdf12b4a-5db8-4970-9095-06013a226b55');
INSERT INTO `classes` VALUES ('42', '17道桥2班', '2018-06-01 10:34:21', '35', '22f367e8-15ca-4067-8749-76596f255c4f');
INSERT INTO `classes` VALUES ('43', '17市政1班', '2018-06-01 10:34:21', '36', '9a155ac2-6911-4c9e-bc76-ed398a9c27c4');
INSERT INTO `classes` VALUES ('44', '17市政2班', '2018-06-01 10:34:21', '36', '897e60b9-c9e8-4e18-bc90-09ddbc9a17f0');
INSERT INTO `classes` VALUES ('45', '17交通1班', '2018-06-01 10:34:21', '37', '08dbaaab-8cd7-4c7d-87ef-d11597dca531');
INSERT INTO `classes` VALUES ('46', '17交通2班', '2018-06-01 10:34:21', '37', 'cb06511b-5a76-4370-ab86-7254c844f0b9');
INSERT INTO `classes` VALUES ('51', 'sss', '2018-06-08 11:27:10', '6', '71902659-fb88-4dce-86ce-b5f2fa4847cf');

-- ----------------------------
-- Table structure for `colleague`
-- ----------------------------
DROP TABLE IF EXISTS `colleague`;
CREATE TABLE `colleague` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `colea_name` varchar(32) DEFAULT NULL,
  `uuid` varchar(40) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `colea_name` (`colea_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of colleague
-- ----------------------------
INSERT INTO `colleague` VALUES ('1', '数计学院', '1d58b8d0-52f3-4d53-a699-7fb90c87616f', '2018-05-09 05:26:36');
INSERT INTO `colleague` VALUES ('2', '经管学院', 'f0d8dcea-08ca-4435-83ba-07611562e8ec', '2018-05-09 05:26:36');
INSERT INTO `colleague` VALUES ('3', '建筑学院', '96d174c2-9341-4091-8b33-8bb78b7e8ef4', '2018-05-09 05:26:36');
INSERT INTO `colleague` VALUES ('4', '电气学院', '31f4c255-ce6d-4d2b-b04b-b3dfaae4b75f', '2018-05-09 05:26:36');
INSERT INTO `colleague` VALUES ('5', '土木学院', '5834a004-2a7f-4e91-a183-b876da0f38f1', '2018-05-09 05:26:36');
INSERT INTO `colleague` VALUES ('6', '物信学院', '5da3e6ad-e79a-4a84-b4c1-93f1ae3eebe9', '2018-05-09 05:26:36');
INSERT INTO `colleague` VALUES ('7', '外国语学院', '7666c813-152e-4aca-a95b-cd7dce058ac8', '2018-05-09 06:10:25');

-- ----------------------------
-- Table structure for `course`
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `course_number` varchar(60) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_name` varchar(32) DEFAULT NULL,
  `course_week_times` int(11) DEFAULT NULL,
  `semester` varchar(32) DEFAULT NULL,
  `course_time` varchar(32) DEFAULT NULL,
  `position` varchar(32) DEFAULT NULL,
  `course_members` int(11) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  `profession_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `profession_id` (`profession_id`),
  KEY `course_number` (`course_number`) USING BTREE,
  CONSTRAINT `course_ibfk_1` FOREIGN KEY (`profession_id`) REFERENCES `profession` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES ('UDREEUEUEEED', '1', '工程训练', '11', '2017-2018学年第二学期', '周一', '东二 2#506', '56', '2018-05-26 16:16:18', '5');
INSERT INTO `course` VALUES ('UCREEUEUEEEF', '2', '算法设计', '10', '2017-2018学年第二学期', '周一', '东二 2#507', '78', '2018-05-26 16:16:45', '5');
INSERT INTO `course` VALUES ('UEREEUEUEEET', '3', '专业英语', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '23', '2018-05-26 16:17:27', '5');
INSERT INTO `course` VALUES ('UCREEUEUEEEJ', '4', '数值计算', '10', '2017-2018学年第二学期', '周一', '东二 3#506', '45', '2018-05-26 16:17:27', '5');
INSERT INTO `course` VALUES ('UPREEUEUEEEB', '5', '软件体系结构', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '67', '2018-05-26 16:17:27', '5');
INSERT INTO `course` VALUES ('URREEUEUEEEF', '6', '软件工程', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '89', '2018-05-26 16:17:27', '5');
INSERT INTO `course` VALUES ('UMREEUEUEEEK', '7', '自然辨证法', '10', '2017-2018学年第二学期', '周一', '东二 5#506', '56', '2018-05-26 16:17:27', '5');
INSERT INTO `course` VALUES ('UDREEUEUEEED', '9', '智能技术', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '12', '2018-05-26 16:17:28', '5');
INSERT INTO `course` VALUES ('UVREEUEUEEEW', '10', '知识产权', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '23', '2018-05-26 16:17:28', '5');
INSERT INTO `course` VALUES ('UWREEUEUEEEQ', '11', '信息检索', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '34', '2018-05-26 16:17:28', '5');
INSERT INTO `course` VALUES ('UZREEUEUEEEX', '12', '数学', '10', '2017-2018学年第二学期', '周一', '东二 2#506', '56', '2018-05-26 16:17:28', '5');
INSERT INTO `course` VALUES ('UCREEUEUEEEF', '25', '算法设计', '11', '2017-2018学年第二学期', '周一', '东二 2#507', '78', '2018-05-31 20:24:00', '5');
INSERT INTO `course` VALUES ('UQREEUEUEEEL', '27', '英语', '19', '2017-2018学年第二学期', '周一', '东二 2#506', '50', '2018-05-31 20:26:05', '5');

-- ----------------------------
-- Table structure for `menu`
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `order` smallint(6) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `menu_type` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES ('1', '学生管理', 'fa fa-table', null, '1', '0', '1', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('2', '学生列表', 'fa fa-table', '/student_management/student_list', '11', '1', '2', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('3', '教师管理', 'fa fa-table', null, '2', '0', '1', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('4', '教师列表', 'fa fa-table', '/teacher_management/teacher_list', '21', '3', '2', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('5', '课程管理', 'fa fa-table', null, '3', '0', '1', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('6', '课程列表', 'fa fa-table', '/course_management/course_list', '31', '5', '2', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('7', '数据权限管理', 'fa fa-table', null, '4', '0', '1', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('8', '组织管理', 'fa fa-table', '/settings_management/level_management', '41', '7', '2', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('9', '权限管理', 'fa fa-table', '/settings_management/permission_management', '42', '7', '2', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('10', '角色管理', 'fa fa-table', '/settings_management/role_management', '43', '7', '2', '2018-05-30 21:06:40');
INSERT INTO `menu` VALUES ('15', '授课安排', 'fa fa-table', '/course_management/course_arrange', '32', '5', '2', '2018-06-09 21:34:05');
INSERT INTO `menu` VALUES ('16', '课表查询', 'fa fa-table', '/course_management/course_query', '33', '5', '2', '2018-06-09 21:34:05');

-- ----------------------------
-- Table structure for `permission`
-- ----------------------------
DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `action` varchar(60) DEFAULT NULL,
  `perm_desc` varchar(100) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of permission
-- ----------------------------
INSERT INTO `permission` VALUES ('1', '学生管理', '/student_management/', '学生管理', '2018-05-22 20:27:06');
INSERT INTO `permission` VALUES ('2', '注册', null, '注册权限', '2018-06-08 17:00:01');
INSERT INTO `permission` VALUES ('5', '注册', null, '注册权限', '2018-06-08 17:02:30');

-- ----------------------------
-- Table structure for `profession`
-- ----------------------------
DROP TABLE IF EXISTS `profession`;
CREATE TABLE `profession` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prof_name` varchar(32) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  `uuid` varchar(40) DEFAULT NULL,
  `colleague_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `prof_name` (`prof_name`),
  KEY `colleague_id` (`colleague_id`),
  CONSTRAINT `profession_ibfk_1` FOREIGN KEY (`colleague_id`) REFERENCES `colleague` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of profession
-- ----------------------------
INSERT INTO `profession` VALUES ('5', '计算机技术', '2018-05-09 06:21:20', '73f8b312-3750-4c94-af81-ad50b78e5411', '1');
INSERT INTO `profession` VALUES ('6', '软件工程', '2018-05-09 06:21:20', 'acd336de-0751-43ba-90c1-a2db17bf9431', '1');
INSERT INTO `profession` VALUES ('7', '离散中心', '2018-05-09 06:21:20', 'ad0fb026-3dec-4551-80fd-21e83c93c3d9', '1');
INSERT INTO `profession` VALUES ('8', '应用数学', '2018-05-09 06:21:20', '52506383-14b3-404f-b5cc-a8ddb82abc16', '1');
INSERT INTO `profession` VALUES ('9', '通信工程', '2018-05-09 06:26:00', '9dc58051-dadd-41d5-be94-335fefb0c2ec', '6');
INSERT INTO `profession` VALUES ('10', '电子信息工程', '2018-05-09 06:26:00', '8934e177-7282-4c62-bbe2-99eae30ea7f7', '6');
INSERT INTO `profession` VALUES ('11', '电子科学与技术', '2018-05-09 06:26:00', 'e5085fd7-8e63-41fd-aac8-ed8809638c1c', '6');
INSERT INTO `profession` VALUES ('12', '光电信息工程', '2018-05-09 06:26:00', '85ced2d0-b141-40e2-b736-3f705e01067e', '6');
INSERT INTO `profession` VALUES ('17', '管理科学与工程', '2018-05-09 06:29:03', '33cf51df-3f78-4226-a0cc-ae740f42fd61', '2');
INSERT INTO `profession` VALUES ('18', '工商管理', '2018-05-09 06:29:03', '09473e66-33d6-41a1-90df-c229a8274623', '2');
INSERT INTO `profession` VALUES ('22', '会计学', '2018-05-09 06:29:03', '8c2a92eb-1430-488e-bd7f-90e3970487b1', '2');
INSERT INTO `profession` VALUES ('27', '建筑学', '2018-05-31 22:08:17', 'ba6708cd-596c-4228-9b3f-54abe066d4dd', '3');
INSERT INTO `profession` VALUES ('28', '城乡规划', '2018-05-31 22:08:17', '67c5efba-62bb-4128-8ff8-a44d730982f9', '3');
INSERT INTO `profession` VALUES ('29', '风景园林', '2018-05-31 22:08:17', 'e77aa243-d8d6-4794-a21d-f17e1cce9231', '3');
INSERT INTO `profession` VALUES ('31', '电力工程', '2018-05-31 22:08:17', '26eb9783-6ba3-459d-92f1-2566be369bd5', '4');
INSERT INTO `profession` VALUES ('32', '应用电子', '2018-05-31 22:08:17', 'ac780491-fbbb-4345-b5d3-4636b7c37ce1', '4');
INSERT INTO `profession` VALUES ('33', '自动化', '2018-05-31 22:08:17', 'b30bb22d-b3a3-4e19-93fd-03b00a8c6643', '4');
INSERT INTO `profession` VALUES ('34', '建筑工程', '2018-05-31 22:08:18', 'c80d931c-ca50-471d-a8d3-a30fe49e3b8c', '5');
INSERT INTO `profession` VALUES ('35', '道路与桥梁工程', '2018-05-31 22:08:18', '265abba3-b938-40c8-a9c6-81378425e86c', '5');
INSERT INTO `profession` VALUES ('36', '市政工程', '2018-05-31 22:08:18', '8e5dbab5-26b9-47a9-b3df-c2caaa087d8e', '5');
INSERT INTO `profession` VALUES ('37', '交通运输工程', '2018-05-31 22:08:18', 'f9200ed0-a1c6-4799-92bd-20aeda1d56a7', '5');
INSERT INTO `profession` VALUES ('38', '英语', '2018-05-31 22:08:18', 'd2b470a5-8a79-46b6-98d7-0a233f4689d1', '7');
INSERT INTO `profession` VALUES ('39', '日语', '2018-05-31 22:08:18', '8a6a1148-1c8e-452f-a9c0-e2db200f3735', '7');
INSERT INTO `profession` VALUES ('40', '德语', '2018-05-31 22:08:18', '33410174-af41-49ce-a699-9d600976324e', '7');

-- ----------------------------
-- Table structure for `role`
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(32) DEFAULT NULL,
  `role_desc` varchar(200) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES ('1', '管理员', '管理员角色', '2018-05-30 12:06:30');
INSERT INTO `role` VALUES ('2', '教师', '教师角色', '2018-05-30 12:06:46');
INSERT INTO `role` VALUES ('3', '学生', '学生角色', '2018-05-30 12:08:04');

-- ----------------------------
-- Table structure for `rolemenu`
-- ----------------------------
DROP TABLE IF EXISTS `rolemenu`;
CREATE TABLE `rolemenu` (
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `display` int(11) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`role_id`,`menu_id`),
  KEY `menu_id` (`menu_id`),
  CONSTRAINT `rolemenu_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `rolemenu_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of rolemenu
-- ----------------------------
INSERT INTO `rolemenu` VALUES ('1', '1', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '2', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '3', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '4', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '5', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '6', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '7', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '8', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '9', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '10', '1', '2018-05-30 21:06:40');
INSERT INTO `rolemenu` VALUES ('1', '15', '1', '2018-06-09 21:39:27');
INSERT INTO `rolemenu` VALUES ('1', '16', '1', '2018-06-09 21:39:27');
INSERT INTO `rolemenu` VALUES ('2', '1', '1', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '2', '1', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '3', '0', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '4', '0', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '5', '1', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '6', '1', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '7', '0', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '8', '0', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '9', '0', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '10', '0', '2018-05-30 21:06:47');
INSERT INTO `rolemenu` VALUES ('2', '15', '1', '2018-06-09 21:34:05');
INSERT INTO `rolemenu` VALUES ('2', '16', '1', '2018-06-09 21:34:05');

-- ----------------------------
-- Table structure for `rolepermission`
-- ----------------------------
DROP TABLE IF EXISTS `rolepermission`;
CREATE TABLE `rolepermission` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  `alloc` int(11) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `rolepermission_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`),
  CONSTRAINT `rolepermission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of rolepermission
-- ----------------------------
INSERT INTO `rolepermission` VALUES ('1', '2', '1', '2018-06-08 17:00:01');
INSERT INTO `rolepermission` VALUES ('2', '5', '0', '2018-06-08 17:02:30');

-- ----------------------------
-- Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(60) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `last_modify_time` (`last_modify_time`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('1', 'Admin', '123456', '2018-05-30 20:05:59', null);
INSERT INTO `user` VALUES ('2', 'Teacher', '123456', '2018-05-31 15:06:34', '2');

-- ----------------------------
-- Table structure for `userinfo`
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(60) DEFAULT NULL,
  `uid` varchar(40) DEFAULT NULL,
  `sex` smallint(6) DEFAULT NULL,
  `avatar` varchar(150) DEFAULT NULL,
  `job_number` varchar(32) DEFAULT NULL,
  `total_grade` float DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `last_modify_time` datetime DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `job_number` (`job_number`),
  KEY `class_id` (`class_id`),
  KEY `userid` (`userid`),
  CONSTRAINT `userinfo_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`),
  CONSTRAINT `userinfo_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES ('1', 'Admin', '6de79739-2195-4d4b-b7e9-7d966c9b660b', '0', null, null, null, '0', '2018-05-30 20:05:59', null, '1');
INSERT INTO `userinfo` VALUES ('97', '鲍尔', null, '0', null, 'N170427094', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('98', '库兹马', null, '0', null, 'N170427096', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('99', '哈特', null, '0', null, 'N170427097', null, '2', '2018-05-30 20:15:49', '5', null);
INSERT INTO `userinfo` VALUES ('100', '兰德尔', null, '0', null, 'N1704270100', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('101', '波普', null, '0', null, 'N170427095', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('102', '威尔', null, '0', null, 'N170427098', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('103', '托马斯', null, '0', null, 'N170427099', null, '2', '2018-05-30 20:15:49', '5', null);
INSERT INTO `userinfo` VALUES ('104', '卡鲁索', null, '0', null, 'N1704270101', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('105', '祖巴茨', null, '0', null, 'N170427093', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('106', '哈登', null, '0', null, 'N170427092', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('107', '保罗', null, '0', null, 'N170427091', null, '2', '2018-05-30 20:15:49', '5', null);
INSERT INTO `userinfo` VALUES ('108', '克莱汤普森', null, '0', null, 'N170427090', null, '2', '2018-05-30 20:15:49', '3', null);
INSERT INTO `userinfo` VALUES ('109', '杜兰特', null, '0', null, 'N170327020', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('110', '格林', null, '0', null, 'N1703270120', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('111', '米切尔', null, '0', null, 'N170327001', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('112', '尼克杨', null, '0', null, 'N170327099', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('113', '欧文', null, '0', null, 'N170327019', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('114', '韦德', null, '0', null, 'N1703270110', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('115', '沃顿', null, '0', null, 'N170327002', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('116', '英格拉姆', null, '0', null, 'N170327098', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('117', '科比', null, '0', null, 'N170327094', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('118', '詹姆斯', null, '0', null, 'N170327096', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('119', '奥拉迪波', null, '0', null, 'N170327097', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('120', '库里', null, '0', null, 'N1703270100', null, '2', '2018-05-30 20:15:49', '2', null);
INSERT INTO `userinfo` VALUES ('121', '布莱德索', null, '0', null, 'N170527094', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('122', '帕克', null, '0', null, 'N170527096', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('123', '邓肯', null, '0', null, 'N170527097', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('124', '奥拉朱旺', null, '0', null, 'N1705270100', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('125', '姚明', null, '0', null, 'N170527095', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('126', '巴特勒', null, '0', null, 'N170527098', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('127', '唐斯', null, '0', null, 'N170527099', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('128', '维金斯', null, '0', null, 'N1705270101', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('129', '雷迪克', null, '0', null, 'N170527093', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('130', '恩比德', null, '0', null, 'N170527092', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('131', '本西蒙斯', null, '0', null, 'N170527091', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('132', '乔西蒙斯', null, '0', null, 'N170527090', null, '2', '2018-05-30 20:15:49', '4', null);
INSERT INTO `userinfo` VALUES ('133', 'Teacher', 'c515a715-8a97-4986-bdf7-47ba05b9c709', '0', null, null, null, '1', '2018-05-31 15:06:34', null, '2');

-- ----------------------------
-- Table structure for `userinfocourse`
-- ----------------------------
DROP TABLE IF EXISTS `userinfocourse`;
CREATE TABLE `userinfocourse` (
  `userinfo_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`userinfo_id`,`course_id`),
  KEY `course_id` (`course_id`),
  CONSTRAINT `userinfocourse_ibfk_1` FOREIGN KEY (`userinfo_id`) REFERENCES `userinfo` (`id`),
  CONSTRAINT `userinfocourse_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfocourse
-- ----------------------------
