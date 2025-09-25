-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: keshe_db
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_coach`
--

DROP TABLE IF EXISTS `accounts_coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_coach` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `coach_level` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hourly_rate` decimal(8,2) NOT NULL,
  `achievements` longtext COLLATE utf8mb4_unicode_ci,
  `max_students` int unsigned NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `approved_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `accounts_coach_approved_by_id_0783a043_fk_accounts_user_id` (`approved_by_id`),
  CONSTRAINT `accounts_coach_approved_by_id_0783a043_fk_accounts_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `accounts_coach_user_id_afb09bc1_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `accounts_coach_chk_1` CHECK ((`max_students` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_coach`
--

LOCK TABLES `accounts_coach` WRITE;
/*!40000 ALTER TABLE `accounts_coach` DISABLE KEYS */;
INSERT INTO `accounts_coach` VALUES (19,'junior',80.00,'成功创建用户并保存头像文件',20,'approved','2025-09-12 10:26:14.264647','2025-09-12 10:25:16.433404','2025-09-12 10:26:14.266642',NULL,113),(39,'senior',200.00,'乒乓球基础训练',20,'approved',NULL,'2025-09-12 14:03:34.361783','2025-09-12 14:03:34.361783',NULL,161),(40,'intermediate',150.00,'乒乓球基础训练',20,'approved',NULL,'2025-09-12 14:03:34.951020','2025-09-12 14:03:34.951020',NULL,162),(41,'junior',80.00,'乒乓球基础训练',20,'approved',NULL,'2025-09-12 14:03:35.523440','2025-09-12 14:03:35.523440',NULL,163),(44,'senior',200.00,'全国乒乓球锦标赛冠军，有10年教学经验，专长正手攻球和反手推挡技术',20,'approved',NULL,'2025-09-13 02:21:31.112381','2025-09-13 02:21:31.112381',NULL,176),(45,'intermediate',150.00,'省级乒乓球比赛亚军，专长技术指导和战术分析',20,'approved',NULL,'2025-09-13 02:21:31.775623','2025-09-13 02:21:31.775623',NULL,177),(46,'junior',80.00,'市级乒乓球比赛冠军，擅长基础教学和青少年培训',20,'approved',NULL,'2025-09-13 02:21:32.372350','2025-09-13 02:21:32.372350',NULL,178),(49,'senior',200.00,'全国乒乓球锦标赛冠军，有15年教学经验，专长技术指导和战术分析',25,'approved',NULL,'2025-09-13 02:23:47.283005','2025-09-13 02:23:47.283005',NULL,183),(51,'senior',200.00,'全国乒乓球锦标赛冠军，有10年教学经验',20,'approved',NULL,'2025-09-13 02:26:28.891755','2025-09-13 02:26:28.891755',NULL,191),(52,'intermediate',150.00,'省级乒乓球比赛亚军，专长技术指导和战术分析',20,'approved',NULL,'2025-09-13 02:26:51.904751','2025-09-13 02:26:51.904751',NULL,196),(53,'senior',200.00,'专业网球教练，经验丰富',20,'approved',NULL,'2025-09-13 02:33:35.596405','2025-09-13 02:33:35.596405',NULL,198),(66,'senior',200.00,'资深乒乓球教练，具有10年教学经验',30,'approved',NULL,'2025-09-13 14:16:41.031840','2025-09-13 14:16:41.031840',NULL,224),(71,'senior',200.00,NULL,20,'approved',NULL,'2025-09-15 11:51:10.639864','2025-09-15 11:51:10.639864',NULL,320),(72,'intermediate',150.00,NULL,20,'approved',NULL,'2025-09-15 11:51:11.003632','2025-09-15 11:51:11.003632',NULL,321),(73,'senior',200.00,NULL,20,'approved',NULL,'2025-09-15 11:51:12.616882','2025-09-15 11:51:12.616882',NULL,324),(74,'intermediate',150.00,NULL,20,'approved',NULL,'2025-09-15 11:51:12.902322','2025-09-15 11:51:12.902322',NULL,325),(75,'senior',200.00,NULL,20,'approved',NULL,'2025-09-15 11:51:13.491817','2025-09-15 11:51:13.492844',NULL,328),(76,'intermediate',150.00,NULL,20,'approved',NULL,'2025-09-15 11:51:13.715583','2025-09-15 11:51:13.715583',NULL,329),(77,'senior',200.00,NULL,20,'approved',NULL,'2025-09-15 11:51:14.366037','2025-09-15 11:51:14.366037',NULL,332),(78,'intermediate',150.00,NULL,20,'approved',NULL,'2025-09-15 11:51:14.624128','2025-09-15 11:51:14.624128',NULL,333),(79,'senior',200.00,NULL,20,'approved',NULL,'2025-09-15 11:51:15.400777','2025-09-15 11:51:15.400777',NULL,336),(80,'intermediate',150.00,NULL,20,'approved',NULL,'2025-09-15 11:51:15.533178','2025-09-15 11:51:15.533178',NULL,337),(81,'senior',200.00,NULL,20,'approved',NULL,'2025-09-15 11:51:16.285437','2025-09-15 11:51:16.285437',NULL,340),(82,'intermediate',150.00,NULL,20,'approved',NULL,'2025-09-15 11:51:16.451521','2025-09-15 11:51:16.451521',NULL,341);
/*!40000 ALTER TABLE `accounts_coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(11) COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `real_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_card` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `gender` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci,
  `emergency_contact` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `emergency_phone` varchar(11) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active_member` tinyint(1) NOT NULL,
  `registration_date` datetime(6) NOT NULL,
  `last_login_ip` char(39) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=348 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (4,'pbkdf2_sha256$600000$d4a8YdLMXtEge5C0yw800Z$n81/mH7BvxgXJoKe9bon7rvvasuYBv+OcWVthAykXUA=','2025-09-16 03:15:01.794618',0,'hhm','','','',0,1,'2025-09-12 06:45:17.900763','student','18043848756','','huang',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 06:45:17.900763',NULL),(96,'pbkdf2_sha256$600000$CZcKwEJLFEiPLFeOKhsdh1$Sw1YFPMjy0kP+1kEmiOYg4ysvIduRSrz+924+/ANBqU=',NULL,0,'student1757668378102','','','',0,1,'2025-09-12 09:13:09.771246','student','13768378102','','王学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 09:13:09.771246',NULL),(100,'pbkdf2_sha256$600000$R5rKo16wrpSCwacbyeO0at$bNxTSlF4OMDFEIUT2CnDULcOX01cvuF1XUVKGoSh5Eo=',NULL,0,'student1757668941129','','','',0,1,'2025-09-12 09:22:29.027064','student','13768941129','','王学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 09:22:29.027064',NULL),(102,'!dxZciaJlB2x3UfBs6Spbme4LoESrZ6q1mEGHt5xf','2025-09-12 14:33:09.389247',0,'coach08','','','',0,1,'2025-09-12 10:10:29.629552','coach','18043848754','','huang',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 10:10:29.629552',NULL),(113,'pbkdf2_sha256$600000$lLDvD2qVHt5Nc8iGwbs7S2$teOHVgO3L0oWe1Dh8w7rMPLVlsfiR4O6flNsTdL84zE=','2025-09-12 12:53:52.530905',0,'coach10','','','1246993130@qq.com',0,1,'2025-09-12 10:25:15.939663','coach','18043848750','avatars/avatar.jpg','haunghm1',NULL,NULL,'male','','','',1,'2025-09-12 10:25:15.939663',NULL),(114,'pbkdf2_sha256$600000$yqLzkkVeCHaebowWR8BB5q$bAWmv9mQbBL8KugDQ3+ypdAQHIyfVxROmpaludg4lGI=','2025-09-12 10:37:53.905884',0,'ahuang11','','','',0,1,'2025-09-12 10:37:44.380462','student','18043848766','avatars/avatar_114_d87aff16.png','haunghm3',NULL,NULL,'female','123','123','',1,'2025-09-12 10:37:44.380462',NULL),(119,'pbkdf2_sha256$600000$1TPhI3WL4hPZfk2lSrxikD$FPm+tAqGGez3+ehAJr2gQFU77MP4E4Nb5LftelLIBPY=','2025-09-16 01:37:26.249910',1,'admin','','','admin@example.com',1,1,'2025-09-12 12:58:18.415790','super_admin','13800000000','','系统管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 12:58:18.415790',NULL),(120,'pbkdf2_sha256$600000$EggDgNsycElxaNySbrLbe6$s3EvQLCdo/Ry2FyoceZVxH5gR+qgxR7fUmRZFDovPJ8=','2025-09-12 13:21:10.644831',0,'ahuang21','','','',0,1,'2025-09-12 13:01:40.983477','student','13617739000','','haunghmoo',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 13:01:40.983477',NULL),(160,'',NULL,0,'backend_test_student','后端','测试学员','backend_student@test.com',0,1,'2025-09-12 14:03:33.354823','student','13800138001','','后端测试学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-12 14:03:33.354823',NULL),(161,'pbkdf2_sha256$600000$JIHse17WIQruqSL3E7aVhW$dRWhxxkjGa5JsUoZxomDGzueaYD77HdeBwXZQmqWKP8=','2025-09-13 03:27:15.774766',0,'coach1','张','教练','coach1@test.com',0,1,'2025-09-12 14:03:33.841442','coach','13800138002','','张教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-12 14:03:33.841442',NULL),(162,'pbkdf2_sha256$600000$I7lsbtMqyioUWOaV86ho7q$a0d0WYvhv8uBbVqcpRh/fWyfrMDoIB9xEalPZh6ir3g=','2025-09-13 06:54:10.202842',0,'coach2','李','教练','coach2@test.com',0,1,'2025-09-12 14:03:34.404534','coach','13800138003','','李教练',NULL,NULL,'female',NULL,NULL,NULL,1,'2025-09-12 14:03:34.404534',NULL),(163,'pbkdf2_sha256$600000$INKQ9cfaT82mHpnK85Z3P0$fJsFSm+AtYRDvdy/eIQ2qOHp+/8mkegpa1qIvQN92Aw=','2025-09-13 06:54:39.041561',0,'coach3','王','教练','coach3@test.com',0,1,'2025-09-12 14:03:35.012957','coach','13800138004','','王教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-12 14:03:35.012957',NULL),(167,'pbkdf2_sha256$600000$sZlpAGSZnIxB7x71fG52nK$9l66dDkTQz+MdzkstGwDeC8IvYHHwPy4xoc+VyBAYvg=','2025-09-13 13:46:04.783829',0,'student2','','','student2@test.com',0,1,'2025-09-12 14:35:43.177999','student','13800000003','','李四',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 14:35:43.177999',NULL),(168,'pbkdf2_sha256$600000$57lUSQPFdbnOCysUNcUfmx$nS1esGmpAJtPff1ljxUNkH0cCVRZluvG4VMttnOI9hM=','2025-09-13 03:16:26.577204',0,'student3','','','student3@test.com',0,1,'2025-09-12 14:35:43.597886','student','13800000004','','王五',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 14:35:43.597886',NULL),(169,'pbkdf2_sha256$600000$GibkakmS0LpBpWnNfwJPOy$XxTFmc/i6h+jWRAcRRgYjzjntoqgoqFMwadmu+OBeSw=','2025-09-13 06:53:37.286434',0,'student4','','','student4@test.com',0,1,'2025-09-12 14:35:44.018213','student','13800000005','','赵六',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-12 14:35:44.018213',NULL),(175,'pbkdf2_sha256$600000$H83IqiLYelgyN2jjbjsSay$64oREqAxsqB8k34vw0gVLZc7U3q0UEZ/ssut6ci3/O8=',NULL,0,'e2e_test_student_1757730089','端到端测试','学员','e2e_student_1757730089@test.com',0,1,'2025-09-13 02:21:29.756655','student','13800130089','','端到端测试学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:21:29.756655',NULL),(176,'pbkdf2_sha256$600000$QdIPODgqjHKrhyOB0D95hz$uAbrblBtskRBZQ5elWEflLGewEGx+jgRVHITZa0O+Ms=',NULL,0,'e2e_test_coach1_1757730089','','','e2e_test_coach1_1757730089@test.com',0,1,'2025-09-13 02:21:30.315065','coach','13800140089','','张教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:21:30.315065',NULL),(177,'pbkdf2_sha256$600000$qBTxzjft3rIipHRwRlTfpa$fIkKZS0kuwhpWGKPY/sk8OOmBZLlJIzfG+OxyvX3mVU=',NULL,0,'e2e_test_coach2_1757730089','','','e2e_test_coach2_1757730089@test.com',0,1,'2025-09-13 02:21:31.190181','coach','13800150089','','李教练',NULL,NULL,'female',NULL,NULL,NULL,1,'2025-09-13 02:21:31.190181',NULL),(178,'pbkdf2_sha256$600000$s0PnX4rECVa6brEXbBV5VU$5wmz3d+wYa0acU910UbeLzziiPs8x6YsnOmW61+JlgY=',NULL,0,'e2e_test_coach3_1757730089','','','e2e_test_coach3_1757730089@test.com',0,1,'2025-09-13 02:21:31.830756','coach','13800160089','','王教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:21:31.830756',NULL),(183,'pbkdf2_sha256$600000$Y5fCK9Ef5p0jfaQr8Vl1wl$CIBo/qZG6FUVBO0+vGgALfFEw+27QYipIZeIK4eiS38=',NULL,0,'e2e_coach_test_main_1757730226','端到端测试','教练','e2e_coach_1757730226@test.com',0,1,'2025-09-13 02:23:46.338865','coach','13800130226','','端到端测试教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:23:46.338865',NULL),(184,'pbkdf2_sha256$600000$rAdiFcunhSmV2DEP2Qn8lo$oAgLRhPK8Wo1jVNcg/7r9knKl8nOVtzu+R91Xs6KsOg=',NULL,0,'e2e_student_test_1_1757730226','','','e2e_student_test_1_1757730226@test.com',0,1,'2025-09-13 02:23:47.400214','student','1380014001','','张学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:23:47.400214',NULL),(185,'pbkdf2_sha256$600000$WngYdWI2Glq2p2YoejmASJ$o0mh5fS72T0WJv6TYL7gJK9ZYuce5mtiBmB0g3fZLI0=',NULL,0,'e2e_student_test_2_1757730226','','','e2e_student_test_2_1757730226@test.com',0,1,'2025-09-13 02:23:48.126691','student','1380014002','','李学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:23:48.126691',NULL),(186,'pbkdf2_sha256$600000$8hj2pogmMY51NSCHNeam1m$B2p71/Qlu/ytz9+1JBq/MeG54Rp73Re7TzpLUtuYUwc=',NULL,0,'e2e_student_test_3_1757730226','','','e2e_student_test_3_1757730226@test.com',0,1,'2025-09-13 02:23:48.718453','student','1380014003','','王学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:23:48.718453',NULL),(191,'pbkdf2_sha256$600000$hajEmXsX8lgQAPTnOJKGLe$vCbKOVnWxY2wPJs3mOXU4ehXk7CXh/D3D67KhwDrtow=',NULL,0,'coach_frontend_test_1757730387','前端测试','教练','coach_frontend_1757730387@test.com',0,1,'2025-09-13 02:26:28.357970','coach','13857730387','','前端测试教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:26:28.357970',NULL),(192,'pbkdf2_sha256$600000$sYQHEa04X3SJuIiCZh58Ti$uUFc5gvoJ8LiIH2pnprlv6YlME5u2ODawBB/mHAaUlo=',NULL,0,'student_frontend_test1_1757730387','','','student_frontend_test1_1757730387@test.com',0,1,'2025-09-13 02:26:28.965908','student','13977303870','','张学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:26:28.965908',NULL),(193,'pbkdf2_sha256$600000$Je12CQXLy7FIoMDgsaRpnw$LFEvkuraxG2JR3O4TEeI1Is6djJxc67G5Ja+10wFz/E=',NULL,0,'student_frontend_test2_1757730387','','','student_frontend_test2_1757730387@test.com',0,1,'2025-09-13 02:26:29.501564','student','13977303871','','李学员',NULL,NULL,'female',NULL,NULL,NULL,1,'2025-09-13 02:26:29.501564',NULL),(194,'pbkdf2_sha256$600000$ioTAbC9UaHB0omrIrfUgnG$0pTvCBL1w9nUGKBjc+oGkKO7GUNCxSyv1paw1Hlowe8=',NULL,0,'student_frontend_test3_1757730387','','','student_frontend_test3_1757730387@test.com',0,1,'2025-09-13 02:26:30.061460','student','13977303872','','王学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:26:30.061460',NULL),(195,'pbkdf2_sha256$600000$MEL3Poied55t27Teq3RGKc$aiBc0em/CdKaL0mA/yRBVqzzNkePv8KP7Gs8AGytwmo=',NULL,0,'frontend_test_student_1757730410','','','frontend_student_1757730410@test.com',0,1,'2025-09-13 02:26:50.300100','student','13800130410','','前端测试学员',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:26:50.300100',NULL),(196,'pbkdf2_sha256$600000$MNXycsw9C4AbS3ZHKapjr4$alUV4UpRe2anXu7a68gKBKUXvdnY24m0JyGNE3f4VXE=',NULL,0,'frontend_test_coach_1757730410','','','frontend_coach_1757730410@test.com',0,1,'2025-09-13 02:26:50.982363','coach','13800140410','','前端测试教练',NULL,NULL,'female',NULL,NULL,NULL,1,'2025-09-13 02:26:50.982363',NULL),(197,'pbkdf2_sha256$600000$3naPdGH4JMnCEtoETvAhT8$hzCETa5uEqVM8WKe4zy6Ax2QwFE8Imulnsrw1MgDzOc=',NULL,0,'debug_coach_1757730759','调试','教练','debug_1757730759@test.com',0,1,'2025-09-13 02:32:39.595330','coach','13857730759','','调试教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:32:39.595330',NULL),(198,'pbkdf2_sha256$600000$El68GArrRiczXlh9eWc0ml$WY97jR2GT/cnv6kfkUkiSi04Lq3RlJCbFLlUEeUVITc=',NULL,0,'debug_coach_1757730815','调试','教练','debug_1757730815@test.com',0,1,'2025-09-13 02:33:35.088596','coach','13857730815','','调试教练',NULL,NULL,'male',NULL,NULL,NULL,1,'2025-09-13 02:33:35.088596',NULL),(224,'pbkdf2_sha256$600000$5MeDvhSE5XBTmENkGLLb9r$toQqpy36It8GVhPhv/xKJqW7h/VhqR7LoPps9GN3wrc=','2025-09-13 14:23:41.077237',0,'王教练','王','教练','wangcoach@example.com',0,1,'2025-09-13 14:16:40.048979','coach','13800138000','','王教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-13 14:16:40.048979',NULL),(226,'pbkdf2_sha256$600000$vsku4MRLV1i3MYJ9K30KET$1ZITyX0XmRiLu/nH7bxsT/6oAIfrd3MwF8preXxQO2M=',NULL,0,'wang_student1','王学生1','','wangstudent1@example.com',0,1,'2025-09-13 14:17:19.535296','student','1380013811','','王学生1',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-13 14:17:19.535296',NULL),(227,'pbkdf2_sha256$600000$3DNAGsUiFG1biVRCScsMEx$1pp46jvWx2ELUg+Rc45Ys5U8ktixnA/HuXyfxKvZDA4=',NULL,0,'wang_student2','王学生2','','wangstudent2@example.com',0,1,'2025-09-13 14:17:20.129996','student','1380013812','','王学生2',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-13 14:17:20.129996',NULL),(228,'pbkdf2_sha256$600000$WoNgRYeNa6DJRPLguGFnZ9$7ue3O9lCdweJRhCjTF31W5x9bhdw2fgj+jVHKzqxbTI=',NULL,0,'wang_student3','王学生3','','wangstudent3@example.com',0,1,'2025-09-13 14:17:20.603139','student','1380013813','','王学生3',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-13 14:17:20.603139',NULL),(251,'pbkdf2_sha256$600000$phAVtTBavXTlJgKOBDWBbg$C8U54iBiT6VmEG664VaEcdOk6Y2SNBOIGkQI5/M9Sv4=',NULL,0,'pending_recharge_user','','','pending@recharge.com',0,1,'2025-09-14 08:38:06.934598','student','1380006750','','待审核充值用户',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-14 08:38:06.934598',NULL),(266,'pbkdf2_sha256$600000$0HOeI30udv51jnHlOU8GID$kjeodt2/oEuXnxvzRQqKUUAv51EYyHTh9HMifyfyHeU=',NULL,0,'coach33835','','','coach33835@test.com',0,1,'2025-09-15 08:09:20.297397','coach','13800033835','','测试教练33835',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:09:20.297397',NULL),(267,'pbkdf2_sha256$600000$2bUXdGy1LPmvPGHup685Rz$vm3LRr3vr72hbMhEv/cms7srBcL+w1S7351afJlO/8s=',NULL,0,'student33835','','','student33835@test.com',0,1,'2025-09-15 08:09:20.733371','student','13900033835','','测试学员33835',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:09:20.733371',NULL),(268,'pbkdf2_sha256$600000$tBdYT3HfTwVfVxCoZyGCII$lcc8jmTeNGCL6a+LzRIyqkE2etjnE2+UjF00Bjz4n9w=',NULL,0,'coach72412','','','coach72412@test.com',0,1,'2025-09-15 08:11:55.966725','coach','13800072412','','测试教练72412',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:11:55.966725',NULL),(269,'pbkdf2_sha256$600000$ZX6Thf9qiLK5IfOP3wlk50$gywyuojZSglWPbwrtVzpAT1qkj71bZ1Wo4s2GYlBYsg=','2025-09-15 08:11:57.543503',0,'student72412','','','student72412@test.com',0,1,'2025-09-15 08:11:56.408652','student','13900072412','','测试学员72412',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:11:56.408652',NULL),(270,'pbkdf2_sha256$600000$R0TGakVDAoPDUeuOxmcJXl$kxrePpmkxVEsRUpJS+l6Sopt7dDjlPoyg7VBDlndlZ0=',NULL,0,'coach22826','','','coach22826@test.com',0,1,'2025-09-15 08:12:37.825595','coach','13800022826','','测试教练22826',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:12:37.825595',NULL),(271,'pbkdf2_sha256$600000$3Qyl2o0K7x24Q7Of11jLl7$n40nOYpUmuuWEPlcjCoCPkaSJ5iWADWzTTghE5jPXos=','2025-09-15 08:12:39.550268',0,'student22826','','','student22826@test.com',0,1,'2025-09-15 08:12:38.252774','student','13900022826','','测试学员22826',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:12:38.252774',NULL),(272,'pbkdf2_sha256$600000$yUeZMAW8ZNgr5dQKKJYwdV$wSWf42h7J6KVHHk9ZNpPYcpD23GXsvtK3CcCKC4rdhw=',NULL,0,'coach65840','','','coach65840@test.com',0,1,'2025-09-15 08:13:16.817633','coach','13800065840','','测试教练65840',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:13:16.817633',NULL),(273,'pbkdf2_sha256$600000$M3PPctfjz0nWhmZRRv7Scn$r0drGtGJ1ZCUWArhZhiaL6uHCSTKzHye511dH9cd0qE=',NULL,0,'student65840','','','student65840@test.com',0,1,'2025-09-15 08:13:17.237767','student','13900065840','','测试学员65840',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:13:17.237767',NULL),(274,'pbkdf2_sha256$600000$mykld0FD3xOEfapsQLldCc$NT3204XZclQ2KQ26P6DrGsqGLhZASKKBmeIfgymwSCA=',NULL,0,'coach48632','','','coach48632@test.com',0,1,'2025-09-15 08:14:33.610316','coach','13800048632','','测试教练48632',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:14:33.610316',NULL),(275,'pbkdf2_sha256$600000$Mn3BkqwQb3JmXe5KATDm85$daaGOwlqPvedOaTqUB32vKiBjV4n/U7nPqR3mhhoYP0=','2025-09-15 08:14:36.379962',0,'student48632','','','student48632@test.com',0,1,'2025-09-15 08:14:34.095643','student','13900048632','','测试学员48632',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:14:34.095643',NULL),(276,'pbkdf2_sha256$600000$jIhOc6yCHSgiYnSuZIr9sh$5aJL/D5Bfbi0QFLN7zjvdoKS5KvONavrPwZclDfrGOs=',NULL,0,'coach58403','','','coach58403@test.com',0,1,'2025-09-15 08:15:11.619110','coach','13800058403','','测试教练58403',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:15:11.619110',NULL),(277,'pbkdf2_sha256$600000$pND8IFXo9BQDOCu7Dg4YQk$nKfnTB9bxDiIKMc6xbtaMZFyW9XQbGe/pNfi0A/hTtk=','2025-09-15 08:15:13.265282',0,'student58403','','','student58403@test.com',0,1,'2025-09-15 08:15:12.075799','student','13900058403','','测试学员58403',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 08:15:12.075799',NULL),(319,'',NULL,0,'test_student_coach_change_937070','','','student_937070@test.com',0,1,'2025-09-15 11:51:10.317432','student','1380937070','','测试学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:10.317432',NULL),(320,'',NULL,0,'test_current_coach_937070','','','current_coach_937070@test.com',0,1,'2025-09-15 11:51:10.510866','coach','1381937070','','当前教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:10.510866',NULL),(321,'',NULL,0,'test_new_coach_937070','','','new_coach_937070@test.com',0,1,'2025-09-15 11:51:10.891731','coach','1382937070','','新教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:10.891731',NULL),(322,'',NULL,0,'test_admin_coach_change_937070','','','admin_937070@test.com',0,1,'2025-09-15 11:51:11.542303','campus_admin','1383937070','','测试管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:11.542303',NULL),(323,'',NULL,0,'test_student_coach_change_937072','','','student_937072@test.com',0,1,'2025-09-15 11:51:12.021043','student','1380937072','','测试学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:12.021043',NULL),(324,'',NULL,0,'test_current_coach_937072','','','current_coach_937072@test.com',0,1,'2025-09-15 11:51:12.504064','coach','1381937072','','当前教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:12.504064',NULL),(325,'',NULL,0,'test_new_coach_937072','','','new_coach_937072@test.com',0,1,'2025-09-15 11:51:12.836605','coach','1382937072','','新教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:12.836605',NULL),(326,'',NULL,0,'test_admin_coach_change_937072','','','admin_937072@test.com',0,1,'2025-09-15 11:51:13.038792','campus_admin','1383937072','','测试管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:13.038792',NULL),(327,'',NULL,0,'test_student_coach_change_937073','','','student_937073@test.com',0,1,'2025-09-15 11:51:13.306926','student','1380937073','','测试学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:13.306926',NULL),(328,'',NULL,0,'test_current_coach_937073','','','current_coach_937073@test.com',0,1,'2025-09-15 11:51:13.445015','coach','1381937073','','当前教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:13.445015',NULL),(329,'',NULL,0,'test_new_coach_937073','','','new_coach_937073@test.com',0,1,'2025-09-15 11:51:13.624279','coach','1382937073','','新教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:13.625277',NULL),(330,'',NULL,0,'test_admin_coach_change_937073','','','admin_937073@test.com',0,1,'2025-09-15 11:51:13.864270','campus_admin','1383937073','','测试管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:13.864270',NULL),(331,'',NULL,0,'test_student_coach_change_937074','','','student_937074@test.com',0,1,'2025-09-15 11:51:14.152981','student','1380937074','','测试学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:14.152981',NULL),(332,'',NULL,0,'test_current_coach_937074','','','current_coach_937074@test.com',0,1,'2025-09-15 11:51:14.310284','coach','1381937074','','当前教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:14.310284',NULL),(333,'',NULL,0,'test_new_coach_937074','','','new_coach_937074@test.com',0,1,'2025-09-15 11:51:14.537052','coach','1382937074','','新教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:14.537052',NULL),(334,'',NULL,0,'test_admin_coach_change_937074','','','admin_937074@test.com',0,1,'2025-09-15 11:51:14.752299','campus_admin','1383937074','','测试管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:14.752299',NULL),(335,'',NULL,0,'test_student_coach_change_937075','','','student_937075@test.com',0,1,'2025-09-15 11:51:15.236666','student','1380937075','','测试学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:15.236666',NULL),(336,'',NULL,0,'test_current_coach_937075','','','current_coach_937075@test.com',0,1,'2025-09-15 11:51:15.345215','coach','1381937075','','当前教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:15.345215',NULL),(337,'',NULL,0,'test_new_coach_937075','','','new_coach_937075@test.com',0,1,'2025-09-15 11:51:15.489714','coach','1382937075','','新教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:15.489714',NULL),(338,'',NULL,0,'test_admin_coach_change_937075','','','admin_937075@test.com',0,1,'2025-09-15 11:51:15.644220','campus_admin','1383937075','','测试管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:15.644220',NULL),(339,'',NULL,0,'test_student_coach_change_937076','','','student_937076@test.com',0,1,'2025-09-15 11:51:16.090388','student','1380937076','','测试学员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:16.090388',NULL),(340,'',NULL,0,'test_current_coach_937076','','','current_coach_937076@test.com',0,1,'2025-09-15 11:51:16.219054','coach','1381937076','','当前教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:16.219054',NULL),(341,'',NULL,0,'test_new_coach_937076','','','new_coach_937076@test.com',0,1,'2025-09-15 11:51:16.397702','coach','1382937076','','新教练',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:16.397702',NULL),(342,'',NULL,0,'test_admin_coach_change_937076','','','admin_937076@test.com',0,1,'2025-09-15 11:51:16.581207','campus_admin','1383937076','','测试管理员',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:51:16.581207',NULL),(343,'pbkdf2_sha256$600000$uj1oFUMOqdbNYIWsG6vVQh$5greaHy+E5ejir1meLk/T1M8CvQxNc8H9EDZ6Qji5yg=','2025-09-15 13:36:16.147314',0,'test_student','','','test_student@example.com',0,1,'2025-09-15 11:55:09.715440','student','','','',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 11:55:09.715440',NULL),(346,'pbkdf2_sha256$600000$TEYqq3mfxlEeiq2FRpF4zn$RucUYiTckTH8MWZuf/Sces2tVl5S8vYCEGOWLV+u5O8=',NULL,0,'test_coach1','测试','教练1','test_coach1@example.com',0,1,'2025-09-15 16:05:01.215915','coach','13800000002','','',NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-09-15 16:05:01.215915',NULL);
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
INSERT INTO `accounts_user_groups` VALUES (37,160,1),(38,161,2),(39,162,2),(40,163,2),(43,175,1),(44,176,2),(45,177,2),(46,178,2),(51,183,2),(52,184,1),(53,185,1),(54,186,1),(59,191,2),(60,192,1),(61,193,1),(62,194,1),(63,195,1),(64,196,2),(65,197,2),(66,198,2);
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_profile`
--

DROP TABLE IF EXISTS `accounts_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bio` longtext COLLATE utf8mb4_unicode_ci,
  `skills` longtext COLLATE utf8mb4_unicode_ci,
  `experience_years` int unsigned NOT NULL,
  `certification` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_user_profile_user_id_0080de5e_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `accounts_user_profile_chk_1` CHECK ((`experience_years` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_profile`
--

LOCK TABLES `accounts_user_profile` WRITE;
/*!40000 ALTER TABLE `accounts_user_profile` DISABLE KEYS */;
INSERT INTO `accounts_user_profile` VALUES (4,'','',0,'','2025-09-12 06:45:18.363620','2025-09-12 10:45:20.440865',4),(58,NULL,NULL,0,NULL,'2025-09-12 09:13:10.286826','2025-09-12 09:13:10.286826',96),(61,NULL,NULL,0,NULL,'2025-09-12 09:22:29.496772','2025-09-12 09:22:29.496772',100),(72,'','',0,NULL,'2025-09-12 10:25:16.398544','2025-09-12 10:36:59.550977',113),(73,'1232131231','123',0,NULL,'2025-09-12 10:37:44.858841','2025-09-12 10:46:52.951514',114),(76,NULL,NULL,0,NULL,'2025-09-12 13:01:41.500167','2025-09-12 13:01:41.500167',120),(79,NULL,NULL,0,NULL,'2025-09-13 03:02:49.356768','2025-09-13 03:02:49.356783',161),(80,NULL,NULL,0,NULL,'2025-09-13 03:05:01.485646','2025-09-13 03:05:01.485646',162),(81,NULL,NULL,0,NULL,'2025-09-13 03:05:44.586415','2025-09-13 03:05:44.586415',167),(82,NULL,NULL,0,NULL,'2025-09-13 03:16:27.101822','2025-09-13 03:16:27.101822',168),(83,NULL,NULL,0,NULL,'2025-09-13 03:26:51.302412','2025-09-13 03:26:51.302412',169),(85,NULL,NULL,0,NULL,'2025-09-13 06:54:39.647391','2025-09-13 06:54:39.647391',163),(86,NULL,NULL,0,NULL,'2025-09-13 14:23:41.554881','2025-09-13 14:23:41.554881',224),(87,NULL,NULL,0,NULL,'2025-09-14 08:30:55.320975','2025-09-14 08:30:55.320975',119);
/*!40000 ALTER TABLE `accounts_user_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'学员'),(2,'教练员');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add Token',6,'add_token'),(22,'Can change Token',6,'change_token'),(23,'Can delete Token',6,'delete_token'),(24,'Can view Token',6,'view_token'),(25,'Can add Token',7,'add_tokenproxy'),(26,'Can change Token',7,'change_tokenproxy'),(27,'Can delete Token',7,'delete_tokenproxy'),(28,'Can view Token',7,'view_tokenproxy'),(29,'Can add 用户',8,'add_user'),(30,'Can change 用户',8,'change_user'),(31,'Can delete 用户',8,'delete_user'),(32,'Can view 用户',8,'view_user'),(33,'Can add 用户资料',9,'add_userprofile'),(34,'Can change 用户资料',9,'change_userprofile'),(35,'Can delete 用户资料',9,'delete_userprofile'),(36,'Can view 用户资料',9,'view_userprofile'),(37,'Can add 校区',10,'add_campus'),(38,'Can change 校区',10,'change_campus'),(39,'Can delete 校区',10,'delete_campus'),(40,'Can view 校区',10,'view_campus'),(41,'Can add 校区学员',11,'add_campusstudent'),(42,'Can change 校区学员',11,'change_campusstudent'),(43,'Can delete 校区学员',11,'delete_campusstudent'),(44,'Can view 校区学员',11,'view_campusstudent'),(45,'Can add 校区教练',12,'add_campuscoach'),(46,'Can change 校区教练',12,'change_campuscoach'),(47,'Can delete 校区教练',12,'delete_campuscoach'),(48,'Can view 校区教练',12,'view_campuscoach'),(49,'Can add 校区分区',13,'add_campusarea'),(50,'Can change 校区分区',13,'change_campusarea'),(51,'Can delete 校区分区',13,'delete_campusarea'),(52,'Can view 校区分区',13,'view_campusarea'),(53,'Can add 课程',14,'add_course'),(54,'Can change 课程',14,'change_course'),(55,'Can delete 课程',14,'delete_course'),(56,'Can view 课程',14,'view_course'),(57,'Can add 课程课时',15,'add_coursesession'),(58,'Can change 课程课时',15,'change_coursesession'),(59,'Can delete 课程课时',15,'delete_coursesession'),(60,'Can view 课程课时',15,'view_coursesession'),(61,'Can add 课程时间表',16,'add_courseschedule'),(62,'Can change 课程时间表',16,'change_courseschedule'),(63,'Can delete 课程时间表',16,'delete_courseschedule'),(64,'Can view 课程时间表',16,'view_courseschedule'),(65,'Can add 课程评价',17,'add_courseevaluation'),(66,'Can change 课程评价',17,'change_courseevaluation'),(67,'Can delete 课程评价',17,'delete_courseevaluation'),(68,'Can view 课程评价',17,'view_courseevaluation'),(69,'Can add 课程报名',18,'add_courseenrollment'),(70,'Can change 课程报名',18,'change_courseenrollment'),(71,'Can delete 课程报名',18,'delete_courseenrollment'),(72,'Can view 课程报名',18,'view_courseenrollment'),(73,'Can add 课程考勤',19,'add_courseattendance'),(74,'Can change 课程考勤',19,'change_courseattendance'),(75,'Can delete 课程考勤',19,'delete_courseattendance'),(76,'Can view 课程考勤',19,'view_courseattendance'),(77,'Can add 支付记录',20,'add_payment'),(78,'Can change 支付记录',20,'change_payment'),(79,'Can delete 支付记录',20,'delete_payment'),(80,'Can view 支付记录',20,'view_payment'),(81,'Can add 支付方式',21,'add_paymentmethod'),(82,'Can change 支付方式',21,'change_paymentmethod'),(83,'Can delete 支付方式',21,'delete_paymentmethod'),(84,'Can view 支付方式',21,'view_paymentmethod'),(85,'Can add 用户账户',22,'add_useraccount'),(86,'Can change 用户账户',22,'change_useraccount'),(87,'Can delete 用户账户',22,'delete_useraccount'),(88,'Can view 用户账户',22,'view_useraccount'),(89,'Can add 退款记录',23,'add_refund'),(90,'Can change 退款记录',23,'change_refund'),(91,'Can delete 退款记录',23,'delete_refund'),(92,'Can view 退款记录',23,'view_refund'),(93,'Can add 发票',24,'add_invoice'),(94,'Can change 发票',24,'change_invoice'),(95,'Can delete 发票',24,'delete_invoice'),(96,'Can view 发票',24,'view_invoice'),(97,'Can add 账户交易记录',25,'add_accounttransaction'),(98,'Can change 账户交易记录',25,'change_accounttransaction'),(99,'Can delete 账户交易记录',25,'delete_accounttransaction'),(100,'Can view 账户交易记录',25,'view_accounttransaction'),(101,'Can add 预约',26,'add_booking'),(102,'Can change 预约',26,'change_booking'),(103,'Can delete 预约',26,'delete_booking'),(104,'Can view 预约',26,'view_booking'),(105,'Can add 球台',27,'add_table'),(106,'Can change 球台',27,'change_table'),(107,'Can delete 球台',27,'delete_table'),(108,'Can view 球台',27,'view_table'),(109,'Can add 师生关系',28,'add_coachstudentrelation'),(110,'Can change 师生关系',28,'change_coachstudentrelation'),(111,'Can delete 师生关系',28,'delete_coachstudentrelation'),(112,'Can view 师生关系',28,'view_coachstudentrelation'),(113,'Can add 预约取消申请',29,'add_bookingcancellation'),(114,'Can change 预约取消申请',29,'change_bookingcancellation'),(115,'Can delete 预约取消申请',29,'delete_bookingcancellation'),(116,'Can view 预约取消申请',29,'view_bookingcancellation'),(117,'Can add 消息通知',30,'add_notification'),(118,'Can change 消息通知',30,'change_notification'),(119,'Can delete 消息通知',30,'delete_notification'),(120,'Can view 消息通知',30,'view_notification'),(121,'Can add 比赛',31,'add_competition'),(122,'Can change 比赛',31,'change_competition'),(123,'Can delete 比赛',31,'delete_competition'),(124,'Can view 比赛',31,'view_competition'),(125,'Can add 比赛分组',32,'add_competitiongroup'),(126,'Can change 比赛分组',32,'change_competitiongroup'),(127,'Can delete 比赛分组',32,'delete_competitiongroup'),(128,'Can view 比赛分组',32,'view_competitiongroup'),(129,'Can add 比赛对战',33,'add_competitionmatch'),(130,'Can change 比赛对战',33,'change_competitionmatch'),(131,'Can delete 比赛对战',33,'delete_competitionmatch'),(132,'Can view 比赛对战',33,'view_competitionmatch'),(133,'Can add 分组成员',34,'add_competitiongroupmember'),(134,'Can change 分组成员',34,'change_competitiongroupmember'),(135,'Can delete 分组成员',34,'delete_competitiongroupmember'),(136,'Can view 分组成员',34,'view_competitiongroupmember'),(137,'Can add 比赛结果',35,'add_competitionresult'),(138,'Can change 比赛结果',35,'change_competitionresult'),(139,'Can delete 比赛结果',35,'delete_competitionresult'),(140,'Can view 比赛结果',35,'view_competitionresult'),(141,'Can add 比赛报名',36,'add_competitionregistration'),(142,'Can change 比赛报名',36,'change_competitionregistration'),(143,'Can delete 比赛报名',36,'delete_competitionregistration'),(144,'Can view 比赛报名',36,'view_competitionregistration'),(145,'Can add 教练员',37,'add_coach'),(146,'Can change 教练员',37,'change_coach'),(147,'Can delete 教练员',37,'delete_coach'),(148,'Can view 教练员',37,'view_coach'),(149,'Can add 教练更换申请',38,'add_coachchangerequest'),(150,'Can change 教练更换申请',38,'change_coachchangerequest'),(151,'Can delete 教练更换申请',38,'delete_coachchangerequest'),(152,'Can view 教练更换申请',38,'view_coachchangerequest');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('02a512b006e88d091756ee0acc69a1da69372003','2025-09-15 08:15:13.322133',277),('033584a4d5a65d3b4d89f871aa8e05e76413f848','2025-09-15 08:14:36.420461',275),('5f358aced305ce570b354a9c12fe378ac95000f2','2025-09-14 09:39:33.147551',4),('63201e715e55121d30cddccf415e87fbc716035f','2025-09-15 08:11:57.632535',269),('840bf627763027e48668d6e461b69db148a6df08','2025-09-13 13:46:04.832393',167),('a5620625c23600ccbad0af020af7ffcb9840a040','2025-09-15 08:12:39.607143',271),('b53d434d6cb75113b48bf077c1f4614c6080d3ae','2025-09-16 01:21:50.928974',119),('e3ebafc7ec6fdcc363fc5186d5df4a3c04fe6df6','2025-09-15 11:55:23.160455',343);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus_area`
--

DROP TABLE IF EXISTS `campus_area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campus_area` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `area_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `capacity` int unsigned NOT NULL,
  `equipment_list` longtext COLLATE utf8mb4_unicode_ci,
  `is_available` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `campus_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `campus_area_campus_id_name_ebdf3d6d_uniq` (`campus_id`,`name`),
  CONSTRAINT `campus_area_campus_id_03ce41bd_fk_campus_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus_campus` (`id`),
  CONSTRAINT `campus_area_chk_1` CHECK ((`capacity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus_area`
--

LOCK TABLES `campus_area` WRITE;
/*!40000 ALTER TABLE `campus_area` DISABLE KEYS */;
INSERT INTO `campus_area` VALUES (1,'训练区A','training','主要训练区域',50,NULL,1,'2025-09-12 03:42:48.959262','2025-09-12 03:42:48.959278',1),(2,'A区训练馆','','A区训练馆，适合基础训练',20,NULL,1,'2025-09-12 03:45:38.340224','2025-09-12 03:45:38.340241',2);
/*!40000 ALTER TABLE `campus_area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus_campus`
--

DROP TABLE IF EXISTS `campus_campus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campus_campus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `facilities` longtext COLLATE utf8mb4_unicode_ci,
  `operating_hours` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `capacity` int unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `manager_id` bigint DEFAULT NULL,
  `campus_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_person` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parent_campus_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `code` (`code`),
  KEY `campus_campus_manager_id_1d73bf33_fk_accounts_user_id` (`manager_id`),
  KEY `campus_campus_parent_campus_id_5dde8907_fk_campus_campus_id` (`parent_campus_id`),
  CONSTRAINT `campus_campus_manager_id_1d73bf33_fk_accounts_user_id` FOREIGN KEY (`manager_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `campus_campus_parent_campus_id_5dde8907_fk_campus_campus_id` FOREIGN KEY (`parent_campus_id`) REFERENCES `campus_campus` (`id`),
  CONSTRAINT `campus_campus_chk_1` CHECK ((`capacity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus_campus`
--

LOCK TABLES `campus_campus` WRITE;
/*!40000 ALTER TABLE `campus_campus` DISABLE KEYS */;
INSERT INTO `campus_campus` VALUES (1,'中心校区','CENTER','北京市海淀区','010-12345678',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-12 03:42:48.903836','2025-09-12 03:42:48.903869',NULL,'center','待填写',NULL),(2,'主校区','','北京市朝阳区体育大街123号','010-12345678',NULL,'主要校区，设施齐全',NULL,'09:00-21:00',100,1,'2025-09-12 03:45:38.274103','2025-09-12 03:45:38.274120',NULL,'branch','待填写',NULL),(21,'吉林大学前卫南区','651828','12312','18043848756','1246993132@qq.com','哈哈hhhh',NULL,'09:00-21:00',100,1,'2025-09-12 07:51:39.155064','2025-09-12 07:51:39.155064',NULL,'branch','待填写',NULL),(40,'测试校区_1757730410','TEST_1757730410','测试地址123号','12345678901',NULL,'用于前端交互测试的校区',NULL,'09:00-21:00',100,1,'2025-09-13 02:26:50.260640','2025-09-13 02:26:50.260640',NULL,'branch','待填写',NULL),(41,'调试校区_1757730739','DEBUG_1757730739','调试地址123号','12345678901',NULL,'用于调试的校区',NULL,'09:00-21:00',100,1,'2025-09-13 02:32:19.240985','2025-09-13 02:32:19.240985',NULL,'branch','待填写',NULL),(42,'调试校区_1757730759','DEBUG_1757730759','调试地址123号','12345678901',NULL,'用于调试的校区',NULL,'09:00-21:00',100,1,'2025-09-13 02:32:39.476718','2025-09-13 02:32:39.476718',NULL,'branch','待填写',NULL),(43,'调试校区_1757730815','DEBUG_1757730815','调试地址123号','12345678901',NULL,'用于调试的校区',NULL,'09:00-21:00',100,1,'2025-09-13 02:33:35.036950','2025-09-13 02:33:35.036950',NULL,'branch','待填写',NULL),(47,'测试校区余额','TEST8138','测试地址','12345678901',NULL,'测试校区',NULL,'09:00-21:00',100,1,'2025-09-15 07:59:28.353269','2025-09-15 07:59:28.353269',NULL,'branch','待填写',NULL),(48,'测试校区46512','TEST46512','测试地址46512','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:07:50.425641','2025-09-15 08:07:50.425641',NULL,'main','待填写',NULL),(49,'测试校区73941','TEST73941','测试地址73941','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:08:23.966338','2025-09-15 08:08:23.966338',NULL,'main','待填写',NULL),(50,'测试校区33835','TEST33835','测试地址33835','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:09:20.262884','2025-09-15 08:09:20.262884',NULL,'main','待填写',NULL),(51,'测试校区72412','TEST72412','测试地址72412','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:11:55.903865','2025-09-15 08:11:55.903865',NULL,'main','待填写',NULL),(52,'测试校区22826','TEST22826','测试地址22826','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:12:37.723181','2025-09-15 08:12:37.723181',NULL,'main','待填写',NULL),(53,'测试校区65840','TEST65840','测试地址65840','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:13:16.788591','2025-09-15 08:13:16.788591',NULL,'main','待填写',NULL),(54,'测试校区48632','TEST48632','测试地址48632','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:14:33.541990','2025-09-15 08:14:33.541990',NULL,'main','待填写',NULL),(55,'测试校区58403','TEST58403','测试地址58403','',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 08:15:11.544383','2025-09-15 08:15:11.544383',NULL,'main','待填写',NULL),(56,'测试校区','TEST001','测试地址','1234567890',NULL,NULL,NULL,'09:00-21:00',100,1,'2025-09-15 11:51:10.256858','2025-09-15 11:51:10.256858',NULL,'branch','测试联系人',NULL);
/*!40000 ALTER TABLE `campus_campus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus_coach`
--

DROP TABLE IF EXISTS `campus_coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campus_coach` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `hire_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `specialties` longtext COLLATE utf8mb4_unicode_ci,
  `max_students` int unsigned NOT NULL,
  `hourly_rate` decimal(8,2) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `campus_id` bigint NOT NULL,
  `coach_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `campus_coach_campus_id_coach_id_1253ddfc_uniq` (`campus_id`,`coach_id`),
  KEY `campus_coach_coach_id_333dfa66_fk_accounts_user_id` (`coach_id`),
  CONSTRAINT `campus_coach_campus_id_8b3228bd_fk_campus_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus_campus` (`id`),
  CONSTRAINT `campus_coach_coach_id_333dfa66_fk_accounts_user_id` FOREIGN KEY (`coach_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `campus_coach_chk_1` CHECK ((`max_students` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus_coach`
--

LOCK TABLES `campus_coach` WRITE;
/*!40000 ALTER TABLE `campus_coach` DISABLE KEYS */;
INSERT INTO `campus_coach` VALUES (10,'2025-09-13 02:26:51.872265',1,NULL,20,0.00,NULL,'2025-09-13 02:26:51.877262',40,196),(11,'2025-09-13 02:32:40.214876',1,NULL,20,0.00,NULL,'2025-09-13 02:32:40.214876',42,197),(12,'2025-09-13 02:33:35.561443',1,NULL,20,0.00,NULL,'2025-09-13 02:33:35.561443',43,198),(20,'2025-09-15 11:51:10.751287',1,NULL,20,0.00,NULL,'2025-09-15 11:51:10.751287',56,320),(21,'2025-09-15 11:51:11.423394',1,NULL,20,0.00,NULL,'2025-09-15 11:51:11.423394',56,321),(22,'2025-09-15 11:51:12.745304',1,NULL,20,0.00,NULL,'2025-09-15 11:51:12.745304',56,324),(23,'2025-09-15 11:51:12.966924',1,NULL,20,0.00,NULL,'2025-09-15 11:51:12.966924',56,325),(24,'2025-09-15 11:51:13.566207',1,NULL,20,0.00,NULL,'2025-09-15 11:51:13.567202',56,328),(25,'2025-09-15 11:51:13.789266',1,NULL,20,0.00,NULL,'2025-09-15 11:51:13.789266',56,329),(26,'2025-09-15 11:51:14.442472',1,NULL,20,0.00,NULL,'2025-09-15 11:51:14.443469',56,332),(27,'2025-09-15 11:51:14.683693',1,NULL,20,0.00,NULL,'2025-09-15 11:51:14.683693',56,333),(28,'2025-09-15 11:51:15.445450',1,NULL,20,0.00,NULL,'2025-09-15 11:51:15.445450',56,336),(29,'2025-09-15 11:51:15.578086',1,NULL,20,0.00,NULL,'2025-09-15 11:51:15.578086',56,337),(30,'2025-09-15 11:51:16.330355',1,NULL,20,0.00,NULL,'2025-09-15 11:51:16.331350',56,340),(31,'2025-09-15 11:51:16.520281',1,NULL,20,0.00,NULL,'2025-09-15 11:51:16.520281',56,341);
/*!40000 ALTER TABLE `campus_coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `campus_student`
--

DROP TABLE IF EXISTS `campus_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campus_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `enrollment_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `campus_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `campus_student_campus_id_student_id_10e60d4f_uniq` (`campus_id`,`student_id`),
  KEY `campus_student_student_id_dfdd3cb0_fk_accounts_user_id` (`student_id`),
  CONSTRAINT `campus_student_campus_id_dd11d3af_fk_campus_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus_campus` (`id`),
  CONSTRAINT `campus_student_student_id_dfdd3cb0_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus_student`
--

LOCK TABLES `campus_student` WRITE;
/*!40000 ALTER TABLE `campus_student` DISABLE KEYS */;
INSERT INTO `campus_student` VALUES (14,'2025-09-13 02:26:51.760527',1,NULL,'2025-09-13 02:26:51.760527',40,195),(18,'2025-09-15 11:51:10.389013',1,NULL,'2025-09-15 11:51:10.389530',56,319),(19,'2025-09-15 11:51:12.306101',1,NULL,'2025-09-15 11:51:12.306101',56,323),(20,'2025-09-15 11:51:13.370251',1,NULL,'2025-09-15 11:51:13.371279',56,327),(21,'2025-09-15 11:51:14.241244',1,NULL,'2025-09-15 11:51:14.242241',56,331),(22,'2025-09-15 11:51:15.301502',1,NULL,'2025-09-15 11:51:15.302499',56,335),(23,'2025-09-15 11:51:16.171574',1,NULL,'2025-09-15 11:51:16.171574',56,339);
/*!40000 ALTER TABLE `campus_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions_competition`
--

DROP TABLE IF EXISTS `competitions_competition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions_competition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `competition_date` datetime(6) NOT NULL,
  `registration_start` datetime(6) NOT NULL,
  `registration_end` datetime(6) NOT NULL,
  `registration_fee` decimal(10,2) NOT NULL,
  `max_participants_per_group` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `campus_id` bigint NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `competitions_competition_campus_id_4c718f4a_fk_campus_campus_id` (`campus_id`),
  KEY `competitions_competi_created_by_id_1b438bb8_fk_accounts_` (`created_by_id`),
  CONSTRAINT `competitions_competi_created_by_id_1b438bb8_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `competitions_competition_campus_id_4c718f4a_fk_campus_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus_campus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions_competition`
--

LOCK TABLES `competitions_competition` WRITE;
/*!40000 ALTER TABLE `competitions_competition` DISABLE KEYS */;
/*!40000 ALTER TABLE `competitions_competition` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions_competitiongroup`
--

DROP TABLE IF EXISTS `competitions_competitiongroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions_competitiongroup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `group_type` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `competition_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `competitions_competition_competition_id_group_nam_5988e135_uniq` (`competition_id`,`group_name`),
  CONSTRAINT `competitions_competi_competition_id_463fee69_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions_competitiongroup`
--

LOCK TABLES `competitions_competitiongroup` WRITE;
/*!40000 ALTER TABLE `competitions_competitiongroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `competitions_competitiongroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions_competitiongroupmember`
--

DROP TABLE IF EXISTS `competitions_competitiongroupmember`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions_competitiongroupmember` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `seed_number` int DEFAULT NULL,
  `group_id` bigint NOT NULL,
  `participant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `competitions_competition_group_id_participant_id_bdb0e943_uniq` (`group_id`,`participant_id`),
  KEY `competitions_competi_participant_id_a522150e_fk_accounts_` (`participant_id`),
  CONSTRAINT `competitions_competi_group_id_993bcd35_fk_competiti` FOREIGN KEY (`group_id`) REFERENCES `competitions_competitiongroup` (`id`),
  CONSTRAINT `competitions_competi_participant_id_a522150e_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions_competitiongroupmember`
--

LOCK TABLES `competitions_competitiongroupmember` WRITE;
/*!40000 ALTER TABLE `competitions_competitiongroupmember` DISABLE KEYS */;
/*!40000 ALTER TABLE `competitions_competitiongroupmember` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions_competitionmatch`
--

DROP TABLE IF EXISTS `competitions_competitionmatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions_competitionmatch` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `match_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `round_number` int NOT NULL,
  `table_number` int DEFAULT NULL,
  `scheduled_time` datetime(6) DEFAULT NULL,
  `actual_start_time` datetime(6) DEFAULT NULL,
  `actual_end_time` datetime(6) DEFAULT NULL,
  `player1_score` int NOT NULL,
  `player2_score` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `competition_id` bigint NOT NULL,
  `group_id` bigint DEFAULT NULL,
  `player1_id` bigint NOT NULL,
  `player2_id` bigint NOT NULL,
  `winner_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competitions_competi_competition_id_77997734_fk_competiti` (`competition_id`),
  KEY `competitions_competi_group_id_4a548b7e_fk_competiti` (`group_id`),
  KEY `competitions_competi_player1_id_965bdd19_fk_accounts_` (`player1_id`),
  KEY `competitions_competi_player2_id_8da082f8_fk_accounts_` (`player2_id`),
  KEY `competitions_competi_winner_id_f82c8359_fk_accounts_` (`winner_id`),
  CONSTRAINT `competitions_competi_competition_id_77997734_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  CONSTRAINT `competitions_competi_group_id_4a548b7e_fk_competiti` FOREIGN KEY (`group_id`) REFERENCES `competitions_competitiongroup` (`id`),
  CONSTRAINT `competitions_competi_player1_id_965bdd19_fk_accounts_` FOREIGN KEY (`player1_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `competitions_competi_player2_id_8da082f8_fk_accounts_` FOREIGN KEY (`player2_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `competitions_competi_winner_id_f82c8359_fk_accounts_` FOREIGN KEY (`winner_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions_competitionmatch`
--

LOCK TABLES `competitions_competitionmatch` WRITE;
/*!40000 ALTER TABLE `competitions_competitionmatch` DISABLE KEYS */;
/*!40000 ALTER TABLE `competitions_competitionmatch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions_competitionregistration`
--

DROP TABLE IF EXISTS `competitions_competitionregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions_competitionregistration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `registration_time` datetime(6) NOT NULL,
  `payment_status` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `competition_id` bigint NOT NULL,
  `participant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `competitions_competition_competition_id_participa_5eb6ad70_uniq` (`competition_id`,`participant_id`),
  KEY `competitions_competi_participant_id_aaa2e1ba_fk_accounts_` (`participant_id`),
  CONSTRAINT `competitions_competi_competition_id_221529de_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  CONSTRAINT `competitions_competi_participant_id_aaa2e1ba_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions_competitionregistration`
--

LOCK TABLES `competitions_competitionregistration` WRITE;
/*!40000 ALTER TABLE `competitions_competitionregistration` DISABLE KEYS */;
/*!40000 ALTER TABLE `competitions_competitionregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `competitions_competitionresult`
--

DROP TABLE IF EXISTS `competitions_competitionresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `competitions_competitionresult` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `matches_played` int NOT NULL,
  `matches_won` int NOT NULL,
  `matches_lost` int NOT NULL,
  `total_score_for` int NOT NULL,
  `total_score_against` int NOT NULL,
  `group_rank` int DEFAULT NULL,
  `overall_rank` int DEFAULT NULL,
  `award` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `competition_id` bigint NOT NULL,
  `participant_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `competitions_competition_competition_id_participa_fbfe5a7e_uniq` (`competition_id`,`participant_id`),
  KEY `competitions_competi_participant_id_e50bd131_fk_accounts_` (`participant_id`),
  CONSTRAINT `competitions_competi_competition_id_6a4ceb02_fk_competiti` FOREIGN KEY (`competition_id`) REFERENCES `competitions_competition` (`id`),
  CONSTRAINT `competitions_competi_participant_id_e50bd131_fk_accounts_` FOREIGN KEY (`participant_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `competitions_competitionresult`
--

LOCK TABLES `competitions_competitionresult` WRITE;
/*!40000 ALTER TABLE `competitions_competitionresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `competitions_competitionresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_attendance`
--

DROP TABLE IF EXISTS `courses_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `check_in_time` datetime(6) DEFAULT NULL,
  `check_out_time` datetime(6) DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `session_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `courses_attendance_session_id_student_id_fb772a56_uniq` (`session_id`,`student_id`),
  KEY `courses_attendance_student_id_dd341799_fk_accounts_user_id` (`student_id`),
  CONSTRAINT `courses_attendance_session_id_32bf1c3e_fk_courses_session_id` FOREIGN KEY (`session_id`) REFERENCES `courses_session` (`id`),
  CONSTRAINT `courses_attendance_student_id_dd341799_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_attendance`
--

LOCK TABLES `courses_attendance` WRITE;
/*!40000 ALTER TABLE `courses_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_course`
--

DROP TABLE IF EXISTS `courses_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_course` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `course_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `max_students` int unsigned NOT NULL,
  `duration_minutes` int unsigned NOT NULL,
  `price_per_session` decimal(8,2) NOT NULL,
  `total_sessions` int unsigned NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `requirements` longtext COLLATE utf8mb4_unicode_ci,
  `equipment_needed` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `area_id` bigint DEFAULT NULL,
  `campus_id` bigint NOT NULL,
  `coach_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `courses_course_area_id_806ef5ae_fk_campus_area_id` (`area_id`),
  KEY `courses_course_campus_id_0c24eed7_fk_campus_campus_id` (`campus_id`),
  KEY `courses_course_coach_id_1b705ade_fk_accounts_user_id` (`coach_id`),
  CONSTRAINT `courses_course_area_id_806ef5ae_fk_campus_area_id` FOREIGN KEY (`area_id`) REFERENCES `campus_area` (`id`),
  CONSTRAINT `courses_course_campus_id_0c24eed7_fk_campus_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus_campus` (`id`),
  CONSTRAINT `courses_course_coach_id_1b705ade_fk_accounts_user_id` FOREIGN KEY (`coach_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `courses_course_chk_1` CHECK ((`max_students` >= 0)),
  CONSTRAINT `courses_course_chk_2` CHECK ((`duration_minutes` >= 0)),
  CONSTRAINT `courses_course_chk_3` CHECK ((`total_sessions` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_course`
--

LOCK TABLES `courses_course` WRITE;
/*!40000 ALTER TABLE `courses_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_enrollment`
--

DROP TABLE IF EXISTS `courses_enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_enrollment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `enrollment_date` datetime(6) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `paid_amount` decimal(8,2) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `courses_enrollment_course_id_student_id_46471c5a_uniq` (`course_id`,`student_id`),
  KEY `courses_enrollment_student_id_aebf8536_fk_accounts_user_id` (`student_id`),
  CONSTRAINT `courses_enrollment_course_id_2631503e_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `courses_enrollment_student_id_aebf8536_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_enrollment`
--

LOCK TABLES `courses_enrollment` WRITE;
/*!40000 ALTER TABLE `courses_enrollment` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_evaluation`
--

DROP TABLE IF EXISTS `courses_evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_evaluation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci,
  `coach_rating` int NOT NULL,
  `facility_rating` int NOT NULL,
  `is_anonymous` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `course_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `courses_evaluation_course_id_student_id_8b8dc96e_uniq` (`course_id`,`student_id`),
  KEY `courses_evaluation_student_id_bdbd16d1_fk_accounts_user_id` (`student_id`),
  CONSTRAINT `courses_evaluation_course_id_2b884470_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `courses_evaluation_student_id_bdbd16d1_fk_accounts_user_id` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_evaluation`
--

LOCK TABLES `courses_evaluation` WRITE;
/*!40000 ALTER TABLE `courses_evaluation` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_evaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_schedule`
--

DROP TABLE IF EXISTS `courses_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_schedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `weekday` int NOT NULL,
  `start_time` time(6) NOT NULL,
  `end_time` time(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `courses_schedule_course_id_weekday_start_time_c13091fe_uniq` (`course_id`,`weekday`,`start_time`),
  CONSTRAINT `courses_schedule_course_id_ed83a201_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_schedule`
--

LOCK TABLES `courses_schedule` WRITE;
/*!40000 ALTER TABLE `courses_schedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses_session`
--

DROP TABLE IF EXISTS `courses_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses_session` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_number` int unsigned NOT NULL,
  `scheduled_date` date NOT NULL,
  `scheduled_time` time(6) NOT NULL,
  `actual_start_time` datetime(6) DEFAULT NULL,
  `actual_end_time` datetime(6) DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` longtext COLLATE utf8mb4_unicode_ci,
  `homework` longtext COLLATE utf8mb4_unicode_ci,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `course_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `courses_session_course_id_session_number_cb966614_uniq` (`course_id`,`session_number`),
  CONSTRAINT `courses_session_course_id_d6a68b24_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`),
  CONSTRAINT `courses_session_chk_1` CHECK ((`session_number` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses_session`
--

LOCK TABLES `courses_session` WRITE;
/*!40000 ALTER TABLE `courses_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `courses_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (5,'2025-09-14 08:44:59.184383','20','PAY20250914CCAADCF8 - 待审核充值用户 - ¥200.00',2,'[{\"changed\": {\"fields\": [\"\\u652f\\u4ed8\\u7c7b\\u578b\"]}}]',20,119),(6,'2025-09-15 07:28:55.121866','13','吉林大学前卫南区 - 100号台',1,'[{\"added\": {}}]',27,119);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (37,'accounts','coach'),(8,'accounts','user'),(9,'accounts','userprofile'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(6,'authtoken','token'),(7,'authtoken','tokenproxy'),(10,'campus','campus'),(13,'campus','campusarea'),(12,'campus','campuscoach'),(11,'campus','campusstudent'),(31,'competitions','competition'),(32,'competitions','competitiongroup'),(34,'competitions','competitiongroupmember'),(33,'competitions','competitionmatch'),(36,'competitions','competitionregistration'),(35,'competitions','competitionresult'),(4,'contenttypes','contenttype'),(14,'courses','course'),(19,'courses','courseattendance'),(18,'courses','courseenrollment'),(17,'courses','courseevaluation'),(16,'courses','courseschedule'),(15,'courses','coursesession'),(30,'notifications','notification'),(25,'payments','accounttransaction'),(24,'payments','invoice'),(20,'payments','payment'),(21,'payments','paymentmethod'),(23,'payments','refund'),(22,'payments','useraccount'),(26,'reservations','booking'),(29,'reservations','bookingcancellation'),(38,'reservations','coachchangerequest'),(28,'reservations','coachstudentrelation'),(27,'reservations','table'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-09-12 03:21:17.864843'),(2,'contenttypes','0002_remove_content_type_name','2025-09-12 03:21:19.205689'),(3,'auth','0001_initial','2025-09-12 03:21:22.583029'),(4,'auth','0002_alter_permission_name_max_length','2025-09-12 03:21:23.356887'),(5,'auth','0003_alter_user_email_max_length','2025-09-12 03:21:23.402633'),(6,'auth','0004_alter_user_username_opts','2025-09-12 03:21:23.509767'),(7,'auth','0005_alter_user_last_login_null','2025-09-12 03:21:23.618127'),(8,'auth','0006_require_contenttypes_0002','2025-09-12 03:21:23.725292'),(9,'auth','0007_alter_validators_add_error_messages','2025-09-12 03:21:23.781816'),(10,'auth','0008_alter_user_username_max_length','2025-09-12 03:21:23.851837'),(11,'auth','0009_alter_user_last_name_max_length','2025-09-12 03:21:23.910869'),(12,'auth','0010_alter_group_name_max_length','2025-09-12 03:21:23.997564'),(13,'auth','0011_update_proxy_permissions','2025-09-12 03:21:24.069863'),(14,'auth','0012_alter_user_first_name_max_length','2025-09-12 03:21:24.132076'),(15,'accounts','0001_initial','2025-09-12 03:21:30.314300'),(16,'admin','0001_initial','2025-09-12 03:21:32.244016'),(17,'admin','0002_logentry_remove_auto_add','2025-09-12 03:21:32.281000'),(18,'admin','0003_logentry_add_action_flag_choices','2025-09-12 03:21:32.346988'),(19,'authtoken','0001_initial','2025-09-12 03:21:33.560590'),(20,'authtoken','0002_auto_20160226_1747','2025-09-12 03:21:33.662839'),(21,'authtoken','0003_tokenproxy','2025-09-12 03:21:33.790866'),(22,'authtoken','0004_alter_tokenproxy_options','2025-09-12 03:21:33.830912'),(23,'campus','0001_initial','2025-09-12 03:21:40.472945'),(24,'campus','0002_campus_campus_type_campus_contact_person_and_more','2025-09-12 03:21:43.727044'),(25,'campus','0003_auto_20250911_1813','2025-09-12 03:21:43.777391'),(26,'courses','0001_initial','2025-09-12 03:22:00.046444'),(27,'notifications','0001_initial','2025-09-12 03:22:05.834312'),(28,'payments','0001_initial','2025-09-12 03:22:20.360382'),(29,'reservations','0001_initial','2025-09-12 03:22:32.296615'),(30,'sessions','0001_initial','2025-09-12 03:22:32.920261'),(31,'competitions','0001_initial','2025-09-12 06:52:29.843477'),(32,'competitions','0002_alter_competitionregistration_participant','2025-09-12 06:57:30.861891'),(33,'accounts','0002_coach','2025-09-12 08:01:26.442112'),(34,'accounts','0003_increase_avatar_field_length','2025-09-12 10:12:06.685426'),(35,'reservations','0002_booking_payment_status_alter_booking_status','2025-09-15 07:51:47.151587'),(36,'reservations','0003_remove_booking_payment_status_alter_booking_status','2025-09-15 08:42:44.355586'),(37,'reservations','0004_booking_payment_status','2025-09-15 08:42:44.872881'),(38,'reservations','0005_alter_bookingcancellation_status_coachchangerequest','2025-09-15 11:46:26.812965'),(39,'reservations','0002_coachchangerequest_and_more','2025-09-15 15:48:59.849281');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('000ap064nfwctsk3qrzluu68bwuf3typ','.eJxVjDsOwjAQBe_iGln-JHZMSZ8zWJvdNQ4gW4qTCnF3EikFtG9m3ltE2NYct8ZLnElchXZBXH7XCfDJ5UD0gHKvEmtZl3mShyJP2uRYiV-30_07yNDyXlswxNpaFaztBiKTjFGph0AOAyuG5H0yOBh2iMn3asfWoabEAB1p8fkCM_Q4vg:1uxGuY:Zg12HEYhK8WmwJdT5DAEtlM22IjlQ1nzZQ0wue3b-Fo','2025-09-27 03:26:50.827522'),('06gyqm5c4onzutsy96wottw0c2pc40bc','.eJxVjEEOgjAQRe_StWloy8y0Lt17BjJ0BosaSCisjHdXEha6_e-9_zIdb2vptqpLN4o5G0zm9Dv2nB867UTuPN1mm-dpXcbe7oo9aLXXWfR5Ody_g8K1fOuUoXGEAdAjp-QkkjZAWb00AQSVQCLCgBpyG5kpc8sDeQfBJU9q3h_poDdl:1uwysY:7B-sYDYfbF3VpKXRNwiqE8CZvT_1Rg9gDMsPDaZYl1o','2025-09-26 08:11:34.463516'),('0yvjvlshve17edvp04hunk2t65tgsony','.eJxVjMsOwiAQRf-FtSGFMkxx6d5vIDM8pGogKe3K-O_apAvd3nPOfQlP21r81tPi5yjOQisQp9-VKTxS3VG8U701GVpdl5nlrsiDdnltMT0vh_t3UKiXb-1gSNlNGgkdKkusCYagMbC1Wscxm0x2sujcqIAzWB45QUDDgYxCJd4fGqA35Q:1uxGyq:5rgoYPmCcgcT2WzBLF9xujWNlHyGIQp-rJyYnmIORO8','2025-09-27 03:31:16.860909'),('113r8zahxennfool1rvcag8xs4o07cdg','.eJxVjMsOwiAQRf-FtSEDpS3j0r3fQIZhkKqBpI-V8d-1SRe6veec-1KBtrWEbZE5TEmdlTWoTr9rJH5I3VG6U701za2u8xT1ruiDLvrakjwvh_t3UGgp39qzWOQBe8LEzorP2Y1gAMYUAYxk00dA7wQjWu6J0WcTU4fW09A5UO8PMvA4FQ:1uxGzd:gmqZtDmOSPZ0mv0V_jrQF84W3NyCo351sw36U0eIMI8','2025-09-27 03:32:05.573674'),('11ewajvsg61fzk7d15o4v31iktrawtcr','.eJxVjEEOwiAQRe_C2hAYwIJL9z0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kbgIY404_a4J84PbjuiO7TbLPLd1mZLcFXnQLseZ-Hk93L-Dir1-a0XJcQI9EHhdsrMGvSlaQWBAk8-oSwgZVLGgkIlDGhQkFTwxuhKseH8ANBc4iw:1uy7nz:6vgzXxTxi8ESPcQN0gHVofeXmM1qKPvaaI2w-HPINZ0','2025-09-29 11:55:35.503957'),('14i7j8zziedkwvzt2q9qxq8t67927b8a','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyKOF:pQJo2O9MEqrk3j-yvKPqQThpawgJpcysmy5FOM1pW-k','2025-09-30 01:21:51.321962'),('15zaw8iw9of6qhvbh53j3728txsbttjb','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uxhuW:jKh4H-a4UT2STI7PKdw3qOAu4LCuFIGbmnRKwE9pwrY','2025-09-28 08:16:36.593748'),('21720z5zej5vbf30sqt3yzql6atdymqu','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxd5H:qFBvoUHNBORKbiOnZBPUD0L-GuTUOXYuz523CmbKHrA','2025-09-28 03:07:23.048803'),('29iscsjyyf42v8ugjflduuvmv163qqbv','.eJxVjEEOwiAQRe_C2hCgAoNL9z0DGWZQqgaS0q6Md7dNutDte-__t4i4LiWuPc9xYnERxmhx-qUJ6ZnrrviB9d4ktbrMU5J7Ig_b5dg4v65H-3dQsJdtjTdDXjsXNFnmrDSCUZoB0xlygrAx53TwTNmSU4NXfkBIHAgMqWDF5ws5ijhu:1uxH0d:1kxh-SyT9HTL-XfH4yQp_Tn2_dc8quDbqEInU9z5YnM','2025-09-27 03:33:07.455001'),('2fmiblqh9g6vw7llp9ju1eir0l00wb0f','.eJxVjMsOwiAQRf-FtSEwJTxcuvcbCMMMUjWQlHZl_Hdt0oVu7znnvkRM21rjNniJM4mzAG3F6XfFlB_cdkT31G5d5t7WZUa5K_KgQ1478fNyuH8HNY36rUtwViUNBTIGX7xlcug1GItIyrFKhifKhjkbomAMkJ6Ch4kwKNIg3h8_9Tia:1uxGyn:PQRtswMI62MnaEP_zGLdU2boGLlO6XqS9dah_rpwxtA','2025-09-27 03:31:13.832960'),('2mfjn2kljwon3gnlznr2ixuq3rrmiju3','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxGZR:U55RNSFr5WQ-9JPPhz0ElZveXnikljSdIC1Is5ayf9U','2025-09-27 03:05:01.096409'),('2rsqo5wjtguwqgbfkctq6ty5eucjisrp','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxdK7:bY65eAIeSNxpqeV12-UpCfKQA9We6vS67gj0stR1O78','2025-09-28 03:22:43.660389'),('386803lx0lgvsrny9p6rfbzmu1dfy7f7','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxGSq:VHSwL8aFmkstmOtr0cpIffDrFhtXPeA3i-_Lbkufi7o','2025-09-27 02:58:12.760287'),('3et5cymuuwwrofsbni02or0l62lc8400','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyKb3:K8O7sASdzJ5J0QXKZQnTSec6R9R9z23S_gppvKfJhkE','2025-09-30 01:35:05.631944'),('3hvb1vi023o5f5lm7nfer8e74rl6gok2','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxd2b:5viuCigjpUwLU_ewgYIAYVLs7u0EugaM1wQvhSvRAAA','2025-09-28 03:04:37.452021'),('3rzxz4yh9eehd2an748jzvz5llxnnz4f','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB9k:ZzR-S36daTZAysApeERX-LFzfuqA6mi_FMA7U863Jjo','2025-09-29 15:30:16.209963'),('43lb1njpp1xjkm5vtep3ea150j5f6uos','.eJxVjEsOwjAMBe-SNYrkOB_Kkj1niBzboQXUSk27qrg7VOoCtm9m3mYyrUuf16ZzHsRcDMDZnH7XQvzUcUfyoPE-WZ7GZR6K3RV70GZvk-jrerh_Bz21_lsXjxo7X7rqktcA6COBY1B2JAlLql6rwyqMwaUkHLFowFhJRBg68_4ANQk4-w:1ux1Yk:k6QfKPzlTfG7ILNyI2Q9uWp448INSW7C7J-Ku5qZjOQ','2025-09-26 11:03:18.346386'),('4a03opvhocwa22ubazfidx0fqeixj7l0','.eJxVjEEOgjAURO_StWkKUtq6dM8ZyPz_W0FNm1BYGe-uJCx0O--9eakR2zqNW43LOIu6KNeq0-9I4EfMO5E78q1oLnldZtK7og9a9VAkPq-H-3cwoU7fGh7nhoK4ADhJltvO9J1rxCZwsraXyD5wI63xnhFhrCeCp5AIIRn1_gAswjlc:1uwyuG:bX8jEt5qaZcqvMGmpn4NnX7zAyOY6UXB4NYC2x4VZuU','2025-09-26 08:13:20.306667'),('4amz9whwx23vblj7xs22zqnvbwk2ed9u','.eJxVjMsOwiAUBf-FtSEUysul-34DuQ-UqoGktCvjv2uTLnR7Zua8RIJtLWnreUkzi7PQWovT74pAj1x3xHeotyap1XWZUe6KPGiXU-P8vBzu30GBXr51GB0Yy8QePVBUROQgqMwKowXCASzbwWlzNV4T-DgawzC6HJxnZBbvD0x2OR8:1uxH0Z:eZ_m1kbjnXrUcRb6Ige_YLKwfa7uM60azfgVeJZ3Vj0','2025-09-27 03:33:03.250839'),('4dv0xr4f1k885prmls9bz03yboee3itf','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLD7:HgRnBEkJR1j7g9vrQPJIKPVblxWU35_lU8mLFpxGl-M','2025-09-27 08:02:17.267467'),('4fupva603fg26lyl5kzw777n1sd7rm66','.eJxVjMsOwiAQAP-FsyEgTz167zc0yy4rVQNJaU_GfzckPeh1ZjJvMcO-lXnveZ0XElcRnDj9wgT4zHUYekC9N4mtbuuS5EjkYbucGuXX7Wj_BgV6GV9L4BhUIsRwNmiUZmcpa2avDCSvDdhLJqDoKQKZwIxM3geMFsmJzxc6ZDmK:1uwz0m:fI_wwFOOTVWIIWI_ry5EmVrdh4H_q4RNYG7BKFO4rEY','2025-09-26 08:20:04.674117'),('4gwjbruxv1rfipjd29o5qdhh4u4kv2ca','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxFJI:SAxFhB7d8nZRfLh_7HR7oM_WGa3Kwo7KFxgEVapnKKw','2025-09-27 01:44:16.182458'),('4ozh18b5ssfw0xua5af7yfm32c1v6s5r','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLAo:GP0ol0mqtz0HdGlLzDOAwxKCtgbsoZNkpRdcTItbPTw','2025-09-27 07:59:54.008490'),('4sfk9dcrc1wh9r2z69647ieuv6h8u673','.eJxVjEEOwiAQRe_C2pACU6Au3XsGMp0ZpGpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzsl1Qp991RHpI3RHfsd5mTXNdl2nUu6IP2vR1ZnleDvfvoGAr3xp8yIOQWDNiZ4ApCg8cKTvTZzTBAQJiiJCDWAIUwAxko--9M8xOvT9Owzj5:1uxGNg:g7afoi1KmPL-C_rcy6Cy1c40mOij_FqizCw-7Z2274s','2025-09-27 02:52:52.779674'),('4utx7fatc1mnvjy9vz9fwm255ek90e73','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyBvg:yHB4TdaqJ3Q5rZuD2SxtbWMymywhuXQE_ibe38gfBuE','2025-09-29 16:19:48.598208'),('4yx5kp769acykotka26zl40l7zrk6s1l','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxdGb:oDclqC4AZWLlxv0qxgL41qYzmC3ekM0IFlC5UaqNCiA','2025-09-28 03:19:05.539741'),('57gk22j1e3xf88e04me9edb7aj888grw','.eJxVjEEOwiAQRe_C2pACU6Au3XsGMp0ZpGpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzsl1Qp991RHpI3RHfsd5mTXNdl2nUu6IP2vR1ZnleDvfvoGAr3xp8yIOQWDNiZ4ApCg8cKTvTZzTBAQJiiJCDWAIUwAxko--9M8xOvT9Owzj5:1uxGOr:rmhvmgpN_Y1R-dsrYKhgQUrZx-gBtej0vjO2BZWh1aQ','2025-09-27 02:54:05.090523'),('58ndtxaz0mova69qbndwu9y8sh69o6cx','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLTa:eMfvZb_bb9QC5NrDHDd_HUZG5QAXDo02Km3g5az8eaY','2025-09-27 08:19:18.573298'),('5cfkwfj8m0dmlxa8w2ctywzerpcr6b95','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLGj:ngANngK9-6z3G2dI3bmaOYfwMnn8_KfcDT-H95DeG3c','2025-09-27 08:06:01.583965'),('5p1y8v21zqub7hkcojqarfpbld5k1os5','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLVt:NwzX3MdW3vsi3C2kG_JdHuYEgNJ_oXdi1r8Jvit0OUw','2025-09-27 08:21:41.475090'),('5powkf2jbvtem7e0nuorc08qmmyzbiag','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxK9C:xeggh9ajnr_yDflD9onVTqqKcg5X4oeDyw5dLugJvGM','2025-09-27 06:54:10.310710'),('64sed4j71d1h25wuffww23kso7isg1nd','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLWG:0yVlcn5WEGCz1Am8z311StZGlNveOgFHJUquAckzX0g','2025-09-27 08:22:04.097017'),('6b8g8otqicb5xjzswmg1cmnt1aa0zb39','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB9k:ZzR-S36daTZAysApeERX-LFzfuqA6mi_FMA7U863Jjo','2025-09-29 15:30:16.144997'),('6br3jysoxy2hbxicism11x3odlz0vfp7','.eJxVjDsOwjAQRO_iGlmxvf5R0nOGaONd4wBypDipEHcHSymgGmnem3mJEfetjHvjdZxJnIVSUZx-2wnTg2tHdMd6W2Ra6rbOk-yKPGiT14X4eTncv4OCrXzXEIFIDwoDIOtokgP0kTkYw2nyGgw7a6wbFFjUPXIgTcAh5Ow8iPcHGC83iA:1uxhkL:Q4hpm2y4_zYwdz5V-tT8X1PS9NC0j6ZAFBEAXfuKAHI','2025-09-28 08:06:05.024605'),('6ju0vje8s5p7lzxdb10087zna9j720oi','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxKCA:V7C-5WC2RF31pO2q-SwnBHbJl_6cX_bVPG9Hv9PmvO0','2025-09-27 06:57:14.060049'),('6m50rse65p0hc45dkx6slyq2d4sdmkl5','.eJxVjDsOwjAQRO_iGlmO_6akzxms3bWDA8iW4qRC3J1ESgHdaN6bebMI21ri1vMS58SubGCX3w6BnrkeID2g3hunVtdlRn4o_KSdjy3l1-10_w4K9LKvrQl6EJNWDgxm76wNKIMnF4gEoUEtlXEOyCAoO2VD0ma9p-AFKhTs8wXLCDeB:1uwuhk:osXxhRRVPCaqvMM1WAsjbogq8O_ShPy7oYQHXJRAIsE','2025-09-26 03:44:08.785212'),('6uw6kpl2iixlz93grs0ucwcibn3fmbxn','.eJxVjMsOwiAQRf-FtSHDq4BL934DGWCQqoGktCvjv2uTLnR7zzn3xQJuaw3boCXMmZ2ZEJqdfteI6UFtR_mO7dZ56m1d5sh3hR908GvP9Lwc7t9BxVG_NRRKJglUegIAka1TTnuM1nsgkCpqCZSdNWiKVtkWJW2hqKMRaQKy7P0BFYs3zA:1ux1A9:WLRPINrgVWCB-ORxbI6CCwl02Z20Kcc6w7riAcd8DDM','2025-09-26 10:37:53.997323'),('6zjseyj0wlwbiljke8bybery30k6epj4','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxKEI:zUx6Rc8UBFEw9F_gi61Z1Eh1eJzfqQO_Jf2DPKIQ8Bg','2025-09-27 06:59:26.230573'),('6zpxd68uv50j5j6zd26rzau15zuswpkw','.eJxVjDsOwjAQRO_iGlkmu_5R0nMGa73e4ABKpDipEHcnkVJAM8W8N_NWidalprXJnIaiLgrV6bfLxE8Zd1AeNN4nzdO4zEPWu6IP2vRtKvK6Hu7fQaVWt3WIAs4iBPRb9OQdCknMcO4cFgbL3pvC0cVsEU0QYNtxD7YzCCykPl--_Tcm:1uyM8X:NF0bTBEa_KWLEOfyN7lwTDkeTx2PMiYuFHf5okidkeo','2025-09-30 03:13:45.616885'),('7f663abjiosactyqrhfy9g71vvjlbhpf','.eJxVjMsOwiAQRf-FtSEDpS3j0r3fQIZhkKqBpI-V8d-1SRe6veec-1KBtrWEbZE5TEmdlTWoTr9rJH5I3VG6U701za2u8xT1ruiDLvrakjwvh_t3UGgp39qzWOQBe8LEzorP2Y1gAMYUAYxk00dA7wQjWu6J0WcTU4fW09A5UO8PMvA4FQ:1uxGzd:gmqZtDmOSPZ0mv0V_jrQF84W3NyCo351sw36U0eIMI8','2025-09-27 03:32:05.020836'),('7fvin1egxbo4nqx9wfdptcelccu1cdi7','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxGbQ:GtYVCmjr5l7hbvFpclmbLZff-5eNdf2lZqq1QZNLiNw','2025-09-27 03:07:04.555051'),('7l72rqlmoz0skn761ftobkfe8552g143','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLEn:wG4ERylgUR3NMom6HjxjA0ZzL1WgKnMMPmWn1YGq2uA','2025-09-27 08:04:01.740117'),('7qey92cfpodj19s212q8p7kf6hlsf35d','.eJxVjEEOwiAQAP_C2RCg28J69N43kAUWqRqalPZk_Lsh6UGvM5N5C0_HXvzRePNLEldhYBKXXxooPrl2lR5U76uMa923JcieyNM2Oa-JX7ez_RsUaqWPRwAzDsjKWp0xEGDUEwREbRQHDsoNbJXR5JAoZmTilNOgwYFFq8XnCxFSN-U:1uxi0y:rdkCWvu44cHo0O7sMMelA7ssBwW3hqEo0ZKkev5yAVs','2025-09-28 08:23:16.162970'),('7qy4mn25udt4cf7fk271x89cjpgnk024','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKuT:YiORVDRBXhJpULn2sllWYafKVXsj7DQKj5YLpOgiQos','2025-09-30 01:55:09.741097'),('7xixpk6gh03rzto0es2bvx6di34eqo7y','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKkM:Emt0Dk5eCgDkOSuvzUZspnveKixgMgxnA8eAjAC_B0Y','2025-09-30 01:44:42.860466'),('7zzl94omitztj7nrrq7j17413c5q2jhn','.eJxVjDsOwyAQBe9CHaHF_EzK9D4DWmAJTiKQjF1FuXtsyUXSvpl5b-ZxW4vfOi1-TuzKhBnZ5XcNGJ9UD5QeWO-Nx1bXZQ78UPhJO59aotftdP8OCvay1zAkbRwIkC7npJyyRC4bbSkIIg1qlKgFQMAdhMFJYWOK5DCTIguSfb4kyTh1:1uxGkU:qi227DTT8CO1tzZnI23-5i3SYQC2v9E5_5iWmAKpabA','2025-09-27 03:16:26.611937'),('81t3qmmcdjz10e3b5ztk3cvxhx050v72','.eJxVjDsOwjAQBe_iGllmvf5R0ucMlj8bHEC2FCcV4u5gKQW0M_Pei_mwb8XvnVa_ZHZhgIadfmkM6UF1qHwP9dZ4anVbl8hHwg_b-dQyPa9H-3dQQi_ftUQ3oz1bCyQMAaImRc4IZWTIiDE6qTTNDqUFAJdwAJkBVcoiKc3eH_4PNwg:1uxi1q:rfijqeCkKRzyf2gEm8unaU9HdGpQbilMcuKxxp_9qt0','2025-09-28 08:24:10.745591'),('84op5vygiqyrzyzjjzin9ghs37ahlps0','.eJxVjEEOgjAQRe_StWkcOnQGl-45QzNtp4IaSCisjHdXEha6_e-9_zJBtnUIW9UljNlcDEBnTr9rlPTQaUf5LtNttmme1mWMdlfsQavt56zP6-H-HQxSh2-d2BfViAotcFLnStfGJA65aQhYqDSkCKqJyAOh56zspaAjxHJ25v0BPfI4Jg:1uxhjt:FKHV1-S6WB0QzGnwQ2kRHZfS1yijtDjyKhV2Ho2oyps','2025-09-28 08:05:37.938130'),('8kx3xv6ny24cxg3k3etp1dvdesj19409','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uxjQp:iGO58rd0XLK_5UwPOCp6A4gYjoSIU42TLxuwA8s-TpE','2025-09-28 09:54:03.112388'),('8th675x46t0t76nbmikvhcax64b7vgex','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGb0:2t8huLx33v2yLmopbSr1y6gJWvbalyoHh1se8AW7vDU','2025-09-27 03:06:38.593938'),('9dcr8pqfdff3o66to60z5utvn1htkake','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxFWU:_cSLzmMasmuRmCfMtYYqFofoy-VRxR4ReEPsNJFYVak','2025-09-27 01:57:54.743190'),('9ewroisxf5apjn4m1rohrcya5cldi4eg','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxGWh:NxRGfDgF7FOVV7dB6irwFDRK2TZ0RefL87tC3tyqI8c','2025-09-27 03:02:11.106705'),('9igvyi2kwae1mcfbpigfl3cha10nauch','.eJxVjMEOwiAQRP-FsyFld0PFo3e_gbAsSNXQpLQn479Lkx70NMmbN_NWPmxr8VtLi59EXdSI6vQLOcRnqnsjj1Dvs45zXZeJ9a7oo236Nkt6XQ_376CEVvqaiIANE_S0w-CEkFGQxwwZyAA5C52anANnipIwgnUSMp6tTRHV5wvkLDfL:1uwyvd:5bvyhSQ2jIq7QbFOncm8Pap404NVaR6bNCfwL_1s64I','2025-09-26 08:14:45.676535'),('9zvhx63tvt04ujkc4fbjpsqcn9e0lf3p','.eJxVjDkOwjAQRe_iGllexhslPWewZrzgAHKkOKkQd4dIKaD9773_YhG3tcVtlCVOmZ2Zko6dflfC9Ch9R_mO_TbzNPd1mYjvCj_o4Nc5l-flcP8OGo72rX1wlZxWSQIgUdVKVE0yBLDGCudJ1kqgCgokAxV8oCxktgQmJS2JvT8ogDhc:1uxGzA:WDsPtX2h5LLHCwf7TUXX8ggGzGHEPqDQ4E7dU6twDw4','2025-09-27 03:31:36.669737'),('a3winx6kgf51r1tbyqz10x02qbun9cfc','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKvO:m1yFO7TKPulULp0wb5d2PO0zs8BU9xWLgq96Ma_vtfo','2025-09-30 01:56:06.833904'),('a5bwwbbbfps1aumogyc23gyp5ewg329u','.eJxVjDsOwjAQRO_iGlkmu_5R0nMGa73e4ABKpDipEHcnkVJAM8W8N_NWidalprXJnIaiLgrV6bfLxE8Zd1AeNN4nzdO4zEPWu6IP2vRtKvK6Hu7fQaVWt3WIAs4iBPRb9OQdCknMcO4cFgbL3pvC0cVsEU0QYNtxD7YzCCykPl--_Tcm:1uyM9l:TkHjedHbzsloBGvIDb_eeVhWc5COLZaA9PnYsmiY3V4','2025-09-30 03:15:01.831588'),('af634d1y918cf83zg6keutmao6e9qouc','.eJxVjDkOwjAQRe_iGllexhslPWewZrzgAHKkOKkQd4dIKaD9773_YhG3tcVtlCVOmZ2Zko6dflfC9Ch9R_mO_TbzNPd1mYjvCj_o4Nc5l-flcP8OGo72rX1wlZxWSQIgUdVKVE0yBLDGCudJ1kqgCgokAxV8oCxktgQmJS2JvT8ogDhc:1uxGzB:EM5L-UoE__9M5b8wk-Yhk3QyXwabrVAyJvi2lXU9ZyE','2025-09-27 03:31:37.497753'),('ag4prldwsdc4pwstfyswh09oj2qc26dy','.eJxVjEEOwiAQRe_C2hDoNMC4dO8ZyMAMUjU0Ke3KeHdt0oVu_3vvv1Skba1x67LEidVZWXX63RLlh7Qd8J3abdZ5busyJb0r-qBdX2eW5-Vw_w4q9fqtjbA3Rgxncn7AXMhyGgkFACgUiwkcEObgETyGMRggZ4fMNhA4Ker9Ae2ZN9Q:1uwuku:eHbxhi0fMPqG4UIPHu0ksdc1i7fMp_HX5rjz_09NLu8','2025-09-26 03:47:24.937536'),('aj4h1bgdef8sthjj2u5xkpvdo85d77jk','.eJxVjDsOwjAQBe_iGln-JHZMSZ8zWJvdNQ4gW4qTCnF3EikFtG9m3ltE2NYct8ZLnElchXZBXH7XCfDJ5UD0gHKvEmtZl3mShyJP2uRYiV-30_07yNDyXlswxNpaFaztBiKTjFGph0AOAyuG5H0yOBh2iMn3asfWoabEAB1p8fkCM_Q4vg:1uxK8f:pmJP2iPQDwOoZJiG91GM24kspYRr3CoonRAwqVN9-4Q','2025-09-27 06:53:37.365028'),('aju7avceenvf7meuophudns38ezp8g50','.eJxVjDsOwjAQBe_iGln2-pelpOcMlj9rHEC2FCcV4u4QKQW0b2bei_mwrdVvgxY_Z3ZmYJGdftcY0oPajvI9tFvnqbd1mSPfFX7Qwa890_NyuH8HNYz6rWVBjVobBGknApQyCAKXlLJJWlNIxSQFJogoXMlB2wJAiJODWAwRe38ABlc3wg:1uy4JZ:wqlUMaZ7_GwIhaYeLcf4IB5qSJDuFgbIZNQ7fBCBfQw','2025-09-29 08:11:57.739658'),('art3dfk5c0iupwqejfoef7xxomcmog66','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLKh:lBN1zoq1RlM6DDm8QjRbaaKyD21-HcFPVXneG9bFFdQ','2025-09-27 08:10:07.487895'),('axr0cffph5s0ea1ywg9jebk073atpnv6','.eJxVjDsOwjAQRO_iGlnrxJ-Ekj5nsHbtNQ4gW4qTCnF3EikFNFPMezNv4XFbs98aL36O4io6AHH5bQnDk8uB4gPLvcpQy7rMJA9FnrTJqUZ-3U737yBjy_saWKPre4UROfVpDzUaA4a1TZoU2zgSMAMPCkJCInDBRbIDdWySAfH5AlM6OW8:1uxG7l:-ScqzLQArP8VpqnyUGXDg43Rw1RR5tHHYc_x2p69Kfg','2025-09-27 02:36:25.762795'),('b5vf1fn9edjn008re00gjtbzqcwcc2aq','.eJxVjEEOwiAQRe_C2hBAKOLSfc9AhplBqgaS0q6Md7dNutDtf-_9t4iwLiWunec4kbgKb8Tpd0yAT647oQfUe5PY6jJPSe6KPGiXYyN-3Q7376BAL1uNTnvHHAYwGrOz4MkhWG8GhZa1v-SgCBg1pTOAc6iYQk46q5zTFonPFyI2OUo:1uwyuE:4lS3od0-keeIyYH74c_OSpDfz71-LeHnVImvb6wK2Tc','2025-09-26 08:13:18.210542'),('b9prtna4di3ufifgji1ibezpsozu300k','.eJxVjEEOwiAQRe_C2pAMFAou3XsGMjOAVA0kpV013t2QdKHb_977hwi4byXsPa1hieIqALS4_K6E_Ep1oPjE-miSW93WheRQ5Em7vLeY3rfT_Tso2MuoiZ2bNIDznPVkySsD1rBBBks8k1EKVGZtLXJ0joHQsleIs84qJfH5AiVCOI4:1ux0yv:yTTsZI7UDk8GDJdtKxfNhK794_8andpqQWTT5weWD-M','2025-09-26 10:26:17.142932'),('bibpjmverniarjmxz2nih3fkomtazv8m','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxGbQ:GtYVCmjr5l7hbvFpclmbLZff-5eNdf2lZqq1QZNLiNw','2025-09-27 03:07:04.575873'),('bim27uzrvz9p4t7hoheqd6lpdfyzhk9l','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uxjc5:i4v7ofyWsmof_4eZS35lskmdtxgnUl23wqHQMFXfMfo','2025-09-28 10:05:41.725603'),('bphjuj1r5ivahyqo36x1rgtcb9xbc97s','.eJxVjMsOwiAQRf-FtSHA8Cgu3fsNhIFBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hzuzMNDv9bhjTg9oO8j22W-ept3WZke8KP-jg157peTncv4MaR_3WoCRlD06bSWJx4MAQKGsnFF7blCATyqK8swVT9IpkQSAhDEkhFQr2_gDJIDdo:1uxhkg:XFrwcNOMdcEx4ROS9KYQiV44kB71Cp94DQSFzZX_yYM','2025-09-28 08:06:26.746864'),('bt476nc07ipcsdvi4ofs9fc3bgpge1v4','.eJxVjMsOwiAQRf-FtSE8hIBL934DmWEGqRpISrtq_Hdt0oVu7znnbiLButS0Dp7TROIitI7i9Lsi5Ce3HdED2r3L3NsyTyh3RR50yFsnfl0P9--gwqjf2qqgM3lHgAFJuRyV0mxz8GAgYizArM6xeI6oiK01FDxaKt4F4w2I9wdDXjjH:1uxi8N:ZXM2WZLKmfOtwLtuiCyUFUEJKlgJir0WTSVtRcCfdJ4','2025-09-28 08:30:55.236492'),('btveavz0f0xo9vqn52838bl9obg6pkqt','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKsW:b3hCdTNpXPASaQUnDnA_YepWwAxPij7pd_xY0iuIqzs','2025-09-30 01:53:08.590431'),('bum8ip35y3llulyw4xrren9xxf2a4ocl','.eJxVjMsOwiAQRf-FtSEgb5fu-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2YVJq9jpd0VID2o7yndot85Tb-syI98VftDBp57peT3cv4MKo35rIYV0gAC-BI1eo0nWeUFnsDYXpOAIIZRE6IIwWhuXnDYJtCBlirLs_QE_WTii:1uxK9f:LBbB0IbYWBi7EUum_MwPqYnQWhEaVTh8U-IanoD5bi0','2025-09-27 06:54:39.231130'),('c03d1i7mof5uujtyg82b4pk13uq1ckwb','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGkw:7-8DbiCeabh_qSiheTV65u0qJERVJnO4kxwS1OQpSeU','2025-09-27 03:16:54.645213'),('c5bub34hzbge5ybe9kmo1v738uf8vt1m','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLAL:mohpgASo_vlq72AX_oQLzUICgcFQVHak6bqdFSmEW3U','2025-09-27 07:59:25.139715'),('ca0ggh84nmnuzyr417mzokqrh7p6ad6i','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLTX:7qmMhay7hQRr8EwqMrD23hjQJlpdFbIckNCG16yyCVo','2025-09-27 08:19:15.928086'),('cf07fwfgfja2ot4rvm7xj1yq59es5yje','.eJxVjEEOgjAURO_StWkKUtq6dM8ZyPz_W0FNm1BYGe-uJCx0O--9eakR2zqNW43LOIu6KNeq0-9I4EfMO5E78q1oLnldZtK7og9a9VAkPq-H-3cwoU7fGh7nhoK4ADhJltvO9J1rxCZwsraXyD5wI63xnhFhrCeCp5AIIRn1_gAswjlc:1uwyuF:GpGWGiHtOhMhYdwGd8Y85AtmyzvyKXDolTOfR0ZEbJs','2025-09-26 08:13:19.717145'),('cfoi7a5a1kn06h3n0ep6zbgd2lvyb5am','.eJxVjDsOwyAQBe9CHSEwX6dM7zOghYXgJALJ2FWUuxtLLpx2Zt77Egfbmt3W4uJmJHfCB0ZuV-ohvGM5FL6gPCsNtazL7OmR0NM2OlWMn8fZ_h1kaLmvR6mFHYRRBqQdZTKaWUTjGUaDlmEniSvEBFF4FJ14DUqD1JwrCIr8dhbKOEM:1ux3iA:mxwWm3dYTM9TERzucQOmiq7-Do4Ut_9XOKS-2TqNTJQ','2025-09-26 13:21:10.615532'),('cp5bkm92bfleuv8r6oj3avyf5olico78','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uyB2c:kIua-NUtlG2TPIOxSQRw_nS-Vnpf7oubqAdaQrwoRCM','2025-09-29 15:22:54.358808'),('cqeiopf087z4l6ml1m70fvmcvancftzz','.eJxVjEEOwiAQRe_C2hAYwIJL9z0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kbgIY404_a4J84PbjuiO7TbLPLd1mZLcFXnQLseZ-Hk93L-Dir1-a0XJcQI9EHhdsrMGvSlaQWBAk8-oSwgZVLGgkIlDGhQkFTwxuhKseH8ANBc4iw:1uy7nn:RwYY7M0dMygIhx8yq5rbV8JO-lSjrazEBwadfakRUy0','2025-09-29 11:55:23.268864'),('cwcn4ijmu1gn7rw0mu4tss36sf72u40t','.eJxVjDsOgzAQRO_iOrLA-EfK9JzB2rV3Y5LISBiqKHePkSiSaqQ3b-YtAuxbDnulNcxJXIVSnbj8UoT4pHJU6QHlvsi4lG2dUR6KPNsqpyXR63a6fwcZam7rDgn1aBJD7yG2xAGBHXm2AKTdqIm1Uz4mRGu8MkZp1gP3iWzDJD5fakk5aA:1uxGzZ:VX6e6_GVWuV37emzbKX3Xu6dDfgFJSnKQi3JQKzQF_A','2025-09-27 03:32:01.616423'),('d5uee666l47uu4p6tcv0hqn3xqxusaas','.eJxVjEEOwiAQRe_C2hAKpYBL956BzAyDVA0kpV0Z765NutDtf-_9l4iwrSVunZc4J3EWzorT74hAD647SXeotyap1XWZUe6KPGiX15b4eTncv4MCvXxrUg4z6sESMw0TBzZ61ACgApINiimYHDIReuDRcrI-TIYUGobkyYn3Bz6YOYw:1uwz0k:kNX9jho4G8L58dJfiNMrpjf9eCWhX9nMqwntFlyZWsE','2025-09-26 08:20:02.595715'),('d8q6drvi6fsofphvelg3484xgbzxfc58','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLPR:DzKPGwEGsEKqJLVrtkDzrGB9p4YUzZRvDAFPehKd27w','2025-09-27 08:15:01.738992'),('dks4r5odnoc5edrysci1l73k8ae1pf7b','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxdK7:bY65eAIeSNxpqeV12-UpCfKQA9We6vS67gj0stR1O78','2025-09-28 03:22:43.807527'),('dxstku551w49g61qi0mzraxjrqiuoqds','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxL9l:AiUKd9y1GnAcTGH91qRT3BYzbMNK2S4kVyr7-tbGtLo','2025-09-27 07:58:49.663906'),('dzmm7kufq9ugb4vrih11jvglbgie4wtz','.eJxVjEEOwiAQRe_C2hCgAoNL9z0DGWZQqgaS0q6Md7dNutDte-__t4i4LiWuPc9xYnERxmhx-qUJ6ZnrrviB9d4ktbrMU5J7Ig_b5dg4v65H-3dQsJdtjTdDXjsXNFnmrDSCUZoB0xlygrAx53TwTNmSU4NXfkBIHAgMqWDF5ws5ijhu:1uxH0c:haLr5zgkaMf3j1Q8FMPmHVsqsIV8-eVXdXdG0t6x7as','2025-09-27 03:33:06.889005'),('e1czd556yqsb52nz6gc2qcfz0zdxmttv','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyKOd:yUmwbY2po7RM7I1vj6UyB5iLpF6oGLww9W_xBicg4bc','2025-09-30 01:22:15.697706'),('e2vm9hw7sq8edz03f4hkuvue8fiwk7kb','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uy9V4:0LUW7Y7sR0_X7rmgGeGOueKCl1_OPfHof6h1doJPZ6Y','2025-09-29 13:44:10.914850'),('e8f1d6cy8i8iibxb8hzlvustjnpj0pfh','.eJxVjEEOwiAQRe_C2hAYwIJL9z0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kbgIY404_a4J84PbjuiO7TbLPLd1mZLcFXnQLseZ-Hk93L-Dir1-a0XJcQI9EHhdsrMGvSlaQWBAk8-oSwgZVLGgkIlDGhQkFTwxuhKseH8ANBc4iw:1uy9NQ:8752ZbAhhQ43rjgyM8-c_cdh6ME4sOnt-cQ8s80krXk','2025-09-29 13:36:16.206732'),('e9erva78x53y1wodug15m0v8x2kdbm32','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uxjCn:X5bIRVhgFFXBRXiOoU6Mxqht4vUIZUBVvweljMuny24','2025-09-28 09:39:33.244744'),('ec7bnhyv4w28i2pficvf5yoetit2u0uu','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLKe:MZgvipGNtdHc9csjmQrwnSFIF5FrldNMKzqtJmLUSUw','2025-09-27 08:10:04.898223'),('ei3s10q80j89ck8qcwpz4lmi45t9me1i','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxFWU:_cSLzmMasmuRmCfMtYYqFofoy-VRxR4ReEPsNJFYVak','2025-09-27 01:57:54.537853'),('ep7s1faeedpfpzd44axw42se2pm0z70x','.eJxVjMsOwiAQRf-FtSG8YVy69xvIAINUDU1KuzL-uzbpQrf3nHNfLOK2trgNWuJU2JkZdvrdEuYH9R2UO_bbzPPc12VKfFf4QQe_zoWel8P9O2g42rf2KCx4h9VKp0joSoSYsilSg5Tgg1FVgxLO-ExB5CIcQdAobSWoRbH3B9hBN64:1uxhoS:XT8UowumQnIBGI_zS9f_hFRu3NTm_elzN0PE6f_NkZ4','2025-09-28 08:10:20.732757'),('f4dmol9srb2azzynw1wxv1un8itx13fj','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxH1g:iBLaKyTT5IBdEW66_lc9o_WcW73YHfCu2pC16tf5ZBw','2025-09-27 03:34:12.802756'),('fdyrblwxrg1bf8hydkaao1u9n2boey80','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGkw:7-8DbiCeabh_qSiheTV65u0qJERVJnO4kxwS1OQpSeU','2025-09-27 03:16:54.599184'),('fiddr8s1vduwlklrn4swvzh9fjz31tha','.eJxVjEEOwiAQRe_C2hCwDMO4dN8zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIizgrE6XeNIT1y2xHfQ7vNMs1tXaYod0UetMtx5vy8Hu7fQQ29futMELUzNChKBXVipIiIZAFIMxQ0bJ2xBA40Aiqr8kAmslKOtaYi3h_-5za_:1uxH89:Ya4MGYcjAszXSywL2sY-3r3CJbGTaqBVEI70KCaQzKM','2025-09-27 03:40:53.758256'),('fm1e0cof76w3ujqqbpysh9t2a7foqv8s','.eJxVjEEOwiAQRe_C2hCwDMO4dN8zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIizgrE6XeNIT1y2xHfQ7vNMs1tXaYod0UetMtx5vy8Hu7fQQ29futMELUzNChKBXVipIiIZAFIMxQ0bJ2xBA40Aiqr8kAmslKOtaYi3h_-5za_:1uxH3w:IvXYqkHQX8Uziqdy5hiwIcTdm6GyTu9B4G60_9aBODc','2025-09-27 03:36:32.923197'),('ftzboup2f5cg6jclrll8nku6zqmd2toc','.eJxVjDEOwjAMRe-SGUVy4tYpIztniBLbJQWUSk07Ie4OlTrA-t97_2Vi2tYSt6ZLnMScjQNnTr9rTvzQuiO5p3qbLc91XaZsd8UetNnrLPq8HO7fQUmtfOsUOACQH8AjAvXsuYNAJD6wwsDQA5Jo5yh7TIIahANlzCONjhTN-wMAuje5:1uxGxX:8VYXTrZUA-wE4RTwDan2IULfLtISvbdKwCaf4CmAgzE','2025-09-27 03:29:55.480985'),('fwgyfq7b98o39fo0kn87y3ogqx1ec0m8','.eJxVjEsOwjAMBe-SNYrkOB_Kkj1niBzboQXUSk27qrg7VOoCtm9m3mYyrUuf16ZzHsRcDMDZnH7XQvzUcUfyoPE-WZ7GZR6K3RV70GZvk-jrerh_Bz21_lsXjxo7X7rqktcA6COBY1B2JAlLql6rwyqMwaUkHLFowFhJRBg68_4ANQk4-w:1ux1Xl:dsxiaG2PD2shjJsqTKIa1nRrtnOhERpXfLWjvM3kQio','2025-09-26 11:02:17.696094'),('fz7xms95hzroycac8sshn6gy3ycd63z1','.eJxVjMEOwiAQRP-FsyHIliIevfcbyC4LUjWQlPZk_Hdp0oNmbm_ezFt43NbstxYXP7O4irPS4vRLCcMzlr3iB5Z7laGWdZlJ7oo82ianyvF1O9y_g4wt9zVZ7ZgQDCTSl1FbHIy1BAMopB6E4JhBuWAcoknGQeIOiFVAS6P4fAE8LjlC:1ux4mS:r65kb7Ff0fO89sWql4ADZcWp85ulvZBw-Iv3I3q1Kgg','2025-09-26 14:29:40.352917'),('g0l62s8yr6g9bcapd65uqu075xc7dv1p','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uy9Rc:QfuSLkNJ6Zp4bI-z3pZtKqEpGfZmbxX9DZyxuplwnPY','2025-09-29 13:40:36.482403'),('g11sg584epovx8bw9tf0ni2p208ayudb','.eJxVjMEOwiAQRP-FsyHIliIevfcbyC4LUjWQlPZk_Hdp0oNmbm_ezFt43NbstxYXP7O4irPS4vRLCcMzlr3iB5Z7laGWdZlJ7oo82ianyvF1O9y_g4wt9zVZ7ZgQDCTSl1FbHIy1BAMopB6E4JhBuWAcoknGQeIOiFVAS6P4fAE8LjlC:1ux4lj:odZHSSfpuvfnfnqcAfFaBpffACP9eLnNdp60yHFonA0','2025-09-26 14:28:55.022955'),('g4h6kampoufvfis81dkikru68lt3cpf0','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB6G:uMAYUs3d11B40AiB-8cHutkoS5-z-C29gQAJop6gD6g','2025-09-29 15:26:40.059431'),('gglqgp5j06ng58ih91zmzesm5bpg7z96','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLEF:m4b_8gJpKFdqJe8pffgGu-QNulDSJhBf24AbsweBxOQ','2025-09-27 08:03:27.251457'),('gzzwye7yu276l2znqi4kj4c9gml2cxxk','.eJxVjMsOwiAURP-FtSGAtwgu3fsN5D5QqoYmpV0Z_12adKHLmXNm3irhupS0tjynUdRZOQvq8NsS8jPXDckD633SPNVlHklvit5p09dJ8uuyu38HBVvpawJmIBbkPMSIPRwJkMUhmxtzNBRCdCHAYBGEgu3Q-RObbNB669XnC3JrOTw:1uxGyJ:mtHPiYi1yf17yYxVa71unWcsjQbOta3a2W-koYJDKQg','2025-09-27 03:30:43.358830'),('h0gu878ziiswjroi15cr6o143eceqafe','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLPU:qN_wLxgkCA4cMn0uUyYy2crT3zRe_B8sEKfeOLL5_WU','2025-09-27 08:15:04.386898'),('h6qvzvvz8mlj1wokf9r13xm4dgzkpn7h','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyBuL:bVd0cv3TkLsAlZRbSgHWj7fxFAL9D4xtrVAJLKZ1uBs','2025-09-29 16:18:25.195819'),('h76wl6srln9gp0okfebgcs0x4oavwz3v','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyKdK:FKx3tl5gTrSNyr68x40WLeRwa0JPy5FeIeQLW2ZmQ0I','2025-09-30 01:37:26.278104'),('hk03ysplvz6h6a444b9dcp4qmhyfnlru','.eJxVjDsOwyAQBe9CHSEwX6dM7zOghYXgJALJ2FWUuxtLLpx2Zt77Egfbmt3W4uJmJHfCB0ZuV-ohvGM5FL6gPCsNtazL7OmR0NM2OlWMn8fZ_h1kaLmvR6mFHYRRBqQdZTKaWUTjGUaDlmEniSvEBFF4FJ14DUqD1JwrCIr8dhbKOEM:1ux3iA:mxwWm3dYTM9TERzucQOmiq7-Do4Ut_9XOKS-2TqNTJQ','2025-09-26 13:21:10.713686'),('hwqwiw7u0qx9w4y0j4gysnu1x4t04d37','.eJxVjMsOwiAQRf-FtSHDtDzq0r3fQAYYpGogKe3K-O_apAvd3nPOfQlP21r81nnxcxJnocTpdwsUH1x3kO5Ub03GVtdlDnJX5EG7vLbEz8vh_h0U6uVbm0GPVhnLiBiyGwAcQoLRgptGMho0qmADkHWMPOXs8qAsYAQKWiUW7w-awTag:1uwxSY:oyuSHf5s3S_5nTDNnGFM80XzK7OpBNPkuQlRxVXNdbA','2025-09-26 06:40:38.493870'),('i26ivlme0dzl890ngpgai0jmrxqc4fkk','.eJxVjMsOwiAQAP-FsyFQ5eXRe7-BLLuLVA0kpT0Z_92Q9KDXmcm8RYR9K3HvvMaFxFVocfplCfDJdQh6QL03ia1u65LkSORhu5wb8et2tH-DAr2MbfLE1gUN6G3mZCwGRpdJT2cwxAyE6DRo57MK3lzIU56UddooCjaLzxcPbjip:1uwugl:srzcweqj77TKBfZrBO6CS_GG_hspn5sJy7ZD2tTJS2U','2025-09-26 03:43:07.229475'),('i4pinbhx3gxpdld0e0hnlhc8q9w70dqu','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uxj11:1PGmmudkzPKBAkN5XIvufYjm-GXT9zNNNlnpN4tq1jU','2025-09-28 09:27:23.994701'),('i69xfeuijqwj585ck3l1fph1w5q3tus9','.eJxVjL0OgjAYAN-ls2mAllIc3XkG8v1a1NCEwmR8d9OEQde7y73NDMee5qPINi9srmYczOUXItBT1mr4Aes9W8rrvi1oa2JPW-yUWV63s_0bJCipfkMMDbAjpKDk-16JR3TU-hEjKvTkxZEMIap2nUrrOAbXimPoGgA2ny831zlg:1ux02R:dk-VKWxSOmsySP0M4WjLe7b8iEwuP9DWwSWpzEF1cMI','2025-09-26 09:25:51.587530'),('if2f7hqxr97f8u9n64m667dkaix6lt8o','.eJxVjDsOwyAQBe9CHSEwX6dM7zOghYXgJALJ2FWUuxtLLpx2Zt77Egfbmt3W4uJmJHfCB0ZuV-ohvGM5FL6gPCsNtazL7OmR0NM2OlWMn8fZ_h1kaLmvR6mFHYRRBqQdZTKaWUTjGUaDlmEniSvEBFF4FJ14DUqD1JwrCIr8dhbKOEM:1ux3PV:PPGXDnwsMafV-caF37NWMrsdbO1-nU-tcXw1eMsvfbc','2025-09-26 13:01:53.930277'),('if414o22fov7qsm4oq12ah9mwioz2n8k','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLU3:BnRVHf-hJyDcis5h80gIcqlRxin1CwaCo9qIvzyEMR0','2025-09-27 08:19:47.511013'),('ikkbmvunbltxeq2nchbs1k6gos9dw0jw','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGux:dS-u9GtcJ3C8Wd4oIBKwTantq7RBTBx0-r5jK7-h0s8','2025-09-27 03:27:15.819755'),('imqfzf0hgkt2po2253uixlestn4bpcvl','.eJxVjLsOwjAMAP8lM4rqxnnAyM43VHbikAJKpaadEP-OInWA9e50bzXRvpVpb7JOc1IXher0y5jiU2oX6UH1vui41G2dWfdEH7bp25LkdT3av0GhVvqWAWzwaCMjZiSXKQ-ACYBEHPBANrDxJjpDeLY-iE0Q0I88sjhj1OcL2D43ZQ:1uwxXC:BKqQaaiUxfh9uUarthT_aRvWM3GrmfxOu_6DH7iIM7k','2025-09-26 06:45:26.164034'),('ineab0zwywg53eeav8r6hhnxk1on8e3d','.eJxVjDsOwjAQRO_iGlkmu_5R0nMGa73e4ABKpDipEHcnkVJAM8W8N_NWidalprXJnIaiLgrV6bfLxE8Zd1AeNN4nzdO4zEPWu6IP2vRtKvK6Hu7fQaVWt3WIAs4iBPRb9OQdCknMcO4cFgbL3pvC0cVsEU0QYNtxD7YzCCykPl--_Tcm:1uyM88:fp2mZFWKJraz4aWPF7-ny7CjOhRyxOd1zrS8eoz288c','2025-09-30 03:13:20.448598'),('iqjoynjtozsedh2rooirryss0wpx6sjj','.eJxVjMsOwiAQRf-FtSE8hIBL934DmWEGqRpISrtq_Hdt0oVu7znnbiLButS0Dp7TROIitI7i9Lsi5Ce3HdED2r3L3NsyTyh3RR50yFsnfl0P9--gwqjf2qqgM3lHgAFJuRyV0mxz8GAgYizArM6xeI6oiK01FDxaKt4F4w2I9wdDXjjH:1uxi8x:Cg1yyt_AYwk7r3s9vI4BU3z_PdeTsQsvGpVmDtnbFMQ','2025-09-28 08:31:31.551984'),('ivdrmpdtd84p6n2eub8jekv37dkwosli','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uy9Sb:IvDp2joq40bR5UOcLs9kx4FYxPvWnME95nFb9D24vYU','2025-09-29 13:41:37.581040'),('izjl4f82zk7lgpnqdrwmbnbdl3kbac89','.eJxVjEEOwiAQRe_C2hBgRKYu3XuGZmAYqRpISrsy3l2bdKHb_977LzXSupRx7XkeJ1ZnZdXhd4uUHrlugO9Ub02nVpd5inpT9E67vjbOz8vu_h0U6uVbDy6HhD7aIGKFJAFkDNGR-CDMDiIexbgUEIyPfEKwBGg8sqEhe1bvD_wOODw:1uwuy7:3PB6S9qSqxhm7c5RoY_5IpCNTm3z9mgthXNagh6aECQ','2025-09-26 04:01:03.757009'),('jkreoivf3pgfknp6i2tjqgma56jaj3ov','.eJxVjDkOwjAQRe_iGllexhslPWewZrzgAHKkOKkQd4dIKaD9773_YhG3tcVtlCVOmZ2Zko6dflfC9Ch9R_mO_TbzNPd1mYjvCj_o4Nc5l-flcP8OGo72rX1wlZxWSQIgUdVKVE0yBLDGCudJ1kqgCgokAxV8oCxktgQmJS2JvT8ogDhc:1uxGzC:4ItB5RQIoWuTnQ2tLzuqU0aiFyBhP_XB6wVd0UIGbm8','2025-09-27 03:31:38.217345'),('jnw1yl2o2ylppio7nsjm7vbfj7lldbb6','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyKQd:ezNnMKUj_r3dDERUZD-dk6OKzu1zMjf_ZktRPW8KtHw','2025-09-30 01:24:19.271960'),('k0tddbir6hgll1xtdpantyla90zwt4u8','.eJxVjDsOwjAQBe_iGllZE_8o6TlDtOtd4wCypXwqxN1JpBTQzsx7bzXgupRhnWUaRlYXBc6r0y8lTE-pu-IH1nvTqdVlGknviT7srG-N5XU92r-DgnPZ1oEFAH1g9JbI9D0iAQaJhjMwZUsSXbQQLZ1N57qwMecRs2EPSbL6fAFTJDlb:1uxGa8:Lu8FkqDR9BYoRjZY3P_S8qWh_x2R6AkLqngTFEcjgdA','2025-09-27 03:05:44.154159'),('k9n7iss4pelua7fax7qxydky4bsmhcni','.eJxVjL0OgjAYAN-ls2mAllIc3XkG8v1a1NCEwmR8d9OEQde7y73NDMee5qPINi9srmYczOUXItBT1mr4Aes9W8rrvi1oa2JPW-yUWV63s_0bJCipfkMMDbAjpKDk-16JR3TU-hEjKvTkxZEMIap2nUrrOAbXimPoGgA2ny831zlg:1ux01n:7cIUojGwM8LDzttjgngu-kl-ss7GsVVXKxLUFmLaKQk','2025-09-26 09:25:11.954839'),('kclflxh04my5eal9f0f9fr78f7z5d60w','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uxjQp:iGO58rd0XLK_5UwPOCp6A4gYjoSIU42TLxuwA8s-TpE','2025-09-28 09:54:03.242255'),('ke6hce2mtxle24hb7lyjhryv81k4jdb6','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uy9Yi:9CicW5UlviitsItNCjlmWFUrxTvENwZuW6jQCC2sak0','2025-09-29 13:47:56.441539'),('ki2oekn2ammu89auajob2mq74myakyjo','.eJxVjMsOwiAQRf-FtSHMDBRw6d5vIDymUjU0Ke3K-O_apAvd3nPOfYkQt7WGrfMSpiLOAsTpd0sxP7jtoNxju80yz21dpiR3RR60y-tc-Hk53L-DGnv91g5zTMXpASEVIpvJW21YawA1GFscjwkJDSATMSgN3jofWVkPMAKK9wfAQzZ5:1uwxNb:uYAcaqHkB-hKGlBLJI_eYRTowtcDgn98WTJkk4wT7-o','2025-09-26 06:35:31.642931'),('kpu5zcvqg0tqt9ioytgupkxos79ivq8j','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKmM:Gi_Znk_Iwc5GIpYFsPBIBWHP-GJnDfV6ZAR4RpuLj7Y','2025-09-30 01:46:46.547358'),('kxkb9cftknj1ykec1zv3jqf3m2mv5jn0','.eJxVjEEOwiAQRe_C2hAYoAWX7j0DYTqDVE1JSrsy3l1JutDVT_57eS8R076VuDde40ziLACsOP2-mKYHLx3RPS23Kqe6bOuMsivyoE1eK_Hzcrh_gZJa6WE9skcmHyg4oywZ4sw-MMCAwYwTOCQaLGXIXqPSKn3HATpkbQ2J9wc7bjiZ:1uxRAD:jBHWvNN2cq0wFmLBzHdjK3e_hnQfc1iDn4HunsxzA8c','2025-09-27 14:23:41.186733'),('ljrwoxg64tmmpecop40dixloinj6h6ck','.eJxVjMsOwiAQRf-FtSE8Bgou3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmE7DT75hiflDbCd5ju3Wee1uXOfFd4Qcd_NqRnpfD_TuocdRvLQiUUZRKRqWNFEJ7iQRSWkeKAGWGWCh5b0tRCDY5U7RxRpKnCTWy9wcIwDhA:1uwz0J:a5m2vHUPpV4_3TxQfV0AFosP4fRtegxA6v5oLgNmvU4','2025-09-26 08:19:35.892222'),('lnzqr94045zo39824uppbni7iy2u7umn','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLD9:mPbTmDdbRvAjFOn_xQyRKphooLcmWv5D10FX8CXxysc','2025-09-27 08:02:19.847471'),('ly5s3ghvnyegkvofcl4ny8habcr6hvvu','.eJxVjEEOwiAQRe_C2hCgFIJL956BDDODVA0kpV013t026UK3_73_NhFhXUpcO89xInEVWlx-twT44noAekJ9NImtLvOU5KHIk3Z5b8Tv2-n-BQr0sr99BoLMNvhBB42ckBCZ9oBynD07F1JOltSADnBM5EzOirQ1bjQjWPH5AjuxOag:1ux1Fg:33-ADj8tiQc7Nmzf8fAxkAsrg6iXScp_MsRXljrfHNU','2025-09-26 10:43:36.798859'),('m0pgyaprkzpcqly1gd9m0wn1vocpw7mr','.eJxVjEEOwiAQRe_C2hCYAiMu3fcMZGBAqoYmpV0Z765NutDtf-_9lwi0rTVsPS9hYnERWntx-l0jpUduO-I7tdss09zWZYpyV-RBuxxnzs_r4f4dVOr1W2MqyjCjwsQWs4OiCQEVO8RoMaqYB_a6EIBNNGhTzrY4xcY6YO9BvD81IzgR:1uxiwg:6wsejh2Jbu0yMSHMvon4Q4CeFc-RonJaaZVGXz8ukkE','2025-09-28 09:22:54.237759'),('m5dif6s6oy1zf3wnvkertggpdd2jan0e','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxH1g:iBLaKyTT5IBdEW66_lc9o_WcW73YHfCu2pC16tf5ZBw','2025-09-27 03:34:12.817421'),('m638c55he6jyvoww6bw1f5o5nvek1jtd','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB5q:BPuKL55maR4eK6_8RmjdBSwB_HmKrXEtB_8bNkUXvIs','2025-09-29 15:26:14.604767'),('m69fkxsnk1ac7n6cbnzl0xsqfrttcvem','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxKD0:2fHy9PWi-QxufALPddk000nJnZXv0Zmnv8ruA5bAnJk','2025-09-27 06:58:06.724402'),('m71vdfj09gc86vcj1d57ipc1wfy5pl93','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxd2b:5viuCigjpUwLU_ewgYIAYVLs7u0EugaM1wQvhSvRAAA','2025-09-28 03:04:37.361280'),('mc1l5jy9f2q95rdnlrisso4dlgi190fg','.eJxVjEEOgjAQRe_StWloy8y0Lt17BjJ0BosaSCisjHdXEha6_e-9_zIdb2vptqpLN4o5G0zm9Dv2nB867UTuPN1mm-dpXcbe7oo9aLXXWfR5Ody_g8K1fOuUoXGEAdAjp-QkkjZAWb00AQSVQCLCgBpyG5kpc8sDeQfBJU9q3h_poDdl:1uwysX:qDtT9r936ENUWgzEoTZDjFsrNVzCoARc1bJVSbca4v8','2025-09-26 08:11:33.848834'),('mepdnz6mpj7qybqfes5afm0kn5d14d3g','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxGZR:U55RNSFr5WQ-9JPPhz0ElZveXnikljSdIC1Is5ayf9U','2025-09-27 03:05:01.030409'),('mh9j0gngz1ouma9wg824j2s4d9fsyr0w','.eJxVjDsOwjAQBe_iGlle_4Ip6XMGa3dt4wBypDipEHeHSCmgfTPzXiLitta49bzEKYmLAAji9LsS8iO3HaU7ttsseW7rMpHcFXnQLsc55ef1cP8OKvb6rYshDkDZOQbnrbJaK8s6eEraF-XN4DKfbVIGHYHWUAiLQ4UQ0AyWxfsDHXc35w:1uxhuX:jQZ4XRpbwtW4wh0spsxh1qjyjY8bvV3d56YVZA2dc4U','2025-09-28 08:16:37.808147'),('mkeyjejy2gwrhlljxto3jdhqinb43jf9','.eJxVjDsOwjAQBe_iGln-xl5Kes5g7XodHECOFCcV4u4QKQW0b2beSyTc1pq2XpY0sTgLrUGcflfC_ChtR3zHdptlntu6TCR3RR60y-vM5Xk53L-Dir1-a8DoDapBG02GIqswErILgyoeLAeIGUJBV8YA2XrL4LR3ylrWpAxG8f4AH2Q3rQ:1uxhkf:LGrKVwOgZzjOTwCNiEkx_o1mbBa9TFYBXUffaYGQnGg','2025-09-28 08:06:25.492307'),('mox98hh7tpasvt8elp56yexkk2wsinox','.eJxVjMsOwiAQRf-FtSE8hIBL934DmWEGqRpISrtq_Hdt0oVu7znnbiLButS0Dp7TROIitI7i9Lsi5Ce3HdED2r3L3NsyTyh3RR50yFsnfl0P9--gwqjf2qqgM3lHgAFJuRyV0mxz8GAgYizArM6xeI6oiK01FDxaKt4F4w2I9wdDXjjH:1uxi8x:Cg1yyt_AYwk7r3s9vI4BU3z_PdeTsQsvGpVmDtnbFMQ','2025-09-28 08:31:31.441413'),('mqnf21d421u6xnmww7k721jg31cmtm2a','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLEC:I8BLof1uGH-rFUSk06NhIxlM0b_ptSLz7v-sxnZbteE','2025-09-27 08:03:24.490275'),('mtgvau3e0vydo3rkv4nqurq3jsjebh4p','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxFJI:SAxFhB7d8nZRfLh_7HR7oM_WGa3Kwo7KFxgEVapnKKw','2025-09-27 01:44:16.182458'),('n3r3lov8fokdssawnffyoh8g2lbgkknj','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLUr:nvg7VJgrBj0R8tWvXCzm-38UxA5PS9VMQxyXHQ0MLi4','2025-09-27 08:20:37.140995'),('n5cr4cxcm5y6tplu71yqux2bpq9ayzyy','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB6c:6zEcJz8jyiieYnN-kT_ynLjXFRnZBe79Me7cCBOkbcI','2025-09-29 15:27:02.951576'),('nb3043e77ov8k00psm4lydvhl3wid2um','.eJxVjMsOwiAQAP-FsyEgTz167zc0yy4rVQNJaU_GfzckPeh1ZjJvMcO-lXnveZ0XElcRnDj9wgT4zHUYekC9N4mtbuuS5EjkYbucGuXX7Wj_BgV6GV9L4BhUIsRwNmiUZmcpa2avDCSvDdhLJqDoKQKZwIxM3geMFsmJzxc6ZDmK:1uwz0m:fI_wwFOOTVWIIWI_ry5EmVrdh4H_q4RNYG7BKFO4rEY','2025-09-26 08:20:04.065954'),('ncc7rvvgp0c4t3rwy44scuo871tjwo1w','.eJxVjEEOwiAQRe_C2pACU6Au3XsGMp0ZpGpoUtqV8e7apAvd_vfef6mE21rS1mRJE6uzsl1Qp991RHpI3RHfsd5mTXNdl2nUu6IP2vR1ZnleDvfvoGAr3xp8yIOQWDNiZ4ApCg8cKTvTZzTBAQJiiJCDWAIUwAxko--9M8xOvT9Owzj5:1uxGOK:cw2fa59Kihb5dFTcGdCg7cDsvwV4hdabwkzic5X-Pn8','2025-09-27 02:53:32.561929'),('nf3prrn8tvh60b99gqgktdmiycu3mioa','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLBH:OB-G0AyKYChzoHsVU9Kplb7Scprgg6fI221bbxbHA28','2025-09-27 08:00:23.527902'),('nf7h1oyglb2cvp2mqmoes1peawjaaywm','.eJxVjDsOwjAQBe_iGlmOE39CSZ8zWOvdDQ4gW4qTCnF3HCkFtDPz3lsE2LcU9sprWEhchevF5RdGwCfnw9AD8r1ILHlblyiPRJ62yqkQv25n-3eQoKa29sZRP8JASptRs4POD6gcxU4BEbN1pnmlGLUl9MawbWy2_Uzeo1fi8wUERTgf:1uwyvf:ZsLtr437z7h6o90yp2fnbDEryljIYHeIrYX13a1eWHA','2025-09-26 08:14:47.256178'),('nfmq2vr3owy7vayjyjja6r7kq38r48sl','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxL9o:3_9RZr1wieyx1SI3EPUEPB8WdisenHYKdz7h2X-Eqfs','2025-09-27 07:58:52.292536'),('niuctnadvhlknvqfdz5viiio4igta502','.eJxVjEEOwiAQRe_C2hAYoAWX7j0DYTqDVE1JSrsy3l1JutDVT_57eS8R076VuDde40ziLACsOP2-mKYHLx3RPS23Kqe6bOuMsivyoE1eK_Hzcrh_gZJa6WE9skcmHyg4oywZ4sw-MMCAwYwTOCQaLGXIXqPSKn3HATpkbQ2J9wc7bjiZ:1uxRAD:jBHWvNN2cq0wFmLBzHdjK3e_hnQfc1iDn4HunsxzA8c','2025-09-27 14:23:41.112255'),('nm781oexhzcy0hdumnd6pg86k5fxo7p4','.eJxVjEEOwiAQRe_C2hCwDMO4dN8zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIizgrE6XeNIT1y2xHfQ7vNMs1tXaYod0UetMtx5vy8Hu7fQQ29futMELUzNChKBXVipIiIZAFIMxQ0bJ2xBA40Aiqr8kAmslKOtaYi3h_-5za_:1uxH7I:y-7gTi-nDfwifqdtY6hnsAVdr2GDNdzGyW6RL_BMegE','2025-09-27 03:40:00.292947'),('nrol7hh2jh6zottx8e5rqz2v6g4s3o5k','.eJxVjDsOwjAQBe_iGllZE_8o6TlDtOtd4wCypXwqxN1JpBTQzsx7bzXgupRhnWUaRlYXBc6r0y8lTE-pu-IH1nvTqdVlGknviT7srG-N5XU92r-DgnPZ1oEFAH1g9JbI9D0iAQaJhjMwZUsSXbQQLZ1N57qwMecRs2EPSbL6fAFTJDlb:1uxQZo:Z9bvZHA5ysVN8Utc6W2S8LEP3rk3ZR65_LQPt1Pn3s0','2025-09-27 13:46:04.898035'),('nryejlz97atxg5dov0rga079y7t705lp','.eJxVjDsOwjAQRO_iGlleE_8o6XMGa71rcAA5UpxUiLvjSCmgnHlv5i0ibmuJW8tLnFhchB7O4vTbJqRnrjviB9b7LGmu6zIluSvyoE2OM-fX9XD_Dgq20tc5ac9kLDLAEEgn36MHThSSAusR2XjDGZV1QbHDW8YOgZRyzoAVny9UgDkd:1uxi0R:8GVX5SReGf4jDY4rRx3cd9osxyj6qRtQGoaURAg-WJ0','2025-09-28 08:22:43.051221'),('nznlu20vsubr2xih6ntfz2gj3oes83d6','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uxjCn:X5bIRVhgFFXBRXiOoU6Mxqht4vUIZUBVvweljMuny24','2025-09-28 09:39:33.320417'),('o0lmufwsjt6jw02n764srce3xpr487hf','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLR6:oml9VxE8dNx346Lnau1ojgSgvxN61Ei7wKZrCC_5fp8','2025-09-27 08:16:44.037872'),('o1v89ylam43qc0u8x8mpyo9uj5x58xh0','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLGm:RHGOhsqwylgXOT7xdyFfWPx2s_-0wF_ON52rm-r6llo','2025-09-27 08:06:04.271031'),('op7bsediah8giyeo79vtikre8vykkehd','.eJxVjDsOwjAQBe_iGln-JHZMSZ8zWJvdNQ4gW4qTCnF3EikFtG9m3ltE2NYct8ZLnElchXZBXH7XCfDJ5UD0gHKvEmtZl3mShyJP2uRYiV-30_07yNDyXlswxNpaFaztBiKTjFGph0AOAyuG5H0yOBh2iMn3asfWoabEAB1p8fkCM_Q4vg:1uxGuY:Zg12HEYhK8WmwJdT5DAEtlM22IjlQ1nzZQ0wue3b-Fo','2025-09-27 03:26:50.888084'),('ovu016wgzq7k802dqh0u8ikh4ebz1hll','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGb0:2t8huLx33v2yLmopbSr1y6gJWvbalyoHh1se8AW7vDU','2025-09-27 03:06:38.481689'),('p79gbmz8k0htc9lw26jkvnn67mow3guw','.eJxVjEEOwiAQRe_C2hDoAKUu3XsGMsMMUjVtUtqV8e7apAvd_vfef6mE21rT1mRJI6uz6p06_Y6E-SHTTviO023WeZ7WZSS9K_qgTV9nluflcP8OKrb6rQcYfBC01oO4Eh2wCZkLxRg6g9mRAekJvDVIDnPskKGwLcRGogVU7w8GjjiA:1uwz0H:TFVBlzT2XmYfnBqGV30HPM1RzBJjSgAC4UAym49eblQ','2025-09-26 08:19:33.934268'),('phxxtnqgb44ehfvlcb55pqf337sniucv','.eJxVjMsOwiAQRf-FtSEgb5fu-w1kBgapGkhKuzL-uzbpQrf3nHNfLMK21rgNWuKc2YVJq9jpd0VID2o7yndot85Tb-syI98VftDBp57peT3cv4MKo35rIYV0gAC-BI1eo0nWeUFnsDYXpOAIIZRE6IIwWhuXnDYJtCBlirLs_QE_WTii:1uxK9f:LBbB0IbYWBi7EUum_MwPqYnQWhEaVTh8U-IanoD5bi0','2025-09-27 06:54:39.214862'),('piiqsw4s7lmmv337iz5h4rttjp4cl39r','.eJxVjEEOwiAQAP_C2RBYFkGP3n0D2cIiVQNJaU_GvytJD3qdmcxLBNrWErbOS5iTOAtALQ6_dKL44DpUulO9NRlbXZd5kiORu-3y2hI_L3v7NyjUyxgbQPaINllUJ9ZZc9aQwSiflaNsnXGJ-Jh9RGssIERSkKJHC1_uxfsDDs030g:1uxhzx:F0MdLiZT4SX6m_U-z2fXochLjZ9-dto16jpgEiSF2lA','2025-09-28 08:22:13.305525'),('pphkx9vrmlw6n2dqfqqvsvdq8iz9blwq','.eJxVjMsOwiAQRf-FtSG8oS7d-w1kZgCpGkhKuzL-uzbpQrf3nHNfLMK21riNvMQ5sTNTXrLT74pAj9x2lO7Qbp1Tb-syI98VftDBrz3l5-Vw_w4qjPqt3TQpgRRyUCUbrbwwjiTqrA14KzBZ6YBCEATWU7EopdGUdFFkrcTA3h8dHjf8:1uy4KF:wCbe9pVnHN2Pjw4UG0t2VcOiUEyg7Q1sR4F0ZR8oqNQ','2025-09-29 08:12:39.682343'),('pwqd4y23wx24eipep3vo1v6jwn8lqtoz','.eJxVjDsOwyAQBe9CHSEwX6dM7zOghYXgJALJ2FWUuxtLLpx2Zt77Egfbmt3W4uJmJHfCB0ZuV-ohvGM5FL6gPCsNtazL7OmR0NM2OlWMn8fZ_h1kaLmvR6mFHYRRBqQdZTKaWUTjGUaDlmEniSvEBFF4FJ14DUqD1JwrCIr8dhbKOEM:1ux3PV:PPGXDnwsMafV-caF37NWMrsdbO1-nU-tcXw1eMsvfbc','2025-09-26 13:01:53.980349'),('q62j4ssojcum25a0ipu58m04aidoa31y','.eJxVjMsOwiAQRf-FtSFMoTxcuvcbyDBDpWogKe3K-O_apAvd3nPOfYmI21ri1vMSZxZnYcTpd0tIj1x3wHestyap1XWZk9wVedAur43z83K4fwcFe_nWwOBZBaM1-xBURh5JA6NFNzkawChlgsmUrPXstRppYCbwAM74iZV4fwDUtDdu:1uxdUi:2ynolpXStoUEbEul3kIZRE6TFIefUiH7CfNfihURdL0','2025-09-28 03:33:40.659736'),('q9wwn6kwuawbsm6glg1cxz82axkvow52','.eJxVjEsOwjAMBe-SNYrkOB_Kkj1niBzboQXUSk27qrg7VOoCtm9m3mYyrUuf16ZzHsRcDMDZnH7XQvzUcUfyoPE-WZ7GZR6K3RV70GZvk-jrerh_Bz21_lsXjxo7X7rqktcA6COBY1B2JAlLql6rwyqMwaUkHLFowFhJRBg68_4ANQk4-w:1ux1ZC:3KWue0kSxMl4WxgfEeqirdZrFHmnxYwnc9_Lx1XNOgY','2025-09-26 11:03:46.082721'),('qbzlizia7np9tap72idcct0ysznrbnk1','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLMf:6qmWvGogU_BfIIbIGruRd3WX3wFm_zsujO_qMm-2vo8','2025-09-27 08:12:09.789526'),('qh9l4i0cootja7xeys3srpjuxo4rjck9','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyKRh:0LDk9LGsnRozVONvcAHV1ZD4gCCMRUXurVTzwbi0CB0','2025-09-30 01:25:25.011622'),('qlbch45x747u6ljus5k76bs6nqmiqxsd','.eJxVjEsOwjAMBe-SNYrkOB_Kkj1niBzboQXUSk27qrg7VOoCtm9m3mYyrUuf16ZzHsRcDMDZnH7XQvzUcUfyoPE-WZ7GZR6K3RV70GZvk-jrerh_Bz21_lsXjxo7X7rqktcA6COBY1B2JAlLql6rwyqMwaUkHLFowFhJRBg68_4ANQk4-w:1ux1dk:E0xIZGmDL-lh6WAzhT9SMIZA5tm7n9A97Kgmgfb1F7Y','2025-09-26 11:08:28.170437'),('qpmp6o7xiqlw9bn02tyyj7qgzshv583e','.eJxVjDsOwjAQBe_iGlnxrr-U9JwhWu-uSAAlUpxUiLtDpBTQvpl5L9PTtg791nTpRzFn48zpd6vED512IHeabrPleVqXsdpdsQdt9jqLPi-H-3cwUBu-dUxRNbnM1QWqXVJGQVFgAcpYGDCA-oIYCaLDTpgKBUgqOQXvi3l_AOnMN6I:1uwxOF:hyJEFCjvhkbNJCQM0UlmDjyY4RKMT1O0ng8h3RUlyj0','2025-09-26 06:36:11.975583'),('qq7j2l63ku7j4xd4t5gt3m1glow2gv6a','.eJxVjEEOwiAQRe_C2hCwDMO4dN8zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIizgrE6XeNIT1y2xHfQ7vNMs1tXaYod0UetMtx5vy8Hu7fQQ29futMELUzNChKBXVipIiIZAFIMxQ0bJ2xBA40Aiqr8kAmslKOtaYi3h_-5za_:1uxH6c:B4B2Hd6VK5rOiFzFhRJKY0RXrHvEnrE3ZD9hINUUD6s','2025-09-27 03:39:18.057862'),('qsqykyjdwcyri7xq9piyatthzo3cf62b','.eJxVjMsOwiAQRf-FtSEDpS3j0r3fQIZhkKqBpI-V8d-1SRe6veec-1KBtrWEbZE5TEmdlTWoTr9rJH5I3VG6U701za2u8xT1ruiDLvrakjwvh_t3UGgp39qzWOQBe8LEzorP2Y1gAMYUAYxk00dA7wQjWu6J0WcTU4fW09A5UO8PMvA4FQ:1uxGzc:BzJ6KbHe-VnGGdDU0MLy4Gysd9ftZSPnxDxewRWpK_E','2025-09-27 03:32:04.468436'),('quajyncig9sxv0bs9kkxryysawf7tiur','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLU0:h0t3vZbQl0cOCR7bFgXV2H6FiidwbMWVc9OYyOMXuWg','2025-09-27 08:19:44.845519'),('qw4943tx0qq6rb52hupx334hyj6x6qlc','.eJxVjEEOwiAQRe_C2hCBzlBduu8ZCMMMUjU0Ke3KeHfbpAvd_vfef6sQ16WEtckcRlZXZT2o0-9KMT2l7ogfsd4nnaa6zCPpXdEHbXqYWF63w_07KLGVrU4AhEgoKORcdj2CJQuWve1y4ozkjbHS5WyA_YUS9y6dheJmGYasPl89aDj5:1uy4M8:ztSFoyebeWIwPDT-pdHV-TRmgk4BvJw5YtODZfX8MhQ','2025-09-29 08:14:36.514232'),('qykylifuojsrht0z08ldemg2y6d380sw','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLUR:_lTx2zW5xMV2pgrKDeHfARw9zZSKOHOvX3Liln1Eayg','2025-09-27 08:20:11.718010'),('qziwuukzxusk44hga76pyhoxxtw5xrrz','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxGXm:izJ8t_JtE8DqKx5oA4crErnJlEHoYXsUTqiu21rKP6o','2025-09-27 03:03:18.144118'),('rgkvevs6ezcsc0vxr556b3dvlg00kgdh','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLVw:Isreps8JjO2U1fb5CDU1yey_hhexVYf2AXLhprjI7Z4','2025-09-27 08:21:44.168386'),('rp891sgr757qymdlabryilk37us5z8d8','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGXI:Ym7wRzy4Iyd7dz8UsP4ZICM5pcVrXFZyO_N7tXJg8E8','2025-09-27 03:02:48.952477'),('rvd9a1knhnr9x82ooj5kg7vk7vkuq7me','.eJxVjEEOwiAQRe_C2pAMFAou3XsGMjOAVA0kpV013t2QdKHb_977hwi4byXsPa1hieIqALS4_K6E_Ep1oPjE-miSW93WheRQ5Em7vLeY3rfT_Tso2MuoiZ2bNIDznPVkySsD1rBBBks8k1EKVGZtLXJ0joHQsleIs84qJfH5AiVCOI4:1ux3Hk:MJmf8YMPHK9gSuRnlg2S7mp7Rxx-sa4rN1vypxeKFi4','2025-09-26 12:53:52.603199'),('s4ncau0oddbe7ew98mmxare8i6g1wwem','.eJxVjMsOwiAQRf-FtSE8C7h07zeQgRmkaiAp7cr479qkC93ec859sQjbWuM2aIkzsjNTOrDT75ogP6jtCO_Qbp3n3tZlTnxX-EEHv3ak5-Vw_w4qjPqti3JWOyg-UHJqkuTTJDRqshZDJuMlalmMyMUZQCpCJU25CBECZDCOvT84nzjU:1uxhz1:SnHt7NKvkfRsz_KhoWRWYRnyH9OPVAO0Lq9J7zol68A','2025-09-28 08:21:15.161168'),('sgifldw4705kg0xjxltxpzmgep5o3dxy','.eJxVjMsOwiAQRf-FtSE8Bgou3fsNBJhBqgaS0q6M_65NutDtPefcFwtxW2vYBi1hRnZmE7DT75hiflDbCd5ju3Wee1uXOfFd4Qcd_NqRnpfD_TuocdRvLQiUUZRKRqWNFEJ7iQRSWkeKAGWGWCh5b0tRCDY5U7RxRpKnCTWy9wcIwDhA:1uwz0J:a5m2vHUPpV4_3TxQfV0AFosP4fRtegxA6v5oLgNmvU4','2025-09-26 08:19:35.289770'),('sleus6ef65glhibqloykjord2bb55hvf','.eJxVjDsOwyAQBe9CHaHF_EzK9D4DWmAJTiKQjF1FuXtsyUXSvpl5b-ZxW4vfOi1-TuzKhBnZ5XcNGJ9UD5QeWO-Nx1bXZQ78UPhJO59aotftdP8OCvay1zAkbRwIkC7npJyyRC4bbSkIIg1qlKgFQMAdhMFJYWOK5DCTIguSfb4kyTh1:1uxGkU:qi227DTT8CO1tzZnI23-5i3SYQC2v9E5_5iWmAKpabA','2025-09-27 03:16:26.679661'),('sxmmqcvepwl4ry153n1w0rwzylfduzdw','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB5P:tAVQn_Ku44kno5OLhuc6nkCSvJKxkrG3wGDo_2HGip0','2025-09-29 15:25:47.441380'),('sydvyj1kwgiiiym6k6xjqie6a76hzqzl','.eJxVjEsOwjAMBe-SNYrkOB_Kkj1niBzboQXUSk27qrg7VOoCtm9m3mYyrUuf16ZzHsRcDMDZnH7XQvzUcUfyoPE-WZ7GZR6K3RV70GZvk-jrerh_Bz21_lsXjxo7X7rqktcA6COBY1B2JAlLql6rwyqMwaUkHLFowFhJRBg68_4ANQk4-w:1ux1bS:kVOm3ovBFiYyeeo1xxvRAzpsFFEa1bM-jg42pPCshao','2025-09-26 11:06:06.655324'),('szgsafwe2tkhy73qkuwyixgwbrbwslss','.eJxVjDsOwjAYg--SGUXk0aZhZOcM1f8KKaBUatoJcXcaqQPI8uLP9luNsK153Kos48TqooJRp98QgZ5SGuEHlPusaS7rMqFuFX3Qqm8zy-t6dP8OMtTc1lGCjzhY7BM47tDZzhn0YegYDYe0K_acQDwIxUQSrN197tERDUZ9viG8ON0:1uwyt9:57XklEMzAiebMoAVXXCwEDDmicDAERRIXplhLsy66wY','2025-09-26 08:12:11.885532'),('takzgmty75f2wcn4dppjxdrerkke3q4h','.eJxVjDsOwjAQBe_iGln-aL2Gkp4zWPbuggPIluKkQtwdIqWA9s3Me6mU16WmdcicJlYnZS2qw-9aMj2kbYjvud26pt6WeSp6U_ROh750lud5d_8Oah71W4sHRBTxho0FpCCRmLINVyz2iAxiAlN0TgozGw_RgYtkOWIghqDeHzgbOHc:1ux1Dz:aWHKEOHckPWH6aMp9j-GMzBpn8FLFSaecXIZA3hgbRU','2025-09-26 10:41:51.476420'),('tc5sc4qm14vd1qctf3skiawp1l2jafip','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLWI:r5-GfGqprbb87ZAlL-ydgjYeDLxC4ACoeIdtHFIF02k','2025-09-27 08:22:06.756309'),('ti7fcm5xdlpqro590ynljoni09qjtd03','.eJxVjMEOwiAQRP-FsyHIliIevfcbyC4LUjWQlPZk_Hdp0oNmbm_ezFt43NbstxYXP7O4irPS4vRLCcMzlr3iB5Z7laGWdZlJ7oo82ianyvF1O9y_g4wt9zVZ7ZgQDCTSl1FbHIy1BAMopB6E4JhBuWAcoknGQeIOiFVAS6P4fAE8LjlC:1ux4oF:kqJmvX7ReGGsCjuR94PcmsE3djnKjWq1__33S3rL2WE','2025-09-26 14:31:31.097139'),('ttrd2y1et6zulzm4ltvn3mc5ns97676n','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1ux1HI:_7AgxvM78FOwt1a2M4Pj5KrGv90hVIcrIgmuBBPU2YQ','2025-09-26 10:45:16.277362'),('tyi1d7ltjcxz26kr062ws84ms9urbvzx','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLEq:lNQYiV4EngYTl8EkoGPWvUJntFy27Q0kKFB6UJAackk','2025-09-27 08:04:04.456946'),('u6aiaqfb02kygawxci0jxvp1jvb8buiz','.eJxVjDsOwjAQBe_iGlmOE39CSZ8zWOvdDQ4gW4qTCnF3HCkFtDPz3lsE2LcU9sprWEhchevF5RdGwCfnw9AD8r1ILHlblyiPRJ62yqkQv25n-3eQoKa29sZRP8JASptRs4POD6gcxU4BEbN1pnmlGLUl9MawbWy2_Uzeo1fi8wUERTgf:1uwyvf:ZsLtr437z7h6o90yp2fnbDEryljIYHeIrYX13a1eWHA','2025-09-26 08:14:47.800892'),('u9vzmqjqzj7x0614euy0pjgud12dw1i3','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxGXm:izJ8t_JtE8DqKx5oA4crErnJlEHoYXsUTqiu21rKP6o','2025-09-27 03:03:18.084306'),('ulj2wb7nurreto8uko8tbqn8irlvmonm','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLR8:dZA-Pfksc5w3BtuVcJlqOIRVUhvQixJ4kfSNOtLNg4I','2025-09-27 08:16:46.671503'),('urfwf4jdtgufr4cti2zgkn8fdnbswqn1','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxKBP:IzK06kLIaRdqXT1hXeKlUl9mgL3h_Oqza_1r5I7Y0pw','2025-09-27 06:56:27.604405'),('utqxxzkxmzhihq17qo4gmwobc8t0zu1z','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKeu:mZqIwxeayZFLEfOYSyPYzEqSaaBR1kFj6AUKI3a_gk0','2025-09-30 01:39:04.455400'),('uwejyqhe1ert9oqlxpcmfrtdz0wn2uf0','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLUU:O0guxML-RcGgzxkb3t9FP41Rx1eMok_eC0odSqX8b18','2025-09-27 08:20:14.293555'),('v1k19nrd244dfeqncza15hb1sygrzemt','.eJxVjMsOwiAQRf-FtSHyGKAu3fsNZKYMUjWQlHZl_HfbpAvd3nPOfYuI61Li2nmOUxIXocTpdyMcn1x3kB5Y702OrS7zRHJX5EG7vLXEr-vh_h0U7GWrnWVgQoCs0J-VQastJB0cggtBG68hM1kiYz2B0jl5DAPmwQG6LRafL9CfN3o:1uwuzz:P3FhpNNOMYyzZ4WKyfuClI75BsT-4Y_F_PV1ulvFC30','2025-09-26 04:02:59.242336'),('v3ziu9rags21szp52k0a81p2hikbm90f','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyB5b:ZO7IM0-PMOLBwevy5Xf032eNdbhZi8-smSj1dzRYLBE','2025-09-29 15:25:59.250184'),('v5982eoii189hmquztgam9hlb2db3opz','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLVE:_rXTm_3KcwiQ21-PpP1tEWvvQKdF8aDJwE1bsSGJMmo','2025-09-27 08:21:00.021713'),('vdj0mrduqsb5twhuy9komlozy6rlfifz','.eJxVjDEOwjAMRe-SGUV2GsUNIztnqOw4pQWUSE07Ie4OlTrA-t97_2UG3tZp2FpehlnN2WBw5vS7CqdHLjvSO5dbtamWdZnF7oo9aLPXqvl5Ody_g4nb9K2dc5E8etd7CRhpBEJCYAActcMsRLEH7RnYJ4xdEMrd6ALmBKog5v0B54Q3MQ:1uxK9C:xeggh9ajnr_yDflD9onVTqqKcg5X4oeDyw5dLugJvGM','2025-09-27 06:54:10.242978'),('vide84pgd1360fbigl3yqp2t9x1zvkg5','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLAl:Gq_ZAgP0X_MpfnD0R37J3uQndxHMk-sLz3FlBEDBipk','2025-09-27 07:59:51.428999'),('vspyp2ts9oz13ssb2c7aazi6ygtq1qca','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyBvg:yHB4TdaqJ3Q5rZuD2SxtbWMymywhuXQE_ibe38gfBuE','2025-09-29 16:19:48.458491'),('w5ab4i19894ef48ckmgqnevx5uyw4ve9','.eJxVjMEOwiAQRP-FsyHIliIevfcbyC4LUjWQlPZk_Hdp0oNmbm_ezFt43NbstxYXP7O4irPS4vRLCcMzlr3iB5Z7laGWdZlJ7oo82ianyvF1O9y_g4wt9zVZ7ZgQDCTSl1FbHIy1BAMopB6E4JhBuWAcoknGQeIOiFVAS6P4fAE8LjlC:1ux4pp:RYhkrw0fZkEvoqrLaa96GqS7X_64QZzmTO254GyuJWA','2025-09-26 14:33:09.458849'),('w626j98bzr45h5lyzi48vn7qtbpa4o3p','.eJxVjDEOwjAMRe-SGUWNlaYOIztniOzEJgXUSk07Ie4OlTrA-t97_2USbWtNW5MljcWcjXO9Of2uTPkh047KnabbbPM8rcvIdlfsQZu9zkWel8P9O6jU6rdG1kAeYlF2JL2DMDgmhhxClE7UB4c5YASPqhzVgwLEOHQihIRo3h896TiG:1ux1CB:SACnU8sMU910K0B7wIIgtPoP7ejsQiZ1_yNtF5QT6Xk','2025-09-26 10:39:59.954669'),('whapr25ovu8w4i953nglw1ts7qsvk9th','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLAN:z6e3To--CRpLCRxIR3p8ACqgNJduavxoxk2flr1VM2E','2025-09-27 07:59:27.911418'),('wop6adlyrv02z7bf7cvo1ohgjpkb6cyf','.eJxVjDsOwjAQBe_iGlnZ9Z-SnjNY66yNA8iR4qRC3B0ipYD2zcx7iUjbWuPW8xInFmeBzonT75pofOS2I75Tu81ynNu6TEnuijxol9eZ8_NyuH8HlXr91jZB1kYrBK3JBwhBMwzOEnplgQcPBVVhn53BpMBD4lQsZnLkMAQj3h_5yjcl:1uy4Mj:-m5wpEd6fvEhIY-N5G_HqXONw1vVJODEKa9p6E0TA00','2025-09-29 08:15:13.391741'),('wvocajxfxqvtzf482lvgr239zjwbgcb8','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxKBj:bfJ3E_6lFlHJese0gSaOGNRTBuCPyRn-bFuzKUIsrlY','2025-09-27 06:56:47.689202'),('wvvg9or4rbzjv8j0a2r1r22q490b1939','.eJxVjEEOwiAQRe_C2pAMFAou3XsGMjOAVA0kpV013t2QdKHb_977hwi4byXsPa1hieIqALS4_K6E_Ep1oPjE-miSW93WheRQ5Em7vLeY3rfT_Tso2MuoiZ2bNIDznPVkySsD1rBBBks8k1EKVGZtLXJ0joHQsleIs84qJfH5AiVCOI4:1ux3Hk:MJmf8YMPHK9gSuRnlg2S7mp7Rxx-sa4rN1vypxeKFi4','2025-09-26 12:53:52.547470'),('wz7l5sj1s6sxes9brjio1myf2u9xn1oo','.eJxVjMsOwiAQRf-FtSHDq4BL934DGWCQqoGktCvjv2uTLnR7zzn3xQJuaw3boCXMmZ2ZEJqdfteI6UFtR_mO7dZ56m1d5sh3hR908GvP9Lwc7t9BxVG_NRRKJglUegIAka1TTnuM1nsgkCpqCZSdNWiKVtkWJW2hqKMRaQKy7P0BFYs3zA:1ux1AA:xYLtqmle-gGgLmk6W0z8aJtjS6p2eMnfZBiv39qOOiQ','2025-09-26 10:37:54.089667'),('x04giq2pc8bxh3hdzfc14bxqr9x07n3c','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLBE:9raIaMJ58I0fKUrMoFK1qGk40IDeMzXSuZKuFLso5MU','2025-09-27 08:00:20.843906'),('x2k7g9lh85n6wixfsyw5beog970c09pf','.eJxVjMEOwiAQRP-FsyHIliIevfcbyC4LUjWQlPZk_Hdp0oNmbm_ezFt43NbstxYXP7O4irPS4vRLCcMzlr3iB5Z7laGWdZlJ7oo82ianyvF1O9y_g4wt9zVZ7ZgQDCTSl1FbHIy1BAMopB6E4JhBuWAcoknGQeIOiFVAS6P4fAE8LjlC:1ux4l3:Jjs6VxsNxYyDPQHA-5ZAADHP1aVasWjwx-HM1j31MMY','2025-09-26 14:28:13.186518'),('x7e33mt1hw27fk0tgkcfmqkbftt17btj','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLUt:2PszjbcGBvUwImxzyZZL498UHwq4Ky4clO2bXTLPtXE','2025-09-27 08:20:39.753352'),('xb3ljnx6d94ws72s9iypmp0npav489am','.eJxVjE0OwiAYBe_C2hB-Ah-4dO8ZCDxQqgaS0q6Md7dNutDtm5n3ZiGuSw3rKHOYMjszaSU7_a4p4lnajvIjtnvn6G2Zp8R3hR908GvP5XU53L-DGkfd6uSEla7AeShACA0rYJQuMMkZZJNAWntsmouCbiQjJBmfMjkSpNjnCynDN9s:1uxGXI:Ym7wRzy4Iyd7dz8UsP4ZICM5pcVrXFZyO_N7tXJg8E8','2025-09-27 03:02:48.896591'),('xbg4s3rvghkqii45cn9pghojph8om2cb','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyBuL:bVd0cv3TkLsAlZRbSgHWj7fxFAL9D4xtrVAJLKZ1uBs','2025-09-29 16:18:25.263992'),('xbw7m3s02eyb9n8jbbiba4qmvi0auig2','.eJxVjDsOwjAQRO_iGln22lk7lPQ5Q7TrtXEAJVI-FeLuJFIK6Ebz3sxb9bSttd-WPPeDqKsCa9Tlt2VKzzweSB403iedpnGdB9aHok-66G6S_Lqd7t9BpaXua2b0TXAA5JDYoiXBlDEIlMKC6MlxMmlPxZoIJhK2EKUJxvvWglOfLzACN8M:1uxGxA:B4dWXnosBZ38kbzYuEXn75r0iQZImEjxm_BKdfRHsOs','2025-09-27 03:29:32.356318'),('xds63ug61zh6q90wm17jyjp6e2qzd0ib','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLMd:aCG8-hHJLJn0I2kXfnlF6im5TiapIyvuueBni3_641g','2025-09-27 08:12:07.158727'),('xrd7msvxnsby8pznyr10ast3k50z63kh','.eJxVjDkOwjAQRe_iGlme2OOFkp4zWDNecAA5UpYKcXeIlALa_977LxFpW1vcljLHMYuzGMCL0-_KlB6l7yjfqd8mmaa-ziPLXZEHXeR1yuV5Ody_g0ZL-9ZoXNbsKiNrC8YmVo58CkyYwbtQPJfEoHJVhFiVV2owNQACIAWrxfsDNwE4Ag:1uxGz7:jB-fdgRWnLimvgyu7E8jRhCLi3ZEhS9mEacahU4hGMw','2025-09-27 03:31:33.762407'),('xs3oj4fk9v123803lejea9d0zsh4vku3','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKpT:5CBT7CPO7pNjyvYF4Mcr7hTx928xvzXILnuaAiakq3Q','2025-09-30 01:49:59.406258'),('y41ff0aw4du0l8rr6vphhpxxc0hc60bb','.eJxVjEEOwiAQRe_C2hCgAoNL9z0DGWZQqgaS0q6Md7dNutDte-__t4i4LiWuPc9xYnERxmhx-qUJ6ZnrrviB9d4ktbrMU5J7Ig_b5dg4v65H-3dQsJdtjTdDXjsXNFnmrDSCUZoB0xlygrAx53TwTNmSU4NXfkBIHAgMqWDF5ws5ijhu:1uxH0c:haLr5zgkaMf3j1Q8FMPmHVsqsIV8-eVXdXdG0t6x7as','2025-09-27 03:33:06.322209'),('yblmscee4l6n29f89hj183k0ey4hbsbh','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLVG:t6NN1FUfIZzj8asngqH5PFiK45craVuAQrUEs08mu3k','2025-09-27 08:21:02.673510'),('yoq68myxgndjivemb5txzqq5xhwyp70t','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxGWh:NxRGfDgF7FOVV7dB6irwFDRK2TZ0RefL87tC3tyqI8c','2025-09-27 03:02:11.235185'),('yqguvvmgrryb5p8c03jqenhr9yz1rlv5','.eJxVjEEOwiAQRe_C2hCwDMO4dN8zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIizgrE6XeNIT1y2xHfQ7vNMs1tXaYod0UetMtx5vy8Hu7fQQ29futMELUzNChKBXVipIiIZAFIMxQ0bJ2xBA40Aiqr8kAmslKOtaYi3h_-5za_:1uxH5P:bRmuGMAZCUN6igorKUusZueK2bMPTushc1k4xcP4xY4','2025-09-27 03:38:03.260961'),('yw445bahcwul75kze8zmwg0tzrim40s0','.eJxVjEEOwiAQRe_C2hAonYG6dO8ZyMAMtmpKUtqV8e7apAvd_vfef6lI2zrGrckSJ1ZnZRHV6XdNlB8y74jvNN-qznVelynpXdEHbfpaWZ6Xw_07GKmN37oYGrAYKbkTSWxMwI5dGERcAfAJApAJkLL4HtFZwRJ6aziQG8Bzp94fSBI4UQ:1uxLIV:x1DoLUtjUpKJ2k4sq_OWur_NPR25tjci-e-AKscJx7s','2025-09-27 08:07:51.017437'),('z82uqr8hw18mmvekiy1muse3l39g7m3v','.eJxVjEEOwiAQRe_C2hCKMFSX7nuGZpgZpGogKe3KeHfbpAvd_vfef6sR1yWPa5N5nFhdlVOn3y0iPaXsgB9Y7lVTLcs8Rb0r-qBND5XldTvcv4OMLW-1F58sk00QnEgyEG0iSucYMUBvSIwnBDLS2U30zBffWQeBSQCD6dXnCxTsOMA:1uyKuo:MmbyRblahFsR75P0LntRhLn2v9PtnCpAmayxfzHgHVA','2025-09-30 01:55:30.944008'),('zcz70y9yd0qvhnjp18vxmx9qdlg8fxzv','.eJxVjDsOwjAQBe_iGllZ_01JnzNYa6-NA8iR4qRC3J1ESgHtzLz3ZgG3tYat5yVMxK5MGGCXXxoxPXM7FD2w3Wee5rYuU-RHwk_b-ThTft3O9u-gYq_72njQ5H1KfgChHWHRIhpLpB1Kq5IsUJQ2BohQuQIgs9wB2DJ4hcmzzxcfuTfs:1uy47W:iBG7uL-FBBQJdXoP802GGTrfoR-2gdQHF1PBdLJv6Ps','2025-09-29 07:59:30.114336'),('zd6agvv0ek5b1ksnlukagmiwjrnth2yo','.eJxVjDsOwjAQBe_iGlle_2JT0nMGy97d4ABypDipEHeHSCmgfTPzXiLlba1p67ykicRZWHH63UrGB7cd0D232yxxbusyFbkr8qBdXmfi5-Vw_w5q7vVbAwLGwiaCcTYrjForO5LzqC2PBgJBMQFoMBoZMiEaT-yV5gDOhUG8P9rIN5M:1uxdGb:oDclqC4AZWLlxv0qxgL41qYzmC3ekM0IFlC5UaqNCiA','2025-09-28 03:19:05.539741'),('zkwz3ugt8sys28wbavza48kr62iwr58z','.eJxVjEEOwiAQRe_C2hBnWgZw6b5nIMNAbdVAUtqV8e7apAvd_vfef6nA2zqFreUlzEldFIBXp981sjxy2VG6c7lVLbWsyxz1ruiDNj3UlJ_Xw_07mLhN35qs7b0Hg75jFCGSJKMRoD45cS6KiQ7p3AlyD4Bk4ogE3jKioB2den8AFNU3hA:1uyBtw:7ZPALB6bwsrvgIwPCBCEccS6Ql-_vj1rdvysq4WhUu8','2025-09-29 16:18:00.908940'),('zq7a1mp03fbpuk0nayel6zmmj1atalmx','.eJxVjEEOwiAQRe_C2pBS2gFcuvcMZGYYpGpoUtqV8e7apAvd_vfef6mI21ri1mSJU1JnZWBQp9-VkB9Sd5TuWG-z5rmuy0R6V_RBm77OSZ6Xw_07KNjKt-7ZJODOoPHcAQIRjGh9cEkoi6MQUFK24t2YyQ3ZZC_Weg8C3AcW9f4ATck5Rw:1uxLIX:fBMzVMetk6Dj5r6JnbZtGyD5mTbfTgp04miUI0AbWZM','2025-09-27 08:07:53.659386'),('zwhapywlgvdzz4qzcqg6g40b0euyx6l1','.eJxVjEsOwjAMBe-SNYrkOB_Kkj1niBzboQXUSk27qrg7VOoCtm9m3mYyrUuf16ZzHsRcDMDZnH7XQvzUcUfyoPE-WZ7GZR6K3RV70GZvk-jrerh_Bz21_lsXjxo7X7rqktcA6COBY1B2JAlLql6rwyqMwaUkHLFowFhJRBg68_4ANQk4-w:1ux1cn:Av2rg-Yj1TIyzPaKoiBJoNpq3ioOGqslD1520oP2_yc','2025-09-26 11:07:29.992672');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `message_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `data` json DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `read_at` datetime(6) DEFAULT NULL,
  `recipient_id` bigint NOT NULL,
  `sender_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_sender_id_57e62d28_fk_accounts_user_id` (`sender_id`),
  KEY `notificatio_recipie_583549_idx` (`recipient_id`,`is_read`),
  KEY `notificatio_message_db1a1b_idx` (`message_type`),
  KEY `notificatio_created_e4c995_idx` (`created_at`),
  CONSTRAINT `notifications_recipient_id_e1133bac_fk_accounts_user_id` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `notifications_sender_id_57e62d28_fk_accounts_user_id` FOREIGN KEY (`sender_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (7,'师生关系申请','学员 hhm 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"relation_id\": 18}','2025-09-12 14:28:13.307606',NULL,102,NULL),(8,'申请审核结果','教练 coach3 已同意您的申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 16}','2025-09-12 14:28:13.466677',NULL,120,NULL),(13,'师生关系审核结果','教练 test_coach 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 20}','2025-09-13 01:56:13.721385',NULL,167,NULL),(14,'师生关系审核结果','教练 coach1 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 38}','2025-09-13 03:06:47.310994',NULL,167,NULL),(15,'师生关系审核结果','教练 coach2 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 37}','2025-09-13 03:07:18.509439',NULL,167,NULL),(17,'师生关系审核结果','教练 coach08 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 39}','2025-09-13 03:13:21.192209',NULL,96,NULL),(18,'新的学员申请','学员 王五 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 168, \"relation_id\": 40, \"student_name\": \"王五\"}','2025-09-13 03:16:34.272069',NULL,178,NULL),(19,'新的学员申请','学员 王五 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 168, \"relation_id\": 41, \"student_name\": \"王五\"}','2025-09-13 03:16:36.536142',NULL,177,NULL),(20,'新的学员申请','学员 王五 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 168, \"relation_id\": 42, \"student_name\": \"王五\"}','2025-09-13 03:16:39.351559',NULL,176,NULL),(21,'新的学员申请','学员 王学员 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 96, \"relation_id\": 43, \"student_name\": \"王学员\"}','2025-09-13 03:20:11.767677',NULL,102,NULL),(22,'师生关系审核结果','教练 coach08 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 43}','2025-09-13 03:20:11.871148',NULL,96,NULL),(26,'师生关系审核结果','教练 test_coach_simple 已同意您的师生关系申请','system',1,'{\"type\": \"relation_approved\", \"relation_id\": 45}','2025-09-13 03:26:21.967146','2025-09-14 07:12:29.101362',4,NULL),(27,'新的学员申请','学员 赵六 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 169, \"relation_id\": 46, \"student_name\": \"赵六\"}','2025-09-13 03:26:58.796744',NULL,178,NULL),(28,'新的学员申请','学员 赵六 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 169, \"relation_id\": 47, \"student_name\": \"赵六\"}','2025-09-13 03:27:01.471435',NULL,176,NULL),(33,'新的学员申请','学员 赵六 申请选择您为教练','system',0,'{\"type\": \"relation_request\", \"student_id\": 169, \"relation_id\": 52, \"student_name\": \"赵六\"}','2025-09-13 06:53:46.748070',NULL,177,NULL),(34,'新的学员申请','学员 赵六 申请选择您为教练','system',1,'{\"type\": \"relation_request\", \"student_id\": 169, \"relation_id\": 53, \"student_name\": \"赵六\"}','2025-09-13 06:53:51.135840','2025-09-13 06:54:43.164185',163,NULL),(35,'师生关系审核结果','教练 coach3 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 53}','2025-09-13 06:54:58.593967',NULL,169,NULL),(36,'师生关系审核结果','教练 coach3 已同意您的师生关系申请','system',0,'{\"type\": \"relation_approved\", \"relation_id\": 36}','2025-09-13 06:55:00.705254',NULL,167,NULL),(59,'预约取消申请','学员 hhm 申请取消预约，请您确认','booking',0,'{\"type\": \"cancellation_request\", \"reason\": \"123\", \"booking_id\": 21, \"cancellation_id\": 7}','2025-09-14 03:04:54.439169',NULL,163,4),(60,'预约取消申请','学员 hhm 申请取消预约，请您确认','booking',0,'{\"type\": \"cancellation_request\", \"reason\": \"123\", \"booking_id\": 38, \"cancellation_id\": 8}','2025-09-14 03:08:15.991780',NULL,163,4),(61,'上课提醒','您预约的课程将在一小时后开始。教练：王教练，球台：球台4号，时间：2025-09-14 04:36','booking',1,'{\"type\": \"class_reminder\", \"booking_id\": 21, \"coach_name\": \"王教练\", \"start_time\": \"2025-09-14T04:36:40.248615+00:00\", \"table_name\": \"球台4号\"}','2025-09-14 03:35:15.368853','2025-09-14 07:12:28.547316',4,NULL),(62,'上课提醒','您的课程将在一小时后开始。学员：huang，球台：球台4号，时间：2025-09-14 04:36','booking',0,'{\"type\": \"class_reminder\", \"booking_id\": 21, \"start_time\": \"2025-09-14T04:36:40.248615+00:00\", \"table_name\": \"球台4号\", \"student_name\": \"huang\"}','2025-09-14 03:35:15.453589',NULL,163,NULL);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_account_transaction`
--

DROP TABLE IF EXISTS `payments_account_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_account_transaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transaction_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `balance_before` decimal(10,2) NOT NULL,
  `balance_after` decimal(10,2) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `account_id` bigint NOT NULL,
  `payment_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_account_tra_account_id_7e260f55_fk_payments_` (`account_id`),
  KEY `payments_account_tra_payment_id_6d152d41_fk_payments_` (`payment_id`),
  CONSTRAINT `payments_account_tra_account_id_7e260f55_fk_payments_` FOREIGN KEY (`account_id`) REFERENCES `payments_user_account` (`id`),
  CONSTRAINT `payments_account_tra_payment_id_6d152d41_fk_payments_` FOREIGN KEY (`payment_id`) REFERENCES `payments_payment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_account_transaction`
--

LOCK TABLES `payments_account_transaction` WRITE;
/*!40000 ALTER TABLE `payments_account_transaction` DISABLE KEYS */;
INSERT INTO `payments_account_transaction` VALUES (3,'recharge',500.00,0.00,500.00,'管理员线下充值录入: 前端测试 - 线下现金支付课程费用','2025-09-14 07:59:40.765854',9,3),(4,'recharge',500.00,500.00,1000.00,'管理员线下充值录入: 前端测试 - 线下现金支付课程费用','2025-09-14 08:00:09.066191',9,4),(5,'recharge',500.00,0.00,500.00,'管理员线下充值录入: 测试线下支付录入 - 课程费用','2025-09-14 08:06:25.578468',10,5),(6,'recharge',200.00,0.00,200.00,'管理员审核通过充值: 测试充值审核功能','2025-09-14 08:16:37.913308',2,11),(9,'recharge',12.00,0.00,12.00,'管理员审核通过充值: ','2025-09-14 08:32:02.709718',11,10),(10,'recharge',12.00,12.00,24.00,'管理员审核通过充值: ','2025-09-14 08:32:04.664575',11,9),(11,'recharge',50.00,200.00,250.00,'管理员审核通过充值: 微信充值测试','2025-09-14 08:32:05.998236',2,8),(12,'recharge',100.00,250.00,350.00,'管理员审核通过充值: 测试充值','2025-09-14 08:32:07.370974',2,7),(13,'recharge',12.00,350.00,362.00,'管理员审核通过充值: ','2025-09-14 08:32:08.534090',2,6);
/*!40000 ALTER TABLE `payments_account_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_invoice`
--

DROP TABLE IF EXISTS `payments_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `invoice_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tax_number` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `issued_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `payment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `payments_invoice_payment_id_1394aa6e_fk_payments_payment_id` (`payment_id`),
  CONSTRAINT `payments_invoice_payment_id_1394aa6e_fk_payments_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payments_payment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_invoice`
--

LOCK TABLES `payments_invoice` WRITE;
/*!40000 ALTER TABLE `payments_invoice` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_method`
--

DROP TABLE IF EXISTS `payments_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_method` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `method_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_method`
--

LOCK TABLES `payments_method` WRITE;
/*!40000 ALTER TABLE `payments_method` DISABLE KEYS */;
INSERT INTO `payments_method` VALUES (1,'现金支付','cash',1,'线下现金支付','2025-09-14 07:47:57.592449'),(2,'微信支付','wechat',1,NULL,'2025-09-14 08:09:24.038473'),(3,'支付宝','alipay',1,NULL,'2025-09-14 08:09:24.115249'),(4,'银行转账','bank_transfer',1,NULL,'2025-09-14 08:37:34.727245');
/*!40000 ALTER TABLE `payments_method` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_payment`
--

DROP TABLE IF EXISTS `payments_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `transaction_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `paid_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `enrollment_id` bigint DEFAULT NULL,
  `payment_method_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_id` (`payment_id`),
  KEY `payments_payment_payment_method_id_c909ff25_fk_payments_` (`payment_method_id`),
  KEY `payments_payment_user_id_f9db060a_fk_accounts_user_id` (`user_id`),
  KEY `payments_payment_enrollment_id_70d4c444_fk_courses_enrollment_id` (`enrollment_id`),
  CONSTRAINT `payments_payment_enrollment_id_70d4c444_fk_courses_enrollment_id` FOREIGN KEY (`enrollment_id`) REFERENCES `courses_enrollment` (`id`),
  CONSTRAINT `payments_payment_payment_method_id_c909ff25_fk_payments_` FOREIGN KEY (`payment_method_id`) REFERENCES `payments_method` (`id`),
  CONSTRAINT `payments_payment_user_id_f9db060a_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_payment`
--

LOCK TABLES `payments_payment` WRITE;
/*!40000 ALTER TABLE `payments_payment` DISABLE KEYS */;
INSERT INTO `payments_payment` VALUES (3,'PAY2025091421D8537C','course_fee',500.00,'completed',NULL,'管理员线下录入: 前端测试 - 线下现金支付课程费用','2025-09-14 07:59:40.738498','2025-09-14 07:59:40.738498','2025-09-14 07:59:40.738498',NULL,1,114),(4,'PAY2025091400C420DB','course_fee',500.00,'completed',NULL,'管理员线下录入: 前端测试 - 线下现金支付课程费用','2025-09-14 08:00:09.065073','2025-09-14 08:00:09.065073','2025-09-14 08:00:09.065073',NULL,1,114),(5,'PAY20250914D8AD98FB','course_fee',500.00,'completed',NULL,'管理员线下录入: 测试线下支付录入 - 课程费用','2025-09-14 08:06:25.576473','2025-09-14 08:06:25.576473','2025-09-14 08:06:25.576473',NULL,1,195),(6,'PAY20250914A66F07A0','recharge',12.00,'completed',NULL,'','2025-09-14 08:32:08.532288','2025-09-14 08:09:19.861872','2025-09-14 08:32:08.532288',NULL,1,4),(7,'PAY202509143FCEC6DE','recharge',100.00,'completed',NULL,'测试充值','2025-09-14 08:32:07.368977','2025-09-14 08:10:20.781524','2025-09-14 08:32:07.368977',NULL,1,4),(8,'PAY20250914D1388E5A','recharge',50.00,'completed',NULL,'微信充值测试','2025-09-14 08:32:05.995244','2025-09-14 08:10:20.849848','2025-09-14 08:32:05.995244',NULL,2,4),(9,'PAY2025091418DB8A03','recharge',12.00,'completed',NULL,'','2025-09-14 08:32:04.661572','2025-09-14 08:14:43.017437','2025-09-14 08:32:04.661572',NULL,2,167),(10,'PAY20250914A359AEF8','recharge',12.00,'completed',NULL,'','2025-09-14 08:32:02.707560','2025-09-14 08:14:48.542047','2025-09-14 08:32:02.707560',NULL,1,167),(11,'PAY20250914F0859F5F','recharge',200.00,'completed',NULL,'测试充值审核功能','2025-09-14 08:16:37.910299','2025-09-14 08:16:36.649124','2025-09-14 08:16:37.910299',NULL,2,4),(12,'PAY2025091491446F83','recharge',100.00,'failed',NULL,'测试拒绝充值','2025-09-14 08:16:38.162318','2025-09-14 08:16:38.106271','2025-09-14 08:16:38.162318',NULL,1,4),(18,'PAY20250914C1BD915E','recharge',50.00,'pending',NULL,'用户充值 ¥50.00 - 等待管理员审核',NULL,'2025-09-14 08:38:07.500670','2025-09-14 08:38:07.500670',NULL,4,251),(19,'PAY20250914BA5E99FA','recharge',100.00,'failed',NULL,'用户充值 ¥100.00 - 等待管理员审核','2025-09-14 09:40:16.371921','2025-09-14 08:38:07.572101','2025-09-14 09:40:16.372918',NULL,4,251),(20,'PAY20250914CCAADCF8','course_fee',200.00,'pending',NULL,'用户充值 ¥200.00 - 等待管理员审核',NULL,'2025-09-14 08:38:07.613738','2025-09-14 08:44:59.183386',NULL,4,251),(25,'PAY202509153A9D3C1E','recharge',123.00,'pending',NULL,'123',NULL,'2025-09-15 16:34:20.970416','2025-09-15 16:34:20.970416',NULL,1,4);
/*!40000 ALTER TABLE `payments_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_refund`
--

DROP TABLE IF EXISTS `payments_refund`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_refund` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `refund_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `reason` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `approved_at` datetime(6) DEFAULT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `payment_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `refund_id` (`refund_id`),
  KEY `payments_refund_approved_by_id_bcd22cd9_fk_accounts_user_id` (`approved_by_id`),
  KEY `payments_refund_payment_id_a70693f7_fk_payments_payment_id` (`payment_id`),
  CONSTRAINT `payments_refund_approved_by_id_bcd22cd9_fk_accounts_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `payments_refund_payment_id_a70693f7_fk_payments_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payments_payment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_refund`
--

LOCK TABLES `payments_refund` WRITE;
/*!40000 ALTER TABLE `payments_refund` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments_refund` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments_user_account`
--

DROP TABLE IF EXISTS `payments_user_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments_user_account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `balance` decimal(10,2) NOT NULL,
  `frozen_amount` decimal(10,2) NOT NULL,
  `total_paid` decimal(10,2) NOT NULL,
  `total_refunded` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `payments_user_account_user_id_51bcf68c_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments_user_account`
--

LOCK TABLES `payments_user_account` WRITE;
/*!40000 ALTER TABLE `payments_user_account` DISABLE KEYS */;
INSERT INTO `payments_user_account` VALUES (2,362.00,0.00,362.00,0.00,'2025-09-12 07:19:44.347524','2025-09-14 08:32:08.535105',4),(4,0.00,0.00,0.00,0.00,'2025-09-12 13:02:07.317476','2025-09-12 13:02:07.317476',120),(6,0.00,0.00,0.00,0.00,'2025-09-13 13:53:54.375386','2025-09-13 13:53:54.375386',163),(9,1000.00,0.00,1000.00,0.00,'2025-09-14 07:59:40.764856','2025-09-14 08:00:09.066191',114),(10,500.00,0.00,500.00,0.00,'2025-09-14 08:06:25.577470','2025-09-14 08:06:25.578468',195),(11,24.00,0.00,24.00,0.00,'2025-09-14 08:14:38.913785','2025-09-14 08:32:04.664575',167),(18,0.00,0.00,0.00,0.00,'2025-09-14 08:31:36.169188','2025-09-14 08:31:36.169188',119),(21,0.00,0.00,0.00,0.00,'2025-09-14 08:38:07.659226','2025-09-14 08:38:07.659226',251),(28,500.00,0.00,0.00,0.00,'2025-09-15 08:11:56.881805','2025-09-15 08:11:56.912750',269),(29,500.00,0.00,0.00,0.00,'2025-09-15 08:12:38.737545','2025-09-15 08:12:38.839959',271),(30,500.00,0.00,0.00,0.00,'2025-09-15 08:13:17.707915','2025-09-15 08:13:17.772441',273),(31,500.00,0.00,0.00,0.00,'2025-09-15 08:14:34.603050','2025-09-15 08:14:34.656106',275),(32,500.00,0.00,0.00,0.00,'2025-09-15 08:15:12.537377','2025-09-15 08:15:12.590655',277);
/*!40000 ALTER TABLE `payments_user_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations_booking`
--

DROP TABLE IF EXISTS `reservations_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations_booking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `duration_hours` decimal(3,1) NOT NULL,
  `total_fee` decimal(10,2) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `confirmed_at` datetime(6) DEFAULT NULL,
  `cancelled_at` datetime(6) DEFAULT NULL,
  `cancel_reason` longtext COLLATE utf8mb4_unicode_ci,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `cancelled_by_id` bigint DEFAULT NULL,
  `relation_id` bigint NOT NULL,
  `table_id` bigint NOT NULL,
  `payment_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reservations_booking_relation_id_e05eebe4_fk_reservati` (`relation_id`),
  KEY `reservations_booking_table_id_fd67f4c3_fk_reservations_table_id` (`table_id`),
  KEY `reservations_booking_cancelled_by_id_9308c64c_fk_accounts_` (`cancelled_by_id`),
  CONSTRAINT `reservations_booking_cancelled_by_id_9308c64c_fk_accounts_` FOREIGN KEY (`cancelled_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_booking_relation_id_e05eebe4_fk_reservati` FOREIGN KEY (`relation_id`) REFERENCES `reservations_coach_student_relation` (`id`),
  CONSTRAINT `reservations_booking_table_id_fd67f4c3_fk_reservations_table_id` FOREIGN KEY (`table_id`) REFERENCES `reservations_table` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations_booking`
--

LOCK TABLES `reservations_booking` WRITE;
/*!40000 ALTER TABLE `reservations_booking` DISABLE KEYS */;
INSERT INTO `reservations_booking` VALUES (21,'2025-09-14 04:36:40.248615','2025-09-14 05:36:40.248615',1.0,100.00,'confirmed',NULL,NULL,NULL,'','2025-09-13 08:27:56.493591','2025-09-14 03:35:03.752784',NULL,17,4,'unpaid'),(22,'2025-09-13 05:54:00.000000','2025-09-13 06:54:00.000000',1.0,100.00,'confirmed',NULL,NULL,NULL,'测试预约1','2025-09-13 14:03:30.346391','2025-09-13 14:03:30.346391',NULL,18,8,'unpaid'),(24,'2025-09-14 17:00:00.000000','2025-09-14 18:00:00.000000',1.0,100.00,'confirmed',NULL,NULL,NULL,'王教练的课程 - 2025-09-13 9:00','2025-09-13 14:17:21.263466','2025-09-13 14:27:58.493262',NULL,55,8,'unpaid'),(25,'2025-09-13 22:00:00.000000','2025-09-13 23:00:00.000000',1.0,100.00,'completed',NULL,NULL,NULL,'王教练的课程 - 2025-09-13 14:00','2025-09-13 14:17:21.306888','2025-09-14 02:22:45.845097',NULL,56,9,'unpaid'),(26,'2025-09-20 00:00:00.000000','2025-09-20 01:00:00.000000',1.0,100.00,'cancelled',NULL,'2025-09-14 02:20:45.089906','123','王教练的课程 - 2025-09-13 16:00','2025-09-13 14:17:21.366683','2025-09-14 02:20:45.089906',224,57,10,'unpaid'),(27,'2025-09-18 17:00:00.000000','2025-09-18 18:00:00.000000',1.0,100.00,'cancelled',NULL,'2025-09-14 02:20:55.718237','123','王教练的课程 - 2025-09-14 9:00','2025-09-13 14:17:21.420718','2025-09-14 02:20:55.718237',224,55,8,'unpaid'),(28,'2025-09-17 22:00:00.000000','2025-09-17 23:00:00.000000',1.0,100.00,'cancelled',NULL,'2025-09-14 02:22:58.043386','123','王教练的课程 - 2025-09-14 14:00','2025-09-13 14:17:21.488442','2025-09-14 02:22:58.043386',224,56,9,'unpaid'),(29,'2025-09-17 00:00:00.000000','2025-09-17 01:00:00.000000',1.0,100.00,'confirmed',NULL,NULL,NULL,'王教练的课程 - 2025-09-14 16:00','2025-09-13 14:17:21.544070','2025-09-13 14:27:58.216966',NULL,57,10,'unpaid'),(30,'2025-09-15 17:00:00.000000','2025-09-15 18:00:00.000000',1.0,100.00,'confirmed',NULL,NULL,NULL,'王教练的课程 - 2025-09-15 9:00','2025-09-13 14:17:21.654173','2025-09-13 14:27:58.173411',NULL,55,8,'unpaid'),(31,'2025-09-14 22:00:00.000000','2025-09-14 23:00:00.000000',1.0,100.00,'confirmed',NULL,NULL,NULL,'王教练的课程 - 2025-09-15 14:00','2025-09-13 14:17:21.698918','2025-09-13 14:27:58.117621',NULL,56,9,'unpaid'),(32,'2025-09-14 00:00:00.000000','2025-09-14 01:00:00.000000',1.0,100.00,'completed',NULL,NULL,NULL,'王教练的课程 - 2025-09-15 16:00','2025-09-13 14:17:21.743125','2025-09-14 02:22:43.473022',NULL,57,10,'unpaid'),(38,'2025-09-16 02:38:02.736358','2025-09-16 03:38:02.736358',1.0,100.00,'confirmed',NULL,NULL,NULL,NULL,'2025-09-14 02:38:02.738353','2025-09-14 02:38:02.738353',NULL,17,8,'unpaid'),(45,'2025-09-16 08:15:13.443663','2025-09-16 09:15:13.443663',1.0,100.00,'pending',NULL,NULL,NULL,'测试预约退费功能','2025-09-15 08:15:13.459018','2025-09-15 08:15:13.459018',NULL,68,16,'unpaid');
/*!40000 ALTER TABLE `reservations_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations_booking_cancellation`
--

DROP TABLE IF EXISTS `reservations_booking_cancellation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations_booking_cancellation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reason` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `response_message` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `booking_id` bigint NOT NULL,
  `processed_by_id` bigint DEFAULT NULL,
  `requested_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `booking_id` (`booking_id`),
  KEY `reservations_booking_processed_by_id_7464e1bf_fk_accounts_` (`processed_by_id`),
  KEY `reservations_booking_requested_by_id_4b31b4bd_fk_accounts_` (`requested_by_id`),
  CONSTRAINT `reservations_booking_booking_id_edd73ebd_fk_reservati` FOREIGN KEY (`booking_id`) REFERENCES `reservations_booking` (`id`),
  CONSTRAINT `reservations_booking_processed_by_id_7464e1bf_fk_accounts_` FOREIGN KEY (`processed_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_booking_requested_by_id_4b31b4bd_fk_accounts_` FOREIGN KEY (`requested_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations_booking_cancellation`
--

LOCK TABLES `reservations_booking_cancellation` WRITE;
/*!40000 ALTER TABLE `reservations_booking_cancellation` DISABLE KEYS */;
INSERT INTO `reservations_booking_cancellation` VALUES (7,'123','pending',NULL,NULL,'2025-09-14 03:04:54.367294',21,NULL,4),(8,'123','pending',NULL,NULL,'2025-09-14 03:08:15.937690',38,NULL,4);
/*!40000 ALTER TABLE `reservations_booking_cancellation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations_coach_change_request`
--

DROP TABLE IF EXISTS `reservations_coach_change_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations_coach_change_request` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reason` longtext NOT NULL,
  `request_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `current_coach_approval` varchar(20) NOT NULL,
  `target_coach_approval` varchar(20) NOT NULL,
  `campus_admin_approval` varchar(20) NOT NULL,
  `current_coach_approved_at` datetime(6) DEFAULT NULL,
  `target_coach_approved_at` datetime(6) DEFAULT NULL,
  `campus_admin_approved_at` datetime(6) DEFAULT NULL,
  `current_coach_notes` longtext,
  `target_coach_notes` longtext,
  `campus_admin_notes` longtext,
  `processed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `campus_admin_approved_by_id` bigint DEFAULT NULL,
  `current_coach_id` bigint NOT NULL,
  `current_coach_approved_by_id` bigint DEFAULT NULL,
  `processed_by_id` bigint DEFAULT NULL,
  `student_id` bigint NOT NULL,
  `target_coach_id` bigint NOT NULL,
  `target_coach_approved_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reservations_coach_ch_campus_admin_approve_b8b8b8b8_fk_accounts_` (`campus_admin_approved_by_id`),
  KEY `reservations_coach_ch_current_coach_id_b8b8b8b8_fk_accounts_` (`current_coach_id`),
  KEY `reservations_coach_ch_current_coach_approv_b8b8b8b8_fk_accounts_` (`current_coach_approved_by_id`),
  KEY `reservations_coach_ch_processed_by_id_b8b8b8b8_fk_accounts_` (`processed_by_id`),
  KEY `reservations_coach_ch_student_id_b8b8b8b8_fk_accounts_` (`student_id`),
  KEY `reservations_coach_ch_target_coach_id_b8b8b8b8_fk_accounts_` (`target_coach_id`),
  KEY `reservations_coach_ch_target_coach_approve_b8b8b8b8_fk_accounts_` (`target_coach_approved_by_id`),
  CONSTRAINT `reservations_coach_ch_campus_admin_approve_b8b8b8b8_fk_accounts_` FOREIGN KEY (`campus_admin_approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_ch_current_coach_approv_b8b8b8b8_fk_accounts_` FOREIGN KEY (`current_coach_approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_ch_current_coach_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`current_coach_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_ch_processed_by_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`processed_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_ch_student_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_ch_target_coach_approve_b8b8b8b8_fk_accounts_` FOREIGN KEY (`target_coach_approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_ch_target_coach_id_b8b8b8b8_fk_accounts_` FOREIGN KEY (`target_coach_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations_coach_change_request`
--

LOCK TABLES `reservations_coach_change_request` WRITE;
/*!40000 ALTER TABLE `reservations_coach_change_request` DISABLE KEYS */;
INSERT INTO `reservations_coach_change_request` VALUES (4,'测试更换教练','2025-09-16 03:15:01.944717','pending','pending','pending','pending',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2025-09-16 03:15:01.944717','2025-09-16 03:15:01.944717',NULL,163,NULL,NULL,4,102,NULL);
/*!40000 ALTER TABLE `reservations_coach_change_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations_coach_student_relation`
--

DROP TABLE IF EXISTS `reservations_coach_student_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations_coach_student_relation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied_by` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied_at` datetime(6) NOT NULL,
  `processed_at` datetime(6) DEFAULT NULL,
  `terminated_at` datetime(6) DEFAULT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `coach_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reservations_coach_stude_coach_id_student_id_c548921f_uniq` (`coach_id`,`student_id`),
  KEY `reservations_coach_s_student_id_e3cc0084_fk_accounts_` (`student_id`),
  CONSTRAINT `reservations_coach_s_coach_id_925e9816_fk_accounts_` FOREIGN KEY (`coach_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `reservations_coach_s_student_id_e3cc0084_fk_accounts_` FOREIGN KEY (`student_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations_coach_student_relation`
--

LOCK TABLES `reservations_coach_student_relation` WRITE;
/*!40000 ALTER TABLE `reservations_coach_student_relation` DISABLE KEYS */;
INSERT INTO `reservations_coach_student_relation` VALUES (16,'approved','student','2025-09-12 14:20:49.587416',NULL,NULL,'学员选择教练：王教练','2025-09-12 14:20:49.587416',163,120),(17,'approved','student','2025-09-12 14:22:07.346006',NULL,NULL,'学员选择教练：王教练','2025-09-12 14:22:07.346006',163,4),(18,'approved','student','2025-09-12 14:28:13.263654','2025-09-12 14:28:55.121926',NULL,'测试申请','2025-09-12 14:28:13.263654',102,4),(23,'pending','student','2025-09-13 02:23:48.062031',NULL,NULL,'我希望跟随您学习乒乓球技术，提高自己的技术水平。我对乒乓球很有兴趣，希望能够得到专业的指导。','2025-09-13 02:23:48.062031',183,184),(24,'pending','student','2025-09-13 02:23:48.664112',NULL,NULL,'我是乒乓球初学者，希望能够在您的指导下掌握基本技术，培养对乒乓球的兴趣。','2025-09-13 02:23:48.664112',183,185),(25,'pending','student','2025-09-13 02:23:49.245641',NULL,NULL,'我想提高乒乓球竞技水平，希望能够得到您的专业指导，参加比赛。','2025-09-13 02:23:49.245641',183,186),(26,'pending','student','2025-09-13 02:26:30.734678',NULL,NULL,'我希望跟随前端测试教练教练学习乒乓球技术','2025-09-13 02:26:30.734678',191,192),(27,'pending','student','2025-09-13 02:26:30.779817',NULL,NULL,'我希望跟随前端测试教练教练学习乒乓球技术','2025-09-13 02:26:30.779817',191,193),(28,'approved','student','2025-09-13 02:26:30.846304',NULL,NULL,'我希望跟随前端测试教练教练学习乒乓球技术','2025-09-13 02:26:30.846304',191,194),(34,'pending','student','2025-09-13 03:06:01.566401',NULL,NULL,'学员选择教练：调试教练','2025-09-13 03:06:01.566401',198,167),(35,'pending','student','2025-09-13 03:06:07.308874',NULL,NULL,'学员选择教练：前端测试教练','2025-09-13 03:06:07.309136',191,167),(36,'approved','student','2025-09-13 03:06:11.986553','2025-09-13 06:55:00.655073',NULL,'学员选择教练：王教练','2025-09-13 03:06:11.991564',163,167),(37,'approved','student','2025-09-13 03:06:17.477807','2025-09-13 03:07:18.466051',NULL,'学员选择教练：李教练','2025-09-13 03:06:17.477807',162,167),(38,'approved','student','2025-09-13 03:06:19.488499','2025-09-13 03:06:47.158269',NULL,'学员选择教练：张教练','2025-09-13 03:06:19.488499',161,167),(40,'pending','student','2025-09-13 03:16:34.233919',NULL,NULL,'学员选择教练：王教练','2025-09-13 03:16:34.233919',178,168),(41,'pending','student','2025-09-13 03:16:36.502935',NULL,NULL,'学员选择教练：李教练','2025-09-13 03:16:36.502935',177,168),(42,'pending','student','2025-09-13 03:16:39.292034',NULL,NULL,'学员选择教练：张教练','2025-09-13 03:16:39.292034',176,168),(43,'approved','student','2025-09-13 03:20:11.742646','2025-09-13 03:20:11.806408',NULL,'希望能成为您的学员，请多指教！','2025-09-13 03:20:11.742646',102,96),(46,'pending','student','2025-09-13 03:26:58.756669',NULL,NULL,'学员选择教练：王教练','2025-09-13 03:26:58.756669',178,169),(47,'pending','student','2025-09-13 03:27:01.429844',NULL,NULL,'学员选择教练：张教练','2025-09-13 03:27:01.429844',176,169),(52,'pending','student','2025-09-13 06:53:46.698652',NULL,NULL,'学员选择教练：李教练','2025-09-13 06:53:46.698652',177,169),(53,'approved','student','2025-09-13 06:53:51.092123','2025-09-13 06:54:58.547019',NULL,'学员选择教练：王教练','2025-09-13 06:53:51.092123',163,169),(55,'approved','student','2025-09-13 14:17:21.085752',NULL,NULL,NULL,'2025-09-13 14:17:21.085752',224,226),(56,'approved','student','2025-09-13 14:17:21.140141',NULL,NULL,NULL,'2025-09-13 14:17:21.140141',224,227),(57,'approved','student','2025-09-13 14:17:21.217905',NULL,NULL,NULL,'2025-09-13 14:17:21.217905',224,228),(64,'approved','student','2025-09-15 08:11:56.847822','2025-09-15 08:11:56.846809',NULL,NULL,'2025-09-15 08:11:56.848803',268,269),(65,'approved','student','2025-09-15 08:12:38.667654','2025-09-15 08:12:38.665984',NULL,NULL,'2025-09-15 08:12:38.667654',270,271),(66,'approved','student','2025-09-15 08:13:17.663404','2025-09-15 08:13:17.662408',NULL,NULL,'2025-09-15 08:13:17.663404',272,273),(67,'approved','student','2025-09-15 08:14:34.546608','2025-09-15 08:14:34.538654',NULL,NULL,'2025-09-15 08:14:34.547598',274,275),(68,'approved','student','2025-09-15 08:15:12.505182','2025-09-15 08:15:12.503153',NULL,NULL,'2025-09-15 08:15:12.505182',276,277),(83,'approved','student','2025-09-15 11:51:11.692393','2025-09-15 11:51:11.685727',NULL,NULL,'2025-09-15 11:51:11.692393',320,319),(84,'approved','student','2025-09-15 11:51:13.121255','2025-09-15 11:51:13.120268',NULL,NULL,'2025-09-15 11:51:13.121255',324,323),(85,'approved','student','2025-09-15 11:51:13.908306','2025-09-15 11:51:13.907308',NULL,NULL,'2025-09-15 11:51:13.908306',328,327),(86,'terminated','student','2025-09-15 11:51:14.846197','2025-09-15 11:51:14.844550','2025-09-15 11:51:15.180432',NULL,'2025-09-15 11:51:14.846197',332,331),(87,'approved','student','2025-09-15 11:51:15.181428','2025-09-15 11:51:15.180432',NULL,NULL,'2025-09-15 11:51:15.181428',333,331),(88,'terminated','student','2025-09-15 11:51:15.740997','2025-09-15 11:51:15.739997','2025-09-15 11:51:16.021209',NULL,'2025-09-15 11:51:15.741371',336,335),(89,'approved','student','2025-09-15 11:51:16.024219','2025-09-15 11:51:16.022205',NULL,NULL,'2025-09-15 11:51:16.024219',337,335),(90,'approved','student','2025-09-15 11:51:16.622201','2025-09-15 11:51:16.621201',NULL,NULL,'2025-09-15 11:51:16.622201',340,339);
/*!40000 ALTER TABLE `reservations_coach_student_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations_table`
--

DROP TABLE IF EXISTS `reservations_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations_table` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `number` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `campus_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `reservations_table_campus_id_number_ab9468a3_uniq` (`campus_id`,`number`),
  CONSTRAINT `reservations_table_campus_id_3eeba474_fk_campus_campus_id` FOREIGN KEY (`campus_id`) REFERENCES `campus_campus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations_table`
--

LOCK TABLES `reservations_table` WRITE;
/*!40000 ALTER TABLE `reservations_table` DISABLE KEYS */;
INSERT INTO `reservations_table` VALUES (1,'T01','球台1号','available',NULL,1,'2025-09-12 03:46:36.803954','2025-09-12 03:46:36.803983',2),(2,'T02','球台2号','available',NULL,1,'2025-09-12 03:46:36.855973','2025-09-12 03:46:36.855989',2),(3,'T03','球台3号','available',NULL,1,'2025-09-12 03:46:36.923072','2025-09-12 03:46:36.923096',2),(4,'T04','球台4号','available',NULL,1,'2025-09-12 03:46:36.981842','2025-09-12 03:46:36.981912',2),(5,'T05','球台5号','available',NULL,1,'2025-09-12 03:46:37.048579','2025-09-12 03:46:37.048648',2),(8,'C01','中心校区1号台','available',NULL,1,'2025-09-13 08:35:21.295402','2025-09-13 08:35:21.295402',1),(9,'C02','中心校区2号台','available',NULL,1,'2025-09-13 08:35:21.445234','2025-09-13 08:35:21.445234',1),(10,'C03','中心校区3号台','available',NULL,1,'2025-09-13 08:35:21.489147','2025-09-13 08:35:21.489147',1),(11,'C04','中心校区4号台','available',NULL,1,'2025-09-13 08:35:21.543591','2025-09-13 08:35:21.543591',1),(12,'C05','中心校区5号台','available',NULL,1,'2025-09-13 08:35:21.585546','2025-09-13 08:35:21.585546',1),(13,'100','temp1','available','123123123',1,'2025-09-15 07:28:55.119870','2025-09-15 07:28:55.119870',21),(14,'T002','测试球台2','available','测试球台',1,'2025-09-15 07:59:28.414528','2025-09-15 07:59:28.414528',47),(15,'T001','测试球台1','available',NULL,1,'2025-09-15 08:14:34.768070','2025-09-15 08:14:34.768070',54),(16,'T001','测试球台1','available',NULL,1,'2025-09-15 08:15:12.625528','2025-09-15 08:15:12.625528',55);
/*!40000 ALTER TABLE `reservations_table` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-19 14:46:28
