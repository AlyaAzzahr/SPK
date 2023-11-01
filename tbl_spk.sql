-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 01, 2023 at 02:19 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uts_spk`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_spk`
--

CREATE TABLE `tbl_spk` (
  `brand_cushion` varchar(50) NOT NULL,
  `reputasi_brand` varchar(100) NOT NULL,
  `kandungan_spf` varchar(10) NOT NULL,
  `ketahanan` varchar(10) NOT NULL,
  `isi_kemasan` varchar(10) NOT NULL,
  `harga` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_spk`
--

INSERT INTO `tbl_spk` (`brand_cushion`, `reputasi_brand`, `kandungan_spf`, `ketahanan`, `isi_kemasan`, `harga`) VALUES
('Rose All Day', 'Terkenal', '40 PA++', '8 Jam', '15 gr', 123000),
('Somethinc', 'Terkenal', '35 PA++', '12 Jam', '15 gr', 161000),
('Make Over', 'Sangat Terkenal', '50 PA++', '24 Jam', '15 gr', 157500),
('Barenbliss', 'Cukup Terkenal', '45 PA++', '24 Jam', '12 gr', 89000),
('Skintific', 'Sangat Terkenal', '35 PA++', '12 Jam', '11 gr', 115000),
('Instaperfect', 'Cukup Terkenal', '33 PA++', '12 Jam', '15 gr', 86500),
('Salsa', 'Kurang Terkenal', '30 PA++', '12 Jam', '20 gr', 47500),
('Luxcrime', 'Terkenal', '50 PA++', '18 Jam', '15 gr', 129000),
('Esqa', 'Cukup Terkenal', '50 PA++', '12 Jam', '15 gr', 139000),
('Kaila Beauty', 'Lumayan Terkenal', '50 PA++', '12 Jam', '13 gr', 89000);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
