-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: BREWBEAUTY
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add product',6,'add_product'),(22,'Can change product',6,'change_product'),(23,'Can delete product',6,'delete_product'),(24,'Can view product',6,'view_product'),(25,'Can add order',7,'add_order'),(26,'Can change order',7,'change_order'),(27,'Can delete order',7,'delete_order'),(28,'Can view order',7,'view_order'),(29,'Can add order item',8,'add_orderitem'),(30,'Can change order item',8,'change_orderitem'),(31,'Can delete order item',8,'delete_orderitem'),(32,'Can view order item',8,'view_orderitem'),(33,'Can add shipping address',9,'add_shippingaddress'),(34,'Can change shipping address',9,'change_shippingaddress'),(35,'Can delete shipping address',9,'delete_shippingaddress'),(36,'Can view shipping address',9,'view_shippingaddress'),(37,'Can add employee',10,'add_employee'),(38,'Can change employee',10,'change_employee'),(39,'Can delete employee',10,'delete_employee'),(40,'Can view employee',10,'view_employee'),(41,'Can add user',11,'add_user'),(42,'Can change user',11,'change_user'),(43,'Can delete user',11,'delete_user'),(44,'Can view user',11,'view_user'),(45,'Can add customer',12,'add_customer'),(46,'Can change customer',12,'change_customer'),(47,'Can delete customer',12,'delete_customer'),(48,'Can view customer',12,'view_customer'),(49,'Can add product image',13,'add_productimage'),(50,'Can change product image',13,'change_productimage'),(51,'Can delete product image',13,'delete_productimage'),(52,'Can view product image',13,'view_productimage'),(53,'Can add product variation',14,'add_productvariation'),(54,'Can change product variation',14,'change_productvariation'),(55,'Can delete product variation',14,'delete_productvariation'),(56,'Can view product variation',14,'view_productvariation'),(57,'Can add payment',15,'add_payment'),(58,'Can change payment',15,'change_payment'),(59,'Can delete payment',15,'delete_payment'),(60,'Can view payment',15,'view_payment'),(61,'Can add inventory log',16,'add_inventorylog'),(62,'Can change inventory log',16,'change_inventorylog'),(63,'Can delete inventory log',16,'delete_inventorylog'),(64,'Can view inventory log',16,'view_inventorylog'),(65,'Can add product recommendation',17,'add_productrecommendation'),(66,'Can change product recommendation',17,'change_productrecommendation'),(67,'Can delete product recommendation',17,'delete_productrecommendation'),(68,'Can view product recommendation',17,'view_productrecommendation'),(69,'Can add Customer Profile',18,'add_customerprofile'),(70,'Can change Customer Profile',18,'change_customerprofile'),(71,'Can delete Customer Profile',18,'delete_customerprofile'),(72,'Can view Customer Profile',18,'view_customerprofile'),(73,'Can add Skin Assessment',19,'add_skinassessment'),(74,'Can change Skin Assessment',19,'change_skinassessment'),(75,'Can delete Skin Assessment',19,'delete_skinassessment'),(76,'Can view Skin Assessment',19,'view_skinassessment'),(77,'Can add some model',20,'add_somemodel'),(78,'Can change some model',20,'change_somemodel'),(79,'Can delete some model',20,'delete_somemodel'),(80,'Can view some model',20,'view_somemodel'),(81,'Can add skin profile',21,'add_skinprofile'),(82,'Can change skin profile',21,'change_skinprofile'),(83,'Can delete skin profile',21,'delete_skinprofile'),(84,'Can view skin profile',21,'view_skinprofile'),(85,'Can add Skin Assessment',22,'add_skinassessment'),(86,'Can change Skin Assessment',22,'change_skinassessment'),(87,'Can delete Skin Assessment',22,'delete_skinassessment'),(88,'Can view Skin Assessment',22,'view_skinassessment'),(89,'Can add customer address',23,'add_customeraddress'),(90,'Can change customer address',23,'change_customeraddress'),(91,'Can delete customer address',23,'delete_customeraddress'),(92,'Can view customer address',23,'view_customeraddress'),(93,'Can add recommendation event',24,'add_recommendationevent'),(94,'Can change recommendation event',24,'change_recommendationevent'),(95,'Can delete recommendation event',24,'delete_recommendationevent'),(96,'Can view recommendation event',24,'view_recommendationevent');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(24,'recommendation','recommendationevent'),(22,'recommendation','skinassessment'),(21,'recommendation','skinprofile'),(5,'sessions','session'),(23,'store','customeraddress'),(16,'store','inventorylog'),(7,'store','order'),(8,'store','orderitem'),(15,'store','payment'),(6,'store','product'),(13,'store','productimage'),(17,'store','productrecommendation'),(14,'store','productvariation'),(9,'store','shippingaddress'),(12,'users','customer'),(18,'users','customerprofile'),(10,'users','employee'),(19,'users','skinassessment'),(20,'users','somemodel'),(11,'users','user');
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
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-24 09:14:25.161064'),(2,'contenttypes','0002_remove_content_type_name','2025-04-24 09:14:25.370193'),(3,'auth','0001_initial','2025-04-24 09:14:25.829911'),(4,'auth','0002_alter_permission_name_max_length','2025-04-24 09:14:25.959941'),(5,'auth','0003_alter_user_email_max_length','2025-04-24 09:14:25.977264'),(6,'auth','0004_alter_user_username_opts','2025-04-24 09:14:25.988745'),(7,'auth','0005_alter_user_last_login_null','2025-04-24 09:14:26.021885'),(8,'auth','0006_require_contenttypes_0002','2025-04-24 09:14:26.043924'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-24 09:14:26.072747'),(10,'auth','0008_alter_user_username_max_length','2025-04-24 09:14:26.089004'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-24 09:14:26.125493'),(12,'auth','0010_alter_group_name_max_length','2025-04-24 09:14:26.165331'),(13,'auth','0011_update_proxy_permissions','2025-04-24 09:14:26.180950'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-24 09:14:26.206459'),(15,'users','0001_initial','2025-04-24 09:14:26.705001'),(16,'admin','0001_initial','2025-04-24 09:14:26.996679'),(17,'admin','0002_logentry_remove_auto_add','2025-04-24 09:14:27.010415'),(18,'admin','0003_logentry_add_action_flag_choices','2025-04-24 09:14:27.029518'),(19,'sessions','0001_initial','2025-04-24 09:14:27.119357'),(20,'store','0001_initial','2025-04-24 09:14:27.165095'),(21,'store','0002_cart','2025-04-24 09:14:27.434681'),(22,'store','0003_product_digital_order_orderitem_shippingaddress_and_more','2025-04-24 09:14:28.028297'),(23,'store','0004_orderitem_quantity','2025-04-24 09:14:28.124921'),(24,'store','0005_rename_image_product_images','2025-04-24 09:14:28.184415'),(25,'store','0006_alter_product_images','2025-04-24 09:14:28.202586'),(26,'store','0007_alter_product_images','2025-04-24 09:14:28.213946'),(27,'store','0008_category_alter_product_category','2025-04-24 09:14:28.512026'),(28,'store','0009_alter_product_category_delete_category','2025-04-24 09:14:28.758862'),(29,'store','0010_category_alter_product_category','2025-04-24 09:14:29.072149'),(30,'store','0011_alter_product_category_delete_category','2025-04-24 09:14:29.305207'),(31,'store','0012_alter_product_digital','2025-04-24 09:14:29.387259'),(32,'store','0013_alter_product_images','2025-04-24 09:14:29.394604'),(33,'store','0014_order_order_id_alter_product_images','2025-04-24 09:14:29.614239'),(34,'store','0015_alter_order_user_alter_shippingaddress_user','2025-04-24 09:14:29.659889'),(35,'users','0002_alter_employee_photo','2025-04-24 09:14:29.667262'),(36,'users','0003_employee_password','2025-04-24 09:14:29.759675'),(37,'users','0004_alter_user_groups_alter_user_user_permissions','2025-04-24 09:14:29.808037'),(38,'users','0005_employee_user','2025-04-27 15:42:21.951996'),(39,'users','0006_customer','2025-05-03 10:13:05.840780'),(40,'store','0016_remove_product_images_productimage_productvariation','2025-05-15 13:48:24.274745'),(41,'users','0007_employee_first_name_employee_last_name','2025-05-15 13:48:24.406820'),(42,'users','0008_alter_customer_user','2025-05-15 16:37:36.019129'),(43,'users','0009_alter_employee_user','2025-05-15 17:10:09.136292'),(44,'store','0017_product_brand','2025-05-15 18:10:13.337189'),(45,'store','0018_order_customer_order_status_alter_order_user_and_more','2025-05-18 08:36:04.936261'),(46,'store','0019_remove_order_customer','2025-05-18 08:52:02.711638'),(47,'store','0020_remove_order_status_alter_order_user','2025-05-18 08:54:44.886386'),(48,'store','0021_payment','2025-05-18 14:48:15.396301'),(49,'store','0022_alter_productimage_image','2025-05-18 17:03:30.016141'),(50,'store','0023_alter_productimage_image','2025-05-19 07:05:10.964747'),(51,'store','0024_alter_productimage_image','2025-05-19 14:17:22.570085'),(52,'store','0025_delete_productimage','2025-05-19 15:19:55.647919'),(53,'store','0026_productimage','2025-05-19 15:26:32.226445'),(54,'store','0027_alter_productimage_image','2025-05-22 15:55:48.560349'),(55,'users','0010_alter_employee_photo','2025-05-22 15:55:48.596960'),(56,'store','0028_alter_productimage_image_alter_productimage_product','2025-05-22 16:40:31.601252'),(57,'store','0029_remove_product_skin_tone_and_more','2025-05-23 11:17:01.107278'),(58,'store','0030_remove_product_variation_code','2025-05-24 16:48:59.141980'),(59,'store','0031_inventorylog','2025-05-24 17:42:48.495131'),(60,'users','0011_remove_customer_loyalty_points_and_more','2025-05-26 06:04:33.698068'),(61,'users','0012_alter_customer_profile_picture','2025-05-26 06:56:17.312788'),(62,'store','0032_order_parcel_image_order_status_order_status_updated_and_more','2025-05-28 11:20:12.224528'),(63,'store','0033_payment_order','2025-05-28 12:13:24.149665'),(64,'store','0034_remove_order_order_id','2025-05-28 17:23:44.408122'),(65,'store','0035_order_order_id','2025-05-28 17:34:29.929082'),(66,'store','0036_remove_order_order_id','2025-05-28 17:40:39.598738'),(67,'store','0034_remove_order_order_id_product_finish_and_more','2025-05-28 20:21:47.740505'),(68,'store','0035_product_coverage_product_spf','2025-05-29 13:49:48.177682'),(69,'store','0036_alter_product_spf','2025-05-29 14:15:36.900403'),(70,'store','0037_alter_product_coverage','2025-05-29 14:57:53.637967'),(71,'store','0038_order_receipt_order_shipping_address_and_more','2025-05-30 02:26:08.063386'),(72,'store','0039_alter_order_shipping_address','2025-05-30 02:31:37.440846'),(73,'store','0040_productrecommendation_alter_product_options_and_more','2025-06-02 19:15:06.502670'),(74,'users','0013_customerprofile_skinassessment_somemodel_and_more','2025-06-02 19:15:06.929009'),(75,'recommendation','0001_initial','2025-06-02 19:15:06.999015'),(76,'recommendation','0002_initial','2025-06-02 19:15:07.111196'),(77,'store','0041_productrecommendation_customer_and_more','2025-06-02 19:15:07.443323'),(78,'store','0042_order_total','2025-06-03 07:34:48.778489'),(79,'users','0014_rename_primary_skin_concerns_customerprofile_concerns_and_more','2025-06-03 07:34:48.980277'),(80,'store','0043_orderitem_variation','2025-06-03 07:36:52.138292'),(81,'users','0015_delete_skinassessment','2025-06-03 10:20:14.391352'),(82,'recommendation','0003_skinassessment','2025-06-03 10:20:14.609871'),(83,'store','0044_remove_shippingaddress_user_customeraddress','2025-06-03 17:41:22.308365'),(84,'store','0045_alter_productrecommendation_options_and_more','2025-06-03 19:16:48.694187'),(85,'users','0016_customerprofile_first_name_customerprofile_last_name','2025-06-07 15:09:50.690022'),(86,'users','0017_customerprofile_email','2025-06-07 15:16:14.896618'),(87,'users','0018_alter_customerprofile_profile_picture','2025-06-07 15:30:17.051957'),(88,'store','0046_product_is_featured','2025-06-07 16:13:09.327520'),(89,'recommendation','0004_skinassessment_surface_tone','2025-06-19 05:52:23.094752'),(90,'store','0047_alter_product_long_last','2025-06-19 05:52:23.126619'),(91,'recommendation','0005_recommendationevent','2025-06-19 19:50:40.814199'),(92,'store','0048_alter_product_quantity','2025-06-21 07:26:14.042548');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4pp0jowr5sn9sspykcj3ushahiab7mkn','.eJxVjDsOwyAQRO9CHSFg-ZiU6X0GtF4gOImwZOwqyt2DJRdJN5r3Zt4s4L6VsLe0hjmyK5Ps8ttNSM9UDxAfWO8Lp6Vu6zzxQ-EnbXxcYnrdTvfvoGArfa1cFgq9BqFhkBYiERjhDUYTnbMepRKCyGZFVvjcgYGUNUIaoEfPPl-5mzcP:1uSs2T:doBDXUgFcgJBK0pHOtNGUH7RiaNjqaAA-Hj_kCbXv9k','2025-07-05 06:49:21.989443'),('879i4cqx46dc2cbo9qoityp6eb94f2yj','.eJxVjDsOwyAQRO9CHSFg-ZiU6X0GtF4gOImwZOwqyt2DJRdJN5r3Zt4s4L6VsLe0hjmyK5Ps8ttNSM9UDxAfWO8Lp6Vu6zzxQ-EnbXxcYnrdTvfvoGArfa1cFgq9BqFhkBYiERjhDUYTnbMepRKCyGZFVvjcgYGUNUIaoEfPPl-5mzcP:1uR320:T_NL4Wzk2QB8QnC0mLxSeMB6fGwNwZZ15ujGa1Hhpjg','2025-06-30 06:09:20.915150'),('hu6zvr77jc3avrtos9wue5bceu4j3t6v','.eJxVjDsOwjAQBe_iGllaf9eU9JzB2rUdHECOFCdVxN1JpBTQvpl5m4i0LjWuvcxxzOIqlLj8bkzpVdoB8pPaY5Jpass8sjwUedIu71Mu79vp_h1U6nWvPbJF0IM1FJxTiBbIUfAIg7IGILHTGLIvmALv2IMGb2xAFYgNOvH5AqksNiU:1uSs3M:5vcSrVUyyG3sDJbxNuiuTs01ae9n0-BGwriZcHkTcLc','2025-07-05 06:50:16.405261'),('ieoxr63tsh682nfo1myqf7f2tghyc467','.eJxVjDsOwjAQBe_iGllaf9eU9JzB2rUdHECOFCdVxN1JpBTQvpl5m4i0LjWuvcxxzOIqlLj8bkzpVdoB8pPaY5Jpass8sjwUedIu71Mu79vp_h1U6nWvPbJF0IM1FJxTiBbIUfAIg7IGILHTGLIvmALv2IMGb2xAFYgNOvH5AqksNiU:1uL3Ju:2U2ee6f5c0XqYdoEESA2ZLbppTkG5PHZAaz6vvuu54Y','2025-06-13 17:15:02.852024'),('koz9vy02i06uof3189s2of1q0g6icw8f','.eJxVjEEOwiAQAP_C2RCW7lLw6L1vaBaW2qqBpLQn499Nkx70OjOZtxp53-Zxb3kdF1FXBaguvzByeuZyGHlwuVedatnWJeoj0adteqiSX7ez_RvM3Obj67BzwNkEAu4Bk2GCXiSLSOzQARGZKVjwxtMEdrLRM6LzmAIQkvp8AeSONtk:1uNiE3:kVpFZdsDfY5A4uTeYjCf0lD0pmQcZmZuEh9PVQxf3Z8','2025-06-21 01:19:59.448021'),('oadn5repq08iudotf0m4qnsc6tsyr8k4','.eJxVjDsOwyAQRO9CHSFg-ZiU6X0GtF4gOImwZOwqyt2DJRdJN5r3Zt4s4L6VsLe0hjmyK5Ps8ttNSM9UDxAfWO8Lp6Vu6zzxQ-EnbXxcYnrdTvfvoGArfa1cFgq9BqFhkBYiERjhDUYTnbMepRKCyGZFVvjcgYGUNUIaoEfPPl-5mzcP:1uSs2S:zYR775ytyX7hRLGWTGMrB6DIUxRd3GgGvb7v5RgPqZg','2025-07-05 06:49:20.380508');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommendation_recommendationevent`
--

