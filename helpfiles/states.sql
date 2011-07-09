-- MySQL dump 10.13  Distrib 5.5.10, for osx10.6 (i386)
--
-- Host: localhost    Database: twitter
-- ------------------------------------------------------
-- Server version	5.5.10

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
-- Table structure for table `states`
--

DROP TABLE IF EXISTS `states`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `states` (
  `state` varchar(2) NOT NULL,
  `state_long` varchar(30) DEFAULT NULL,
  `rgb` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`state`),
  UNIQUE KEY `state_long` (`state_long`),
  UNIQUE KEY `rgb_UNIQUE` (`rgb`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `states`
--

LOCK TABLES `states` WRITE;
/*!40000 ALTER TABLE `states` DISABLE KEYS */;
INSERT INTO `states` VALUES ('ac','Acre','0,255,0'),('al','Alagoas','242,103,34'),('am','Amazonas','255,255,0'),('ap','Amapá','0,255,255'),('ba','Bahia','142,76,33'),('ce','Ceará','0,170,169'),('df','Brazilian Federal District','255,255,255'),('es','Espírito Santo','254,220,189'),('go','Goiás','162,28,80'),('ma','Maranhão','130,0,79'),('mg','Minas Gerais','0,75,106'),('ms','Mato Grosso do Sul','0,173,104'),('mt','Mato Grosso','130,0,255'),('pa','Pará','0,0,255'),('pb','Paraíba','211,32,40'),('pe','Pernambuco','0,120,94'),('pi','Piauí','0,138,0'),('pr','Paraná','52,44,116'),('rj','Rio de Janeiro','236,0,135'),('rn','Rio Grande do Norte','195,121,179'),('ro','Rondônia','255,0,255'),('rr','Roraima','255,0,0'),('rs','Rio Grande do Sul','0,110,185'),('sc','Santa Catarina','255,211,0'),('se','Sergipe','204,222,105'),('sp','São Paulo','127,160,211'),('to','Tocantins','255,138,79');
/*!40000 ALTER TABLE `states` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-07-09  9:52:46
