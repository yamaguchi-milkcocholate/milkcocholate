-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: 2018 年 11 月 04 日 05:02
-- サーバのバージョン： 10.3.10-MariaDB-1:10.3.10+maria~bionic
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `milkcocholate`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `fitness_functions`
--

CREATE TABLE `fitness_functions` (
  `id` int(11) NOT NULL,
  `name` char(50) COLLATE utf8_bin NOT NULL,
  `spec` char(100) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- テーブルのデータのダンプ `fitness_functions`
--

INSERT INTO `fitness_functions` (`id`, `name`, `spec`) VALUES
(1, 'simple_macd_params', NULL),
(2, 'bollinger_band_linear_end', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fitness_functions`
--
ALTER TABLE `fitness_functions`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fitness_functions`
--
ALTER TABLE `fitness_functions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
