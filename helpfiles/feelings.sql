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
-- Table structure for table `feelings`
--

DROP TABLE IF EXISTS `feelings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feelings` (
  `id` int(11) NOT NULL,
  `feeling` varchar(20) DEFAULT NULL,
  `re` varchar(60) DEFAULT NULL,
  `rgb` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `feeling` (`feeling`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feelings`
--

LOCK TABLES `feelings` WRITE;
/*!40000 ALTER TABLE `feelings` DISABLE KEYS */;
INSERT INTO `feelings` VALUES (1,'feliz','fe+l+i+(s|z)','255,231,13'),(2,'triste','tri+st','4,63,105'),(3,'alegre','a+l+e+gr','255,164,1'),(4,'cansado','(c|k)a+n(s+|ç|sc|c)a+d','36,156,240'),(5,'morto','mo+rt(a|o|i)','200,0,39'),(6,'louco','lo+u+(c|k)','243,2,109'),(7,'fome','(fo+me+)|(fa+mi+nt)','247,32,65'),(8,'saudade','sa+u+da+d','1,91,92'),(9,'puto','pu+t(a|o)+','89,88,132'),(10,'nervoso','ne+(r|l)vo+(s|z+)','255,176,3'),(11,'tenso','te+n(c|ç|sc|s)','0,115,78'),(12,'doente','d(o|u)+e+nt','137,15,185'),(13,'culpado','(k|c)u+l*pa+d','0,78,111'),(14,'sozinho','so+(z+|s)i+nh','150,173,198'),(15,'estranho','(e|i)+stra+nh','243,1,87'),(16,'carente','(c|k)a+re+nt','1,72,114'),(17,'deprimido','de+pri+mi+d','40,49,82'),(18,'frio','fri+o+','127,181,183'),(19,'sono','so+no+','113,62,243'),(20,'preguiçoso','pre+gu*i+(sc|ç|s|c)','78,95,193'),(21,'disposto','d(e|i)+spo+st','254,153,1'),(22,'ótimo','(o|ó)+ti+m','255,216,1'),(23,'abençoado','a+be+n(s+|sc|ç|c)o+a+d','24,116,41'),(24,'sortudo','so+rtu+d','254,215,60'),(25,'velho','ve+lh(a|o)+','53,44,101'),(26,'forte','fo+rt','255,178,0'),(27,'fraco','(en){0,1}fra+(qu|k|c)','243,1,114'),(28,'relaxado','re+la+(ch|x)a+d','254,215,60'),(29,'orgulhoso','o+rgu+lho+(s|z)','255,179,0'),(30,'especial','e+spe+(c|s+|sc)i+a+l+','243,2,99'),(31,'estressado','e+stre+(c|ç|s+)a+n*d','146,86,160'),(32,'confortável','co+nfo+rt(á|a)+a*v','64,182,184'),(33,'confiante','co+nfi+a+nt','228,146,2'),(34,'apaixonado','a*pa+i+(x+|ch)o+na+d','115,32,124');
/*!40000 ALTER TABLE `feelings` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-07-09  9:53:36
