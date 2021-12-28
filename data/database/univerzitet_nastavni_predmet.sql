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
-- Table structure for table `nastavni_predmet`
--

DROP TABLE IF EXISTS `nastavni_predmet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nastavni_predmet` (
  `vu_oznaka` char(2) NOT NULL,
  `np_oznaka` varchar(6) NOT NULL,
  `np_naziv` varchar(120) NOT NULL,
  `np_espb` decimal(2,0) NOT NULL,
  PRIMARY KEY (`vu_oznaka`,`np_oznaka`),
  CONSTRAINT `fk_izvodi_predmete` FOREIGN KEY (`vu_oznaka`) REFERENCES `visokoskolska_ustanova` (`vu_oznaka`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nastavni_predmet`
--

LOCK TABLES `nastavni_predmet` WRITE;
/*!40000 ALTER TABLE `nastavni_predmet` DISABLE KEYS */;
INSERT INTO `nastavni_predmet` VALUES ('FK','ANT','Antropomotorika',8),('FK','FA','Funkcionalna anatomija',8),('FK','ITS','Internet tehnologije u sportu',8),('IR','BP','Baze podataka',6),('IR','OP','Osnove programiranja',8),('IR','OS','Operativni sistemi',8),('PF','MEJ','Morfologija engleskog jezika',7),('PF','PSIHO','Psihologija',8),('PF','RACUN','Racunovodstvo',8),('TF','MRS','Metodologije razvoja softvera',8),('TF','SIMS','Specifikacije i modeliranje softvera',8),('TF','SPA','Strukture podataka i algortimi',8),('TH','MG','Medjunarodna gastronomija',6),('TH','MTD','Menadzment turistickih destinacija',6),('TH','MTH','Marketing u turizmu i hotelijerstvu',6);
/*!40000 ALTER TABLE `nastavni_predmet` ENABLE KEYS */;
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
