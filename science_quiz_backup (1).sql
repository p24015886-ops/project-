- MySQL dump 10.13  Distrib 9.6.0, for macos26.2 (arm64)
--
-- Host: localhost    Database: science_quiz
-- ------------------------------------------------------
-- Server version	9.6.0

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '5c78d8e0-0f1a-11f1-bbdc-264d1068d807:1-91';

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `workshop_id` int DEFAULT NULL,
  `question_text` text NOT NULL,
  `question_image` varchar(500) DEFAULT NULL,
  `option_a` varchar(255) NOT NULL,
  `option_b` varchar(255) NOT NULL,
  `option_c` varchar(255) NOT NULL,
  `option_d` varchar(255) NOT NULL,
  `correct_answer` char(1) NOT NULL,
  `difficulty` varchar(20) DEFAULT 'medium',
  `level` varchar(50) NOT NULL DEFAULT 'upper_primary',
  `points` int DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `workshop_id` (`workshop_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`workshop_id`) REFERENCES `workshops` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,1,'What is the center of our Solar System?',NULL,'Earth','Moon','Sun','Mars','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(2,1,'Which planet is known as the Red Planet?',NULL,'Venus','Mars','Jupiter','Saturn','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(3,1,'Water freezes at what temperature (°C)?',NULL,'0','10','50','100','A','medium','upper_primary',1,'2026-03-01 04:45:14'),(4,1,'Which gas do plants use for photosynthesis?',NULL,'Oxygen','Nitrogen','Carbon Dioxide','Hydrogen','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(5,1,'What force pulls objects toward Earth?',NULL,'Magnetism','Friction','Gravity','Electricity','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(6,1,'Which organ pumps blood in the human body?',NULL,'Brain','Heart','Lungs','Kidney','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(7,1,'Which planet has the most rings?',NULL,'Earth','Mars','Saturn','Mercury','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(8,1,'What is H2O commonly known as?',NULL,'Oxygen','Salt','Hydrogen','Water','D','medium','upper_primary',1,'2026-03-01 04:45:14'),(9,1,'How many legs does an insect have?',NULL,'4','6','8','10','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(10,1,'Which planet is closest to the Sun?',NULL,'Mercury','Venus','Earth','Mars','A','medium','upper_primary',1,'2026-03-01 04:45:14'),(11,1,'Which vitamin do we get from sunlight?',NULL,'Vitamin A','Vitamin B','Vitamin C','Vitamin D','D','medium','upper_primary',1,'2026-03-01 04:45:14'),(12,1,'What part of the plant conducts photosynthesis?',NULL,'Root','Stem','Leaf','Flower','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(13,1,'Which gas do humans breathe in?',NULL,'Oxygen','Carbon Dioxide','Nitrogen','Helium','A','medium','upper_primary',1,'2026-03-01 04:45:14'),(14,1,'Which planet is the largest?',NULL,'Earth','Mars','Jupiter','Neptune','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(15,1,'Which animal is known as the King of the Jungle?',NULL,'Tiger','Lion','Elephant','Leopard','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(16,1,'What is the boiling point of water (°C)?',NULL,'50','90','100','120','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(17,1,'Which instrument measures temperature?',NULL,'Barometer','Thermometer','Hygrometer','Altimeter','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(18,1,'Which planet is known for its Great Red Spot?',NULL,'Saturn','Jupiter','Mars','Neptune','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(19,1,'Which blood cells fight infection?',NULL,'Red blood cells','White blood cells','Platelets','Plasma','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(20,1,'What do bees collect from flowers?',NULL,'Water','Pollen','Sand','Leaves','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(21,1,'Which is the hardest natural substance?',NULL,'Iron','Gold','Diamond','Silver','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(22,1,'Which planet is known as Earth\'s twin?',NULL,'Mars','Venus','Jupiter','Mercury','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(23,1,'What do we call animals that eat only plants?',NULL,'Carnivores','Herbivores','Omnivores','Insectivores','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(24,1,'Which part of the body helps us think?',NULL,'Heart','Brain','Lungs','Liver','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(25,1,'Which planet is known for its beautiful rings?',NULL,'Mars','Earth','Saturn','Venus','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(26,1,'What is the main source of energy for Earth?',NULL,'Wind','Moon','Sun','Water','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(27,1,'Which organ helps us breathe?',NULL,'Liver','Lungs','Kidney','Stomach','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(28,1,'Which state of matter has no fixed shape or volume?',NULL,'Solid','Liquid','Gas','Plasma','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(29,1,'What do we call molten rock from a volcano?',NULL,'Magma','Lava','Coal','Ash','B','medium','upper_primary',1,'2026-03-01 04:45:14'),(30,1,'Which planet takes the longest time to orbit the Sun?',NULL,'Earth','Mars','Neptune','Venus','C','medium','upper_primary',1,'2026-03-01 04:45:14'),(31,2,'What is the center of our Solar System?','','Earth','Moon','Sun','Mars','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(32,2,'Which planet is known as the Red Planet?','','Venus','Mars','Jupiter','Saturn','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(33,2,'Water freezes at what temperature (°C)?','','0','10','50','100','A','medium','upper_primary',1,'2026-03-02 13:25:20'),(34,2,'Which gas do plants use for photosynthesis?','','Oxygen','Nitrogen','Carbon Dioxide','Hydrogen','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(35,2,'What force pulls objects toward Earth?','','Magnetism','Friction','Gravity','Electricity','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(36,2,'Which organ pumps blood in the human body?','','Brain','Heart','Lungs','Kidney','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(37,2,'Which planet has the most rings?','','Earth','Mars','Saturn','Mercury','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(38,2,'What is H2O commonly known as?','','Oxygen','Salt','Hydrogen','Water','D','medium','upper_primary',1,'2026-03-02 13:25:20'),(39,2,'How many legs does an insect have?','','4','6','8','10','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(40,2,'Which planet is closest to the Sun?','','Mercury','Venus','Earth','Mars','A','medium','upper_primary',1,'2026-03-02 13:25:20'),(41,2,'Which vitamin do we get from sunlight?','','Vitamin A','Vitamin B','Vitamin C','Vitamin D','D','medium','upper_primary',1,'2026-03-02 13:25:20'),(42,2,'What part of the plant conducts photosynthesis?','','Root','Stem','Leaf','Flower','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(43,2,'Which gas do humans breathe in?','','Oxygen','Carbon Dioxide','Nitrogen','Helium','A','medium','upper_primary',1,'2026-03-02 13:25:20'),(44,2,'Which planet is the largest?','','Earth','Mars','Jupiter','Neptune','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(45,2,'Which animal is known as the King of the Jungle?','','Tiger','Lion','Elephant','Leopard','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(46,2,'What is the boiling point of water (°C)?','','50','90','100','120','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(47,2,'Which instrument measures temperature?','','Barometer','Thermometer','Hygrometer','Altimeter','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(48,2,'Which planet is known for its Great Red Spot?','','Saturn','Jupiter','Mars','Neptune','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(49,2,'Which blood cells fight infection?','','Red blood cells','White blood cells','Platelets','Plasma','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(50,2,'What do bees collect from flowers?','','Water','Pollen','Sand','Leaves','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(51,2,'Which is the hardest natural substance?','','Iron','Gold','Diamond','Silver','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(52,2,'Which planet is known as Earth\'s twin?','','Mars','Venus','Jupiter','Mercury','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(53,2,'What do we call animals that eat only plants?','','Carnivores','Herbivores','Omnivores','Insectivores','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(54,2,'Which part of the body helps us think?','','Heart','Brain','Lungs','Liver','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(55,2,'Which planet is known for its beautiful rings?','','Mars','Earth','Saturn','Venus','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(56,2,'What is the main source of energy for Earth?','','Wind','Moon','Sun','Water','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(57,2,'Which organ helps us breathe?','','Liver','Lungs','Kidney','Stomach','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(58,2,'Which state of matter has no fixed shape or volume?','','Solid','Liquid','Gas','Plasma','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(59,2,'What do we call molten rock from a volcano?','','Magma','Lava','Coal','Ash','B','medium','upper_primary',1,'2026-03-02 13:25:20'),(60,2,'Which planet takes the longest time to orbit the Sun?','','Earth','Mars','Neptune','Venus','C','medium','upper_primary',1,'2026-03-02 13:25:20'),(91,17,'Which body part helps a penguin swim strongly in icy water?',NULL,'Thick feathers','Flippers','Webbed feet','Gills','B','medium','upper_primary',1,'2026-03-02 15:09:41'),(92,17,'What is the primary purpose of a cactus\'s thick stem?',NULL,'To attract insects','To protect against predators','To store water','To reduce water loss','C','medium','upper_primary',1,'2026-03-02 15:09:41'),(93,17,'Which feature helps a fish breathe underwater?',NULL,'Fins','Scales','Gills','Webbed feet','C','medium','upper_primary',1,'2026-03-02 15:09:41'),(94,17,'Plants grow differently depending on which environmental factors?',NULL,'Sunlight, water, and soil','Wind and noise','Gravity and moonlight','Altitude and oxygen levels','A','medium','upper_primary',1,'2026-03-02 15:09:41'),(95,17,'What help penguins walk effectively on top of ice?',NULL,'Fins','Scales','Thick feathers','Webbed feet','D','medium','upper_primary',1,'2026-03-02 15:09:41'),(96,17,'What do cacti have instead of leaves to reduce water loss?',NULL,'Flowers','Spines','Flippers','Thick feathers','B','medium','upper_primary',1,'2026-03-02 15:09:41'),(97,18,'Which body part helps a penguin swim strongly in icy water?','','Thick feathers','Flippers','Webbed feet','Gills','B','medium','upper_primary',1,'2026-03-02 15:25:15'),(98,18,'What is the primary purpose of a cactus\'s thick stem?','','To attract insects','To protect against predators','To store water','To reduce water loss','C','medium','upper_primary',1,'2026-03-02 15:25:15'),(99,18,'Which feature helps a fish breathe underwater?','','Fins','Scales','Gills','Webbed feet','C','medium','upper_primary',1,'2026-03-02 15:25:15'),(100,18,'Plants grow differently depending on which environmental factors?','','Sunlight, water, and soil','Wind and noise','Gravity and moonlight','Altitude and oxygen levels','A','medium','upper_primary',1,'2026-03-02 15:25:15'),(101,18,'What help penguins walk effectively on top of ice?','','Fins','Scales','Thick feathers','Webbed feet','D','medium','upper_primary',1,'2026-03-02 15:25:15'),(102,18,'What do cacti have instead of leaves to reduce water loss?','','Flowers','Spines','Flippers','Thick feathers','B','medium','upper_primary',1,'2026-03-02 15:25:15');
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_attempts`
--

DROP TABLE IF EXISTS `quiz_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_attempts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `workshop_id` int NOT NULL,
  `score` int DEFAULT '0',
  `total_questions` int DEFAULT '0',
  `percentage` decimal(5,2) DEFAULT NULL,
  `passed` tinyint(1) DEFAULT '0',
  `attempt_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `workshop_id` (`workshop_id`),
  CONSTRAINT `quiz_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `quiz_attempts_ibfk_2` FOREIGN KEY (`workshop_id`) REFERENCES `workshops` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_attempts`
--

LOCK TABLES `quiz_attempts` WRITE;
/*!40000 ALTER TABLE `quiz_attempts` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_attempts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'student',
  `level` varchar(50) DEFAULT 'lower_primary',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workshops`
--

DROP TABLE IF EXISTS `workshops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workshops` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `description` text,
  `category` varchar(100) NOT NULL,
  `target_level` varchar(100) DEFAULT 'both',
  `is_game` tinyint(1) DEFAULT '0',
  `time_limit` int DEFAULT '0',
  `duration_minutes` int DEFAULT '60',
  `max_participants` int DEFAULT '20',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workshops`
--

LOCK TABLES `workshops` WRITE;
/*!40000 ALTER TABLE `workshops` DISABLE KEYS */;
INSERT INTO `workshops` VALUES (1,'Workshop 1','Physics is great','physics','upper_primary',0,0,60,20,'2026-03-01 04:45:14'),(2,'hello','Hello','chemistry','upper_primary',1,300,60,20,'2026-03-02 13:25:20'),(3,'Herbarium',NULL,'biology','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(4,'Terrarium',NULL,'biology','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(5,'Bug Busters !',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(6,'DIY Natural Lipbalm',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(7,'DIY Soap',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(8,'Glow Slime',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(9,'Natural Moisturiser 101',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(10,'Natural Moisturizer (pH Testing Result)',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(11,'Natural Moisturizer (Universal Indicator)',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(12,'Perfume Atelier',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(13,'Soapy Turtle',NULL,'chemistry','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(14,'Blast Off !',NULL,'physics','upper_primary',0,0,60,20,'2026-03-02 14:36:09'),(15,'Mini Piano',NULL,'technology','upper_primary',0,0,60,20,'2026-03-02 14:36:11'),(17,'alien architecture','study explore','physics','upper_primary',0,0,60,20,'2026-03-02 15:09:41'),(18,'Hello world','doing','physics','upper_primary',1,300,60,20,'2026-03-02 15:25:15');
/*!40000 ALTER TABLE `workshops` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-03 11:02:30
