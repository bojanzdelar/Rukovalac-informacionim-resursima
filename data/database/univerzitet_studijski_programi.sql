CREATE DATABASE  IF NOT EXISTS `univerzitet` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `univerzitet`;
-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: univerzitet
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `studijski_programi`
--

DROP TABLE IF EXISTS `studijski_programi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studijski_programi` (
  `vu_oznaka` char(2) NOT NULL,
  `niv_oznaka` decimal(2,0) NOT NULL,
  `sp_oznaka` varchar(3) NOT NULL,
  `sp_naziv` varchar(120) NOT NULL,
  PRIMARY KEY (`vu_oznaka`,`sp_oznaka`),
  KEY `fk_klasifikacija_po_nivou` (`niv_oznaka`),
  CONSTRAINT `fk_klasifikacija_po_nivou` FOREIGN KEY (`niv_oznaka`) REFERENCES `nivo_studija` (`niv_oznaka`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_obrazuje_za` FOREIGN KEY (`vu_oznaka`) REFERENCES `visokoskolska_ustanova` (`vu_oznaka`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studijski_programi`
--

LOCK TABLES `studijski_programi` WRITE;
/*!40000 ALTER TABLE `studijski_programi` DISABLE KEYS */;
INSERT INTO `studijski_programi` VALUES ('FK',10,'FVS','Fizicko vaspitanje i sport'),('FK',10,'MS','Menadzment u sportu'),('IR',10,'IR','Informatika i racunarstvo'),('IR',10,'IT','Informacione tehnologije'),('PF',10,'ANG','Anglistika'),('PF',10,'PE','Poslovna Ekonomija'),('TF',10,'SII','Softversko i informaciono inzenjerstvo'),('TH',10,'EH','Ekonomija hrane'),('TH',10,'HOT','Hotelijerstvo'),('TH',10,'TUR','Turizam');
/*!40000 ALTER TABLE `studijski_programi` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-11 16:09:10
