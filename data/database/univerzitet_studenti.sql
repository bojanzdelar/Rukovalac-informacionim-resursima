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
-- Table structure for table `studenti`
--

DROP TABLE IF EXISTS `studenti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studenti` (
  `vu_oznaka` char(2) NOT NULL,
  `stu_struka` char(2) NOT NULL,
  `stu_broj_indeksa` varchar(6) NOT NULL,
  `stu_prezime` varchar(20) NOT NULL,
  `stu_ime_roditelja` varchar(20) DEFAULT NULL,
  `stu_ime` varchar(20) NOT NULL,
  `stu_pol` char(1) NOT NULL DEFAULT 'N',
  `stu_adresa_stanovanja` varchar(80) DEFAULT NULL,
  `stu_telefon` varchar(20) DEFAULT NULL,
  `stu_jmbg` char(13) DEFAULT NULL,
  `stu_datum_rodjenja` date DEFAULT NULL,
  PRIMARY KEY (`vu_oznaka`,`stu_struka`,`stu_broj_indeksa`),
  CONSTRAINT `fk_studiraju_na` FOREIGN KEY (`vu_oznaka`) REFERENCES `visokoskolska_ustanova` (`vu_oznaka`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studenti`
--

LOCK TABLES `studenti` WRITE;
/*!40000 ALTER TABLE `studenti` DISABLE KEYS */;
INSERT INTO `studenti` VALUES ('FK','SP','151001','Grujic','Milivoje','Ana','Z','Beograd','381632142414','909997865599','1997-09-09'),('FK','SP','161103','Zoric','Nebojsa','Milan','M','Beograd','381622948512','1112000288826','2000-12-11'),('FK','SP','171101','Tomicevic','Jovan','Violeta','Z','Beograd','381652345864','2309997486339','1997-09-23'),('FK','SP','181206','Jovanov','Pavle','Jelena','Z','Beograd','381623105120','804999612522','1999-04-08'),('FK','SP','191203','Tatomirovic','Dimitrije','Vladislav','M','Novi Sad','381611847295','1502998778833','1998-02-15'),('FK','SP','201207','Kosijer','Mirko','Dejan','M','Novi Sad','381642947563','1804000117888','2000-04-18'),('IR','IT','162311','Suvic','Anastazija','Mina','Z','Beograd','381622847529','1307998772159','1998-07-13'),('IR','IT','172507','Dragosavljevic','Marko','Djordje','M','Beograd','381631947385','1507999485120','1999-07-15'),('IR','IT','182512','Stefanovic','Strahinja','Ivan','M','Beograd','381601859306','107000579235','2000-07-01'),('IR','IT','192302','Mazic','Stefan','Aleksandra','Z','Beograd','381611837452','411997688833','1997-11-04'),('IR','IT','192503','Milinkovic','Milica','Mladen','M','Novi Sad','381631846305','603997753770','1997-03-06'),('IR','IT','202306','Dostanic','Nemanja','Branko','M','Beograd','381651843058','1802997282476','1997-02-18'),('PF','PO','174212','Mirkovic','Todor','Katarina','Z','Beograd','381633254982','2305000207943','2000-05-23'),('PF','PO','184204','Perunovic','Petar','Milovan','M','Novi Sad','381661049538','2502000728286','2000-02-25'),('PF','PO','184306','Cvetincanin','Zora','Kristina','Z','Novi Sad','381642863469','1104000182497','2000-04-11'),('PF','PO','194208','Pavic','Borislav','Darko','M','Sremska Mitrovica','381622306923','2807000957778','2000-07-28'),('PF','PO','194307','Milic','Predrag','Dalma','Z','Beograd','381642958421','1608999527041','1999-08-16'),('PF','PO','204303','Jancic','Maksim','Lazar','M','Beograd','381631260493','1004000190907','2000-04-10'),('TF','IT','182708','Milakovic','Nenad','Marija','Z','Beograd','381622948376','2808997270266','1997-08-28'),('TF','IT','192701','Markovic','Milan','Igor','M','Novi Sad','381645551323','1610000748687','2000-10-16'),('TF','IT','192709','Zdelar','Slobodan','Bojan','M','Sremska Mitrovica','381645556356','609999444489','1999-09-06'),('TH','TH','173205','Milkovic','Albert','Filip','M','Beograd','381627938150','312000706555','2000-12-03'),('TH','TH','183207','Starovic','Ognjen','Dusko','M','Nis','381631133245','1104999596174','1999-04-11'),('TH','TH','183304','Maticic','Luka','Lena','Z','Beograd','381602836548','1708000302345','2000-08-17'),('TH','TH','193108','Dzombeta','Nikola','Dusan','M','Nis','381669534876','1409000506754','2000-09-14'),('TH','TH','193307','Krstic','Anastazija','Mihajlo','M','Beograd','381602164065','903000583491','2000-03-09'),('TH','TH','193308','Pantic','Robert','Vesna','Z','Beograd','381614356333','308999489667','1999-08-03'),('TH','TH','203103','Novakovic','Nikola','Ivana','Z','Novi Sad','381655334568','2411997147809','1997-11-24'),('TH','TH','203112','Rasulic','Vladan','Isidora','Z','Beograd','381641234555','1004998455702','1998-04-10'),('TH','TH','203206','Mihajlovic','Igor','Drago','M','Beograd','381634435678','1502998833997','1998-02-15');
/*!40000 ALTER TABLE `studenti` ENABLE KEYS */;
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
