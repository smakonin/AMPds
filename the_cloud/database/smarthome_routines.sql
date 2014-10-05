CREATE DATABASE  IF NOT EXISTS `smarthome` /*!40100 DEFAULT CHARACTER SET ascii */;
USE `smarthome`;
-- MySQL dump 10.13  Distrib 5.6.13, for osx10.6 (i386)
--
-- Host: localhost    Database: smarthome
-- ------------------------------------------------------
-- Server version	5.1.61-0ubuntu0.10.10.1

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
-- Dumping routines for database 'smarthome'
--
/*!50003 DROP PROCEDURE IF EXISTS `ihd_agg` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ihd_agg`()
BEGIN

PREPARE stmt1 FROM  'SELECT AVG(a.inst) FROM (SELECT inst FROM log_minutely WHERE inst >= 0 AND home_id = ''MAK'' AND meter_id = ''MHE'' ORDER BY inst LIMIT ?, ?) a into @median;';
SET @didx = (SELECT COUNT(inst)/2 FROM log_minutely WHERE inst >= 0 AND home_id = 'MAK' AND meter_id = 'MHE');
SET @idx = CEILING(@didx);
SET @lim = IF(@didx = @idx, 2, 1);
EXECUTE stmt1 USING @idx, @lim;
-- SELECT @didx, @idx, @lim, @median;
DEALLOCATE PREPARE stmt1;

PREPARE stmt2 FROM  'SELECT AVG(a.inst) FROM (SELECT inst FROM log_minutely WHERE inst < ? AND home_id = ''MAK'' AND meter_id = ''MHE'' ORDER BY inst LIMIT ?, ?) a into @q1;';
SET @didx = (SELECT COUNT(inst)/2 FROM log_minutely WHERE inst < @median AND home_id = 'MAK' AND meter_id = 'MHE');
SET @idx = CEILING(@didx);
SET @lim = IF(@didx = @idx, 2, 1);
EXECUTE stmt2 USING @median, @idx, @lim;
-- SELECT @didx, @idx, @lim, @median, @q1;
DEALLOCATE PREPARE stmt2;

PREPARE stmt3 FROM  'SELECT AVG(a.inst) FROM (SELECT inst FROM log_minutely WHERE inst > ? AND home_id = ''MAK'' AND meter_id = ''MHE'' ORDER BY inst LIMIT ?, ?) a into @q3;';
SET @didx = (SELECT COUNT(inst)/2 FROM log_minutely WHERE inst > @median AND home_id = 'MAK' AND meter_id = 'MHE');
SET @idx = CEILING(@didx);
SET @lim = IF(@didx = @idx, 2, 1);
EXECUTE stmt3 USING @median, @idx, @lim;
-- SELECT @didx, @idx, @lim, @median, @q3;
DEALLOCATE PREPARE stmt3;

SET @iqr = 1.5 * (@q3 - @q1);
SET @llim = @q1 - @iqr;
SET @ulim = @q3 + @iqr;
SET @onpeak = IF(CURTIME() BETWEEN '17:00' AND '19:00', 1, 0);
SET @watts = (SELECT inst FROM log_minutely WHERE inst >= 0 AND home_id = 'MAK' AND meter_id = 'MHE' ORDER BY year DESC, jday DESC, hour DESC, minute DESC LIMIT 0, 1);

UPDATE calc_ihd_agg SET updated_dt = now(), median = @median, q1 = @q1, q3 = @q3, iqr = @iqr, lower = @llim, upper = @ulim, onpeak = @onpeak, watts = @watts WHERE id = 1; 

SELECT @median as median, @q1 as q1, @q3 as q3, @iqr as iqr, @llim as lower, @ulim as upper, @onpeak AS onpeak, @watts AS watts;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-05  9:37:36