DROP TABLE IF EXISTS `recommendation_recommendationevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendation_recommendationevent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `event_type` varchar(10) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `product_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `recommendation_recom_product_id_d6256f2c_fk_store_pro` (`product_id`),
  KEY `recommendat_user_id_372a5c_idx` (`user_id`,`product_id`),
  KEY `recommendat_event_t_38a5b3_idx` (`event_type`),
  KEY `recommendat_timesta_0a9fad_idx` (`timestamp`),
  CONSTRAINT `recommendation_recom_product_id_d6256f2c_fk_store_pro` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`),
  CONSTRAINT `recommendation_recom_user_id_e2ec19d2_fk_users_use` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendation_recommendationevent`
--

LOCK TABLES `recommendation_recommendationevent` WRITE;
/*!40000 ALTER TABLE `recommendation_recommendationevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `recommendation_recommendationevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommendation_skinassessment`
--

DROP TABLE IF EXISTS `recommendation_skinassessment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendation_skinassessment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `assessment_date` datetime(6) NOT NULL,
  `hydration_level` int NOT NULL,
  `oiliness_level` int NOT NULL,
  `sensitivity_level` int NOT NULL,
  `acne_proneness` int NOT NULL,
  `aging_concerns` int NOT NULL,
  `skin_type` varchar(20) NOT NULL,
  `undertone` varchar(20) NOT NULL,
  `concerns` varchar(255) NOT NULL,
  `finish_preference` varchar(20) DEFAULT NULL,
  `texture_preference` varchar(20) DEFAULT NULL,
  `customer_id` bigint NOT NULL,
  `surface_tone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recommendation_skina_customer_id_b1bc247b_fk_users_cus` (`customer_id`),
  CONSTRAINT `recommendation_skina_customer_id_b1bc247b_fk_users_cus` FOREIGN KEY (`customer_id`) REFERENCES `users_customerprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendation_skinassessment`
--

LOCK TABLES `recommendation_skinassessment` WRITE;
/*!40000 ALTER TABLE `recommendation_skinassessment` DISABLE KEYS */;
INSERT INTO `recommendation_skinassessment` VALUES (1,'2025-06-03 11:48:36.787179',1,4,1,2,2,'oily','warm','acne,redness,sensitive','matte','powder',1,NULL),(2,'2025-06-03 19:27:53.955845',1,4,1,2,2,'oily','warm','acne,redness,sensitive','matte','powder',1,NULL),(3,'2025-06-03 19:39:03.324342',1,4,1,2,2,'oily','warm','acne,redness,sensitive','matte','powder',1,NULL),(4,'2025-06-03 19:39:30.925458',1,4,1,2,2,'oily','warm','acne,redness,sensitive','matte','powder',1,NULL),(5,'2025-06-06 19:14:25.077358',5,4,5,1,3,'dry','warm','acne,aging','matte','liquid',1,NULL),(6,'2025-06-06 19:31:43.639370',5,4,5,1,3,'dry','olive','acne,aging,redness','matte','liquid',1,NULL),(7,'2025-06-06 20:01:12.835118',5,4,5,1,3,'dry','olive','acne,aging,redness','matte','liquid',1,NULL),(8,'2025-06-06 21:38:53.576149',5,4,5,1,3,'normal','cool','acne','matte','liquid',1,NULL),(9,'2025-06-09 20:53:42.733157',5,4,5,1,3,'normal','cool','acne','dewy','liquid',1,NULL),(10,'2025-06-19 04:39:27.742702',3,3,3,3,4,'oily','warm','acne,redness,dehydrated','dewy','liquid',1,NULL),(11,'2025-06-19 04:43:33.607457',3,3,3,3,4,'oily','warm','acne,redness,dehydrated','dewy','liquid',1,NULL),(12,'2025-06-19 04:46:26.322639',3,3,3,3,4,'oily','warm','acne,redness,dehydrated','dewy','liquid',1,NULL),(13,'2025-06-19 05:17:22.558089',3,3,3,3,4,'oily','warm','acne,redness,dehydrated','dewy','liquid',1,NULL),(14,'2025-06-19 05:27:28.474707',3,3,3,3,4,'normal','warm','acne,redness,dehydrated','dewy','liquid',1,NULL),(15,'2025-06-19 05:40:51.065423',3,3,3,3,4,'oily','warm','acne,redness,dehydrated','dewy','liquid',1,NULL),(16,'2025-06-19 05:54:00.604626',3,2,2,3,2,'dry','olive','acne,redness,dehydrated','matte','powder',1,NULL),(17,'2025-06-19 09:47:01.882368',3,2,2,3,2,'dry','olive','acne,redness,dehydrated','matte','powder',1,NULL),(18,'2025-06-19 10:02:55.139599',3,2,2,3,2,'dry','olive','acne,redness,dehydrated,sensitive','matte','powder',1,NULL),(19,'2025-06-19 10:07:55.793675',3,2,2,3,2,'normal','cool','acne,redness,dehydrated,pigmentation','matte','powder',1,NULL),(20,'2025-06-19 12:13:12.284404',3,4,2,3,4,'normal','cool','acne,redness,dehydrated,pigmentation','matte','cream',1,NULL),(21,'2025-06-19 22:12:51.866541',3,4,2,3,4,'normal','cool','acne,redness,dehydrated,pigmentation','matte','cream',1,NULL),(22,'2025-06-19 22:13:14.005651',3,4,2,4,4,'normal','cool','acne,redness,dehydrated,pigmentation','matte','cream',1,NULL),(23,'2025-06-19 23:03:03.665427',4,2,2,3,2,'oily','olive','acne,pigmentation','glitter','liquid',1,NULL),(24,'2025-06-20 02:44:39.763486',4,2,2,3,2,'oily','olive','acne,pigmentation','glitter','gel',1,NULL),(25,'2025-06-20 02:46:56.142912',4,2,2,3,2,'oily','olive','acne,pigmentation','glitter','gel',1,NULL),(26,'2025-06-20 03:01:49.080497',4,4,2,3,3,'dry','cool','acne,sensitive,pigmentation','glitter','cream',1,NULL);
/*!40000 ALTER TABLE `recommendation_skinassessment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommendation_skinprofile`
--

DROP TABLE IF EXISTS `recommendation_skinprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendation_skinprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `skin_type` varchar(20) NOT NULL,
  `concerns` varchar(200) NOT NULL,
  `undertone` varchar(20) NOT NULL,
  `sensitivity` varchar(10) NOT NULL,
  `texture_preference` varchar(20) NOT NULL,
  `finish_preference` varchar(20) NOT NULL,
  `customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customer_id` (`customer_id`),
  CONSTRAINT `recommendation_skinp_customer_id_88348a6e_fk_users_cus` FOREIGN KEY (`customer_id`) REFERENCES `users_customerprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendation_skinprofile`
--

LOCK TABLES `recommendation_skinprofile` WRITE;
/*!40000 ALTER TABLE `recommendation_skinprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `recommendation_skinprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_customeraddress`
--

DROP TABLE IF EXISTS `store_customeraddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_customeraddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(200) NOT NULL,
  `city` varchar(200) NOT NULL,
  `state` varchar(200) NOT NULL,
  `zipcode` varchar(200) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store_customeraddress_user_id_56fd1689_fk_users_user_id` (`user_id`),
  CONSTRAINT `store_customeraddress_user_id_56fd1689_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_customeraddress`
--

LOCK TABLES `store_customeraddress` WRITE;
/*!40000 ALTER TABLE `store_customeraddress` DISABLE KEYS */;
INSERT INTO `store_customeraddress` VALUES (1,'D03-147, Apartment Taman Universiti, Jalan Persiaran Taman Universiti, 86400 Parit Raja, Batu Pahat, Johor\r\nBatu Pahat, Johor, 86400','Batu Pahat','Johor','86400',1),(2,'D03-147, Apartment Taman Universiti, Jalan Persiaran Taman Universiti, 86400 Parit Raja, Batu Pahat, Johor\r\nBatu Pahat, Johor, 86400','Batu Pahat','Johor','86400',17);
/*!40000 ALTER TABLE `store_customeraddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_inventorylog`
--

DROP TABLE IF EXISTS `store_inventorylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_inventorylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stock_in` int unsigned NOT NULL,
  `stock_out` int unsigned NOT NULL,
  `date_logged` date NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_inventorylog_product_id_c1385dc5_fk_store_product_id` (`product_id`),
  CONSTRAINT `store_inventorylog_product_id_c1385dc5_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`),
  CONSTRAINT `store_inventorylog_chk_1` CHECK ((`stock_in` >= 0)),
  CONSTRAINT `store_inventorylog_chk_2` CHECK ((`stock_out` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_inventorylog`
--

LOCK TABLES `store_inventorylog` WRITE;
/*!40000 ALTER TABLE `store_inventorylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_inventorylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_order`
--

DROP TABLE IF EXISTS `store_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_ordered` datetime(6) NOT NULL,
  `complete` tinyint(1) NOT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `user_id` bigint DEFAULT NULL,
  `parcel_image` varchar(100) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `status_updated` datetime(6) NOT NULL,
  `tracking_number` varchar(100) DEFAULT NULL,
  `receipt` varchar(100) DEFAULT NULL,
  `shipping_address_id` bigint DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_order_user_id_ae5f7a5f_fk_users_user_id` (`user_id`),
  KEY `store_order_shipping_address_id_9d19a8a7_fk_store_shi` (`shipping_address_id`),
  CONSTRAINT `store_order_shipping_address_id_9d19a8a7_fk_store_shi` FOREIGN KEY (`shipping_address_id`) REFERENCES `store_shippingaddress` (`id`),
  CONSTRAINT `store_order_user_id_ae5f7a5f_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_order`
--

LOCK TABLES `store_order` WRITE;
/*!40000 ALTER TABLE `store_order` DISABLE KEYS */;
INSERT INTO `store_order` VALUES (13,'2025-06-03 16:59:51.267545',1,NULL,1,'','verified','2025-06-07 01:34:47.480619',NULL,'receipts/Intern_Resume_1.pdf',2,61.99),(14,'2025-06-03 17:53:47.484485',1,NULL,1,'','verified','2025-06-07 16:58:01.344391',NULL,'',NULL,61.99),(16,'2025-06-07 18:16:57.847923',1,NULL,1,'','pending','2025-06-07 18:16:57.848040',NULL,'',NULL,37.90),(17,'2025-06-07 18:17:19.544697',1,NULL,1,'','pending','2025-06-07 18:17:19.570867',NULL,'receipts/TRANSCRIPT_EZLYN.pdf',NULL,37.90),(19,'2025-06-09 21:07:31.336652',1,NULL,1,'','pending','2025-06-09 21:07:31.378574',NULL,'receipts/GANTT_CHART.pdf',4,37.90),(20,'2025-06-11 18:35:31.662079',0,NULL,1,'','pending','2025-06-11 18:35:31.662576',NULL,'',NULL,0.00),(22,'2025-06-16 15:31:38.408488',1,NULL,17,'','verified','2025-06-16 15:40:15.898247',NULL,'receipts/images.jfif',5,37.90);
/*!40000 ALTER TABLE `store_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_orderitem`
--

DROP TABLE IF EXISTS `store_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_added` datetime(6) NOT NULL,
  `order_id` bigint DEFAULT NULL,
  `product_id` bigint DEFAULT NULL,
  `quantity` int NOT NULL,
  `variation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store_orderitem_order_id_acf8722d_fk_store_order_id` (`order_id`),
  KEY `store_orderitem_product_id_f2b098d4_fk_store_product_id` (`product_id`),
  KEY `store_orderitem_variation_id_10b2cc08_fk_store_pro` (`variation_id`),
  CONSTRAINT `store_orderitem_order_id_acf8722d_fk_store_order_id` FOREIGN KEY (`order_id`) REFERENCES `store_order` (`id`),
  CONSTRAINT `store_orderitem_product_id_f2b098d4_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`),
  CONSTRAINT `store_orderitem_variation_id_10b2cc08_fk_store_pro` FOREIGN KEY (`variation_id`) REFERENCES `store_productvariation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_orderitem`
--

LOCK TABLES `store_orderitem` WRITE;
/*!40000 ALTER TABLE `store_orderitem` DISABLE KEYS */;
INSERT INTO `store_orderitem` VALUES (3,'2025-05-17 13:57:41.257892',NULL,1,1,NULL),(4,'2025-05-17 13:57:43.192819',NULL,NULL,2,NULL),(5,'2025-05-17 15:03:58.554650',NULL,NULL,2,NULL),(6,'2025-05-17 15:11:36.663732',NULL,3,1,NULL),(7,'2025-05-17 15:11:58.328365',NULL,1,2,NULL),(8,'2025-05-18 05:27:37.370415',NULL,NULL,2,NULL),(9,'2025-05-18 05:27:37.374074',NULL,3,1,NULL),(10,'2025-05-18 13:20:02.659363',NULL,3,1,NULL),(11,'2025-05-18 13:20:08.228911',NULL,3,1,NULL),(12,'2025-05-18 13:20:15.190008',NULL,3,1,NULL),(13,'2025-05-18 13:20:17.892104',NULL,3,1,NULL),(14,'2025-05-18 13:20:39.774325',NULL,3,1,NULL),(15,'2025-05-18 13:21:54.834224',NULL,3,1,NULL),(16,'2025-05-18 13:28:46.762371',NULL,3,1,NULL),(30,'2025-06-03 16:03:03.249000',NULL,8,1,6),(31,'2025-06-03 16:59:51.276715',13,8,1,6),(32,'2025-06-03 17:53:47.494224',14,8,1,7),(33,'2025-06-07 00:04:28.845525',NULL,NULL,1,NULL),(34,'2025-06-07 17:09:26.178362',NULL,3,1,3),(35,'2025-06-07 18:16:57.864856',16,3,1,3),(36,'2025-06-07 18:17:19.555701',17,3,1,3),(37,'2025-06-09 21:01:16.071101',NULL,3,1,3),(38,'2025-06-09 21:07:31.350503',19,3,1,3),(39,'2025-06-11 18:36:24.090306',20,3,1,3),(40,'2025-06-16 15:30:55.482236',NULL,3,1,3),(41,'2025-06-16 15:31:38.471183',22,3,1,3);
/*!40000 ALTER TABLE `store_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_payment`
--

DROP TABLE IF EXISTS `store_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `receipt` varchar(100) DEFAULT NULL,
  `order_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  CONSTRAINT `store_payment_order_id_b5ee0383_fk_store_order_id` FOREIGN KEY (`order_id`) REFERENCES `store_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_payment`
--

LOCK TABLES `store_payment` WRITE;
/*!40000 ALTER TABLE `store_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `store_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_product`
--

DROP TABLE IF EXISTS `store_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `price` decimal(10,2) NOT NULL,
  `quantity` int unsigned DEFAULT NULL,
  `min_stock` int unsigned NOT NULL,
  `max_stock` int unsigned NOT NULL,
  `category` varchar(20) DEFAULT NULL,
  `skin_type` varchar(20) DEFAULT NULL,
  `skin_condition` varchar(100) DEFAULT NULL,
  `skin_texture` varchar(20) DEFAULT NULL,
  `sensitivity_level` varchar(10) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `digital` tinyint(1) DEFAULT NULL,
  `brand` varchar(100) NOT NULL,
  `finish` varchar(20) DEFAULT NULL,
  `is_cruelty_free` tinyint(1) DEFAULT NULL,
  `is_vegan` tinyint(1) DEFAULT NULL,
  `long_last` tinyint(1) DEFAULT NULL,
  `size` varchar(20) NOT NULL,
  `suitable_for` varchar(20) NOT NULL,
  `texture` varchar(20) DEFAULT NULL,
  `waterproof` tinyint(1) DEFAULT NULL,
  `coverage` varchar(20) DEFAULT NULL,
  `spf` int DEFAULT NULL,
  `detailed_description` longtext,
  `is_hypoallergenic` tinyint(1) NOT NULL,
  `popularity_score` double NOT NULL,
  `subcategory` varchar(50) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `is_featured` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `store_product_chk_1` CHECK ((`quantity` >= 0)),
  CONSTRAINT `store_product_chk_2` CHECK ((`min_stock` >= 0)),
  CONSTRAINT `store_product_chk_3` CHECK ((`max_stock` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_product`
--

LOCK TABLES `store_product` WRITE;
/*!40000 ALTER TABLE `store_product` DISABLE KEYS */;
INSERT INTO `store_product` VALUES (1,'Liquid foundation','foundation',30.00,100,20,199,'Foundation',NULL,'Sensitive',NULL,NULL,'2025-05-15 20:04:46.203090','2025-06-21 06:55:02.930109',0,'Trulook',NULL,0,0,0,'Size','all',NULL,0,NULL,NULL,'',0,0,NULL,NULL,0),(3,'Cupcake Cream Blush 2.0','Blusher to blush your cheeks',29.90,200,25,300,'Blusher',NULL,'Acne-Prone',NULL,NULL,'2025-05-17 15:08:14.255515','2025-06-16 10:24:57.154298',0,'Maezz',NULL,0,0,0,'Size','all',NULL,0,NULL,NULL,'',0,0,NULL,NULL,0),(5,'Powder Contour','For Shading',19.99,49,10,99,'Contour','Combination','Dehydrated','Pori Besar','Medium','2025-05-19 16:11:50.945189','2025-05-19 16:11:50.945230',0,'Cubremi','',0,0,0,'Size','all',NULL,0,NULL,NULL,NULL,0,0,NULL,NULL,0),(8,'azwaezlyn','ghfhgfchgv',53.99,20,10,100,'Foundation','dry','Sensitive','Berparut','low','2025-05-30 13:43:24.852851','2025-05-30 13:43:24.906961',1,'Brand','glitter',0,0,1,'Size','combination','cream',1,'full',56,NULL,0,0,NULL,NULL,0),(16,'Liquid Foundation 30ΓÇ»ml','Foundation ringan, buildable coverage tanpa rasa berat',35.00,75,20,198,'Foundation','all','open pores, fine lines','large_pores','low','2025-06-20 03:54:40.859099','2025-06-20 03:54:40.937051',1,'Cubremi','matte',0,NULL,1,'30ΓÇ»ml','all',NULL,0,'medium',NULL,'Foundation ringan, buildable coverage tanpa rasa berat',1,0,'Liquid Foundation','lightweight, buildable, poreΓÇæblur',1),(17,'Foundation Stick','Krim foundation, SPF50, menyesuaikan nada kulit selepas sapuan',35.00,58,48,298,'Foundation','all','Aging, fine lines','smooth','low','2025-06-20 08:07:07.517795','2025-06-20 08:07:07.642124',1,'Cubremi','satin',1,0,1,'Stick','all',NULL,0,'full',49,'Krim foundation, SPF50, menyesuaikan nada kulit selepas sapuan',1,1,'Foundation Stick','SPF50, no cracks, allΓÇæinΓÇæone',1),(18,'Haute Liquid Blush On Moisturizing Blusher 8 Colors','',17.95,157,20,100,'Blusher',NULL,'Moisturizing, dull','smooth','low','2025-06-20 08:26:42.749107','2025-06-21 07:11:12.465107',1,'O.TWO.O','glitter',1,0,1,'30g','all',NULL,1,'medium',-1,'',1,3,'Liquid Blusher','Light, watery texture, Moisturizing, non-sticky',1),(19,'colorkey','',24.99,25,0,100,NULL,NULL,NULL,NULL,NULL,'2025-06-21 07:27:22.474467','2025-06-21 07:27:22.506389',0,'Brand',NULL,0,0,0,'Size','all',NULL,0,NULL,NULL,'',0,0,NULL,NULL,0);
/*!40000 ALTER TABLE `store_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_productimage`
--

DROP TABLE IF EXISTS `store_productimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_productimage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_productimage_product_id_e50e4046_fk_store_product_id` (`product_id`),
  CONSTRAINT `store_productimage_product_id_e50e4046_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_productimage`
--

LOCK TABLES `store_productimage` WRITE;
/*!40000 ALTER TABLE `store_productimage` DISABLE KEYS */;
INSERT INTO `store_productimage` VALUES (1,'product_image/download (3).jfif',1),(3,'product_image/blusher.jfif',3),(5,'product_image/contour.jfif',5),(6,'product_image/contour2.jfif',5),(7,'product_image/contour3.jfif',5),(8,'product_image/blusher_2.jfif',3),(9,'product_image/blusher.jfif',3),(10,'product_image/blusher_2.jfif',3),(11,'product_image/blusher_3.jfif',3),(14,'product_image/rppf4_En0A6cw.jfif',8),(15,'product_image/rppf3_mndJJOa.jpg',8),(16,'product_image/product1.jfif',16),(17,'product_image/product3.jfif',17),(18,'product_image/product_2.jfif',17),(19,'product_image/product7_oF5G8hT.webp',18),(20,'product_image/product5_z9HkOtK.webp',18),(21,'product_image/product6_BubQkA4.webp',18),(22,'product_image/product5_qFzXpuz.webp',18),(23,'product_image/product6_sj5Hevb.webp',18),(24,'product_image/product7_Dn2F2ff.webp',18),(25,'product_image/product1_3Qspqkw.jfif',1),(26,'product_image/product6_zn8IJDC.webp',19);
/*!40000 ALTER TABLE `store_productimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_productrecommendation`
--

DROP TABLE IF EXISTS `store_productrecommendation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_productrecommendation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `match_score` double NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `customer_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_productrecommendation_product_id_customer_id_10f5f472_uniq` (`product_id`,`customer_id`),
  KEY `store_productrecomme_customer_id_c1346ae7_fk_users_cus` (`customer_id`),
  CONSTRAINT `store_productrecomme_customer_id_c1346ae7_fk_users_cus` FOREIGN KEY (`customer_id`) REFERENCES `users_customerprofile` (`id`),
  CONSTRAINT `store_productrecomme_product_id_db663302_fk_store_pro` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=265 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_productrecommendation`
--

LOCK TABLES `store_productrecommendation` WRITE;
/*!40000 ALTER TABLE `store_productrecommendation` DISABLE KEYS */;
INSERT INTO `store_productrecommendation` VALUES (259,0.4,'Content similarity: 1.0','2025-06-20 03:01:49.220525',1,3),(260,0,'No strong signals','2025-06-20 03:01:49.220621',1,1),(262,0,'No strong signals','2025-06-20 03:01:49.220688',1,5),(264,0,'No strong signals','2025-06-20 03:01:49.220746',1,8);
/*!40000 ALTER TABLE `store_productrecommendation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_productvariation`
--

DROP TABLE IF EXISTS `store_productvariation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_productvariation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `variation_code` varchar(50) NOT NULL,
  `quantity` int unsigned NOT NULL,
  `product_id` bigint NOT NULL,
  `skin_tone` varchar(20) DEFAULT NULL,
  `surface_tones` varchar(20) DEFAULT NULL,
  `hex_color` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_productvariation_product_id_variation_code_7d27d8dc_uniq` (`product_id`,`variation_code`),
  CONSTRAINT `store_productvariation_product_id_279b7a52_fk_store_product_id` FOREIGN KEY (`product_id`) REFERENCES `store_product` (`id`),
  CONSTRAINT `store_productvariation_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_productvariation`
--

LOCK TABLES `store_productvariation` WRITE;
/*!40000 ALTER TABLE `store_productvariation` DISABLE KEYS */;
INSERT INTO `store_productvariation` VALUES (1,'001',50,1,NULL,NULL,NULL),(3,'01',20,3,NULL,NULL,NULL),(6,'rose',10,8,'Warm Undertone','Sederhana',NULL),(7,'tulip',10,8,'Warm Undertone','Terang',NULL),(8,'Light Ivory',25,16,'neutral','light',NULL),(9,'Natural',25,16,'neutral','medium',NULL),(10,'Tanned',25,16,'warm','tan',NULL),(11,'Light',20,17,'neutral','very_fair',NULL),(12,'Natural',19,17,'olive','fair',NULL),(13,'Medium',19,17,'warm','light',NULL),(14,'01 Bean Paste',20,18,'neutral','fair',NULL),(15,'02 Pleasure',19,18,'neutral','light',NULL),(16,'03 Coral Peach',20,18,'warm','light',NULL),(17,'04 Wild Rose',18,18,'olive','medium',NULL),(18,'05 Warm Sun',20,18,'warm','medium',NULL),(19,'06 Sunset Red',20,18,'cool','tan',NULL),(20,'07 Cinnamon',20,18,'cool','light',NULL),(21,'08 Toffee',20,18,'warm','light',NULL),(22,'01 Bean Paste',25,19,NULL,NULL,NULL);
/*!40000 ALTER TABLE `store_productvariation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store_shippingaddress`
--

DROP TABLE IF EXISTS `store_shippingaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `store_shippingaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` varchar(200) NOT NULL,
  `city` varchar(200) NOT NULL,
  `state` varchar(200) NOT NULL,
  `zipcode` varchar(200) NOT NULL,
  `date_added` datetime(6) NOT NULL,
  `order_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store_shippingaddress_order_id_e6decfbb_fk_store_order_id` (`order_id`),
  CONSTRAINT `store_shippingaddress_order_id_e6decfbb_fk_store_order_id` FOREIGN KEY (`order_id`) REFERENCES `store_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_shippingaddress`
--

LOCK TABLES `store_shippingaddress` WRITE;
/*!40000 ALTER TABLE `store_shippingaddress` DISABLE KEYS */;
INSERT INTO `store_shippingaddress` VALUES (2,'D03-147, Apartment Taman Universiti, Jalan Persiaran Taman Universiti, 86400 Parit Raja, Batu Pahat, Johor\r\nBatu Pahat, Johor, 86400','Batu Pahat','Johor','86400','2025-06-03 16:59:51.281978',NULL),(3,'D03-147, Apartment Taman Universiti, Jalan Persiaran Taman Universiti, 86400 Parit Raja, Batu Pahat, Johor\r\nBatu Pahat, Johor, 86400','Batu Pahat','Johor','86400','2025-06-07 18:17:19.564727',17),(4,'D03-147, Apartment Taman Universiti, Jalan Persiaran Taman Universiti, 86400 Parit Raja, Batu Pahat, Johor\r\nBatu Pahat, Johor, 86400','Batu Pahat','Johor','86400','2025-06-09 21:07:31.362974',19),(5,'D03-147, Apartment Taman Universiti, Jalan Persiaran Taman Universiti, 86400 Parit Raja, Batu Pahat, Johor\r\nBatu Pahat, Johor, 86400','Batu Pahat','Johor','86400','2025-06-16 15:31:38.490479',22);
/*!40000 ALTER TABLE `store_shippingaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_customerprofile`
--

DROP TABLE IF EXISTS `users_customerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_customerprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(15) DEFAULT NULL,
  `preferred_contact_method` varchar(10) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `skin_type` varchar(20) DEFAULT NULL,
  `undertone` varchar(10) DEFAULT NULL,
  `surface_tone` varchar(20) DEFAULT NULL,
  `concerns` varchar(255) DEFAULT NULL,
  `sensitivity_level` varchar(10) DEFAULT NULL,
  `known_allergies` longtext,
  `preferred_finish` varchar(20) DEFAULT NULL,
  `preferred_coverage` varchar(20) DEFAULT NULL,
  `preferred_texture` varchar(20) DEFAULT NULL,
  `ethical_preferences` json NOT NULL,
  `last_skin_assessment` datetime(6) DEFAULT NULL,
  `skin_assessment_version` varchar(10) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `email` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `users_customerprofile_user_id_c320f1e5_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_customerprofile`
--

LOCK TABLES `users_customerprofile` WRITE;
/*!40000 ALTER TABLE `users_customerprofile` DISABLE KEYS */;
INSERT INTO `users_customerprofile` VALUES (1,'0149840609','email','female','2003-10-25','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.892031','2025-06-07 15:54:55.742131',1,'Ezlyn Azwa','Lah','ezlyn0910@gmail.com'),(2,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.912772','2025-06-03 11:03:12.912814',2,NULL,NULL,NULL),(3,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.922416','2025-06-03 11:03:12.922458',3,NULL,NULL,NULL),(4,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.941640','2025-06-03 11:03:12.941680',6,NULL,NULL,NULL),(5,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.952941','2025-06-03 11:03:12.952983',8,NULL,NULL,NULL),(6,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.964229','2025-06-03 11:03:12.964272',10,NULL,NULL,NULL),(7,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.974577','2025-06-03 11:03:12.974618',11,NULL,NULL,NULL),(8,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:12.984777','2025-06-03 11:03:12.984824',12,NULL,NULL,NULL),(9,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:13.001382','2025-06-03 11:03:13.001422',13,NULL,NULL,NULL),(10,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-03 11:03:13.083028','2025-06-03 11:03:13.083066',14,NULL,NULL,NULL),(11,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-07 00:39:58.505529','2025-06-07 00:39:58.505568',15,NULL,NULL,NULL),(12,NULL,'email',NULL,NULL,'',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-07 01:06:04.016685','2025-06-07 01:06:04.016727',16,NULL,NULL,NULL),(13,'0149840609','email','female','2003-07-22','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'[]',NULL,NULL,'2025-06-16 15:29:02.028048','2025-06-16 15:33:09.194085',17,'Anissa','June','ezlyn0910@gmail.com');
/*!40000 ALTER TABLE `users_customerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_employee`
--

DROP TABLE IF EXISTS `users_employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `position` varchar(100) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `date_hired` date NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `password` varchar(128) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_employee_user_id_6131bb7a_uniq` (`user_id`),
  CONSTRAINT `users_employee_user_id_6131bb7a_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_employee`
--

LOCK TABLES `users_employee` WRITE;
/*!40000 ALTER TABLE `users_employee` DISABLE KEYS */;
INSERT INTO `users_employee` VALUES (4,'admin3','Admin','0149840906','dezpaxnjtxb@hotmail.com','2025-05-10','','defaultpassword',13,'firstname','lastname'),(5,'Balqis','Casher','0111569824','irieizumi1@gmail.com','2024-11-07','media/employee_photo/photo_2025-05-14_14-20-58.jpg','Balqis123',14,'Izz','Balqis'),(6,'Ash','Manager','0111569824','ash123@gmail.com','2025-03-11','employee_photo/photo_2025-05-28_23-59-38.jpg','Ash123@',15,'Asyra','Muhammad'),(7,'Deeniy','Inventory Coordinator','0156505544','deeniy123@gmail.com','2024-12-18','employee_photo/photo_2025-06-01_22-30-43.jpg','Deeniy123@',16,'Deeniy','Dina'),(8,'Nik','','0149840609','ezlyn0910@gmail.com','2024-12-24','employee_photo/download.jfif','defaultpassword',2,'Nicky','Jun');
/*!40000 ALTER TABLE `users_employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$870000$LDvFTkafwcZWZIpo61fzX8$Wxg2t8wHG4KNGMYB/fuXHAVkASuZY24AEfjWg/8K2qs=','2025-06-21 06:49:24.227492',0,'ezlynazwa','','','ezlyn0910@gmail.com',0,1,'2025-04-24 09:49:10.835059'),(2,'pbkdf2_sha256$870000$JDcQVniAXVmOLHPWCocH1E$VBaZcF4ac6Zt/2mX1JOz4DL29/9M7hKzjYz8w+3cLXU=','2025-06-21 06:50:16.398247',1,'admin1','','','ezlyn0910@gmail.com',1,1,'2025-04-24 11:58:02.295764'),(3,'pbkdf2_sha256$870000$mHiDy8nTG8QjImBpYJhKUT$OtAyTlIWkCsZo2EusqR0kJp6oeO0DuYPXB4aENOfhkQ=',NULL,1,'Azwa','','','ai220213@student.uthm.edu.my',1,1,'2025-04-28 04:49:27.089716'),(6,'pbkdf2_sha256$870000$yQAKDfeNBd3alYBzjZen61$1jntTxF2zdSIzdFauNk74lOwCDEyxzFpGwSvubJr8DM=',NULL,1,'Azlyn','','','ai220213@student.uthm.edu.my',1,1,'2025-04-28 05:33:37.524778'),(8,'pbkdf2_sha256$870000$sAbJQQUSjhkZkeMShjpB4K$OYhE2Gs460Y++RNkVyXOX02gZImqxdXLGJvff9osaT8=',NULL,1,'Ahmad ','','','ahmad123@gmail.com',1,1,'2025-04-28 05:41:15.352704'),(10,'pbkdf2_sha256$870000$FjhAFajBCAYaNVh1xETolZ$a5f+oSjuEdWXTKLeKkWjE3eJpF4NRE00IfRbRaQw2o0=','2025-05-08 15:38:42.083373',0,'Baihaqi','','','baiqiqi54@gmail.com',0,1,'2025-05-08 15:38:38.908213'),(11,'pbkdf2_sha256$870000$ZXuZPA9DVDhvNsg00KZqZ6$VQTKALSQffJ64sDjPX+N/Dxa3+0f4jkEz1Q+AC6LpCk=',NULL,0,'Ezlyn2','Nur Ezlyn Azwa','Lah','ezlyn0910@gmail.com',1,1,'2025-05-15 16:01:25.855493'),(12,'pbkdf2_sha256$870000$oh83X1GdjtntSndl9W7bFC$zYjkRtavfPB44Uy0tQjJ27RgXq0FfaZnitGigpyPgtE=',NULL,1,'admin2','Bunga','Orkid','ezlyn0910@gmail.com',1,1,'2025-05-15 16:31:36.408565'),(13,'pbkdf2_sha256$870000$GLXLTmODn86SL4jr1DUbiB$CEsQAbthUt/kLz4JmwN7XDX9E/7+bhA7/9ihtf67+Vg=','2025-05-18 16:06:59.418907',1,'admin3','Izz','Muhammad','dezpaxnjtxb@hotmail.com',1,1,'2025-05-15 16:49:33.012755'),(14,'pbkdf2_sha256$870000$14Bm2R1xGvd3WRvzO2olWe$n26YQ8MFOnWlQ4i5184q+co32cAjYv/QnR7hoqQoEbA=','2025-06-20 08:30:05.496597',0,'Balqis','Izz','Balqis','irieizumi1@gmail.com',1,1,'2025-05-15 17:20:09.908179'),(15,'pbkdf2_sha256$870000$pKJq6hXsIouBwRlwgsBzC1$bLJbNKRcaGFkWuq4NipV2nwf71i9PEY0jQdEsZp09nc=',NULL,1,'Ash','Asyra','Muhammad','ash123@gmail.com',1,1,'2025-06-07 00:39:55.724758'),(16,'pbkdf2_sha256$870000$fBrU5i09c7QAq0SdRy0IkS$kOG6ORkT4wPNrzSd1jZAvo1K51HTmaTlOcfRliDoSFY=',NULL,0,'Deeniy','Deeniy','Dina','deeniy123@gmail.com',1,1,'2025-06-07 01:06:01.227483'),(17,'pbkdf2_sha256$870000$heTIkTr5UJwXZoOrCxHrwJ$tt1UakC9MJMSyQyisnNoqvzATJbF/nPfIdIblv2PEe8=','2025-06-16 15:30:02.836543',0,'Anissa','','','irieizumi1@gmail.com',0,1,'2025-06-16 15:29:00.347208');
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_groups`
--

DROP TABLE IF EXISTS `users_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_groups_user_id_group_id_b88eab82_uniq` (`user_id`,`group_id`),
  KEY `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_user_groups_group_id_9afc8d0e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_user_groups_user_id_5f6f5a90_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_groups`
--

LOCK TABLES `users_user_groups` WRITE;
/*!40000 ALTER TABLE `users_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_user_permissions`
--

DROP TABLE IF EXISTS `users_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_user_permissions_user_id_permission_id_43338c45_uniq` (`user_id`,`permission_id`),
  KEY `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_user_perm_permission_id_0b93982e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_user_permissions_user_id_20aca447_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_user_permissions`
--

LOCK TABLES `users_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-22 12:06:30
