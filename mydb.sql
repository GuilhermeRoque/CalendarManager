-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.18.04.4

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
-- Table structure for table `Agenda`
--

DROP TABLE IF EXISTS `Agenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Agenda` (
  `idAgenda` int(11) NOT NULL AUTO_INCREMENT,
  `descricao` varchar(45) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `estado` bit(1) NOT NULL,
  PRIMARY KEY (`idAgenda`,`idUsuario`),
  KEY `fk_Agenda_Usuario_idx` (`idUsuario`),
  CONSTRAINT `fk_Agenda_Usuario` FOREIGN KEY (`idUsuario`) REFERENCES `Usuario` (`idUsuario`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Agenda`
--

LOCK TABLES `Agenda` WRITE;
/*!40000 ALTER TABLE `Agenda` DISABLE KEYS */;
INSERT INTO `Agenda` VALUES (1,'Agenda1',1,_binary ''),(2,'Agenda2',1,_binary '\0'),(3,'Agenda1',2,_binary ''),(4,'Agenda2',2,_binary ''),(5,'Agenda22',1,_binary '');
/*!40000 ALTER TABLE `Agenda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Evento`
--

DROP TABLE IF EXISTS `Evento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Evento` (
  `idEvento` int(11) NOT NULL AUTO_INCREMENT,
  `dia` date NOT NULL,
  `inicio` time NOT NULL,
  `fim` time NOT NULL,
  `idAgenda` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `descricao` varchar(45) NOT NULL,
  `vagas` int(11) NOT NULL,
  PRIMARY KEY (`idEvento`,`idAgenda`,`idUsuario`),
  KEY `fk_Event_Agenda1_idx` (`idAgenda`,`idUsuario`),
  CONSTRAINT `fk_Event_Agenda1` FOREIGN KEY (`idAgenda`, `idUsuario`) REFERENCES `Agenda` (`idAgenda`, `idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Evento`
--

LOCK TABLES `Evento` WRITE;
/*!40000 ALTER TABLE `Evento` DISABLE KEYS */;
INSERT INTO `Evento` VALUES (1,'2019-02-03','00:00:00','01:00:00',1,1,'Evento1',5),(2,'2019-02-03','01:00:00','02:00:00',1,1,'Evento1',5),(3,'2019-02-04','02:00:00','03:00:00',1,1,'Evento2',5),(4,'2019-02-05','03:00:00','04:00:00',2,1,'Evento3',4),(5,'2019-02-06','04:00:00','05:00:00',2,1,'Evento4',0),(7,'2019-02-07','05:00:00','06:00:00',3,2,'Evento5',5),(8,'2019-02-08','06:00:00','07:00:00',3,2,'Evento6',5),(9,'2019-02-10','07:00:00','08:00:00',4,2,'Evento7',5),(10,'2019-02-09','08:00:00','09:00:00',4,2,'Evento8',5),(11,'2019-02-04','02:00:00','03:00:00',1,1,'EventoX',0);
/*!40000 ALTER TABLE `Evento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Inscricao`
--

DROP TABLE IF EXISTS `Inscricao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Inscricao` (
  `idInscricao` varchar(45) NOT NULL,
  `idAgenda` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `idEvento` int(11) NOT NULL,
  PRIMARY KEY (`idAgenda`,`idUsuario`,`idInscricao`),
  KEY `fk_Inscricao_Evento1_idx` (`idEvento`),
  CONSTRAINT `fk_Inscricao_Agenda1` FOREIGN KEY (`idAgenda`, `idUsuario`) REFERENCES `Agenda` (`idAgenda`, `idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Inscricao_Evento1` FOREIGN KEY (`idEvento`) REFERENCES `Evento` (`idEvento`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Inscricao`
--

LOCK TABLES `Inscricao` WRITE;
/*!40000 ALTER TABLE `Inscricao` DISABLE KEYS */;
INSERT INTO `Inscricao` VALUES ('Marcio',1,1,1),('Marcio',2,1,4),('Gabriel',3,2,7),('Gabriel',4,2,9),('Joao',1,1,11);
/*!40000 ALTER TABLE `Inscricao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) NOT NULL,
  `senha` varchar(255) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `nome_UNIQUE` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (1,'Roque','pbkdf2:sha256:150000$0GNoYVE4$3ba1ea9d4d9c4b38b7d785b76158196428bee67a48298912e2497c88bc0426fc'),(2,'Joao','pbkdf2:sha256:150000$Ns1lx1gq$0ece343180e1fc8f527d60fce86b52a94978247f4fef8a7b0d09112deb39dfc0'),(3,'Lucas','pbkdf2:sha256:150000$SZupjeGT$a48adb870c5614a1ce81a99904e2c3512084699485503cb4bb7c8c99f844a649');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-15 21:32:42
