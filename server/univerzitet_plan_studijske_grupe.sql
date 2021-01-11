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
-- Table structure for table `plan_studijske_grupe`
--

DROP TABLE IF EXISTS `plan_studijske_grupe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plan_studijske_grupe` (
  `stu_vu_oznaka` char(2) NOT NULL,
  `sp_oznaka` varchar(3) NOT NULL,
  `spb_blok` decimal(2,0) NOT NULL,
  `spb_pozicija` decimal(2,0) NOT NULL,
  `vu_oznaka` char(2) NOT NULL,
  `np_oznaka` varchar(6) NOT NULL,
  PRIMARY KEY (`stu_vu_oznaka`,`sp_oznaka`,`spb_blok`,`spb_pozicija`),
  KEY `fk_na_poziciji` (`vu_oznaka`,`np_oznaka`),
  CONSTRAINT `fk_na_poziciji` FOREIGN KEY (`vu_oznaka`, `np_oznaka`) REFERENCES `nastavni_predmet` (`vu_oznaka`, `np_oznaka`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_struktura_po_blokovima` FOREIGN KEY (`stu_vu_oznaka`, `sp_oznaka`) REFERENCES `studijski_programi` (`vu_oznaka`, `sp_oznaka`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plan_studijske_grupe`
--

LOCK TABLES `plan_studijske_grupe` WRITE;
/*!40000 ALTER TABLE `plan_studijske_grupe` DISABLE KEYS */;
INSERT INTO `plan_studijske_grupe` VALUES ('FK','FVS',5,1,'FK','ANT'),('FK','FVS',3,2,'FK','FA'),('FK','MS',6,1,'FK','ITS'),('IR','IR',4,2,'IR','BP'),('IR','IT',3,1,'IR','OP'),('IR','IR',6,3,'IR','OS'),('PF','ANG',2,3,'PF','MEJ'),('PF','PE',3,1,'PF','PSIHO'),('PF','PE',4,1,'PF','RACUN'),('TF','SII',3,1,'TF','MRS'),('TF','SII',2,1,'TF','SIMS'),('TF','SII',1,1,'TF','SPA'),('TH','EH',2,2,'TH','MG'),('TH','TUR',6,1,'TH','MTD'),('TH','HOT',1,2,'TH','MTH');
/*!40000 ALTER TABLE `plan_studijske_grupe` ENABLE KEYS */;
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
