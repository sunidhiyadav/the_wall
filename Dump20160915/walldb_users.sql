-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: walldb
-- ------------------------------------------------------
-- Server version	5.7.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'sunidhi','sunidhi','s@s.com','2016-09-12 00:44:04','2016-09-12 00:44:04','$2b$12$JblPQNXT5/FgNF0OMRiHdObvUHEwE50LA0pbMsMotCysNMBRghm..'),(2,'antara','sri','antara@antara.com','2016-09-12 01:20:24','2016-09-12 01:20:24','$2b$12$pbJ8oX8oJrP28CTAAKQX8O5DAT8K42GfnRB7fXOhOGKxhsTmXIyzm'),(3,'test','test','test@test.com','2016-09-12 01:33:44','2016-09-12 01:33:44','$2b$12$U4tgMvHFwah4ZUtyXlSwHenNGPZo9M71nAW3dPymtGxrd2klxei0y'),(4,'Antara','Srivastava','antara@antara.com','2016-09-12 23:12:18','2016-09-12 23:12:18','$2b$12$BxYS5HgHP/62qE//FaKsGuu8Nkmd1RevhPuPOIOUZhM2zI74wW2F2'),(5,'Hung','Quach','hung.quach@gmail.com','2016-09-13 16:34:16','2016-09-13 16:34:16','$2b$12$4KpqJVliRDfxNn9H3ieTze2SNIkjeb7unl39wsFSU3sVuxqR/sJxW'),(12,'ghjh','jjhkhj','girl@girl.com','2016-09-14 19:52:52','2016-09-14 19:52:52','$2b$12$nF4M6VCAcsCUwO3XxHig2uv9YKnt8cbKEYmFEkNkrGCdAEQXtT5Uy');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-15 12:25:35
