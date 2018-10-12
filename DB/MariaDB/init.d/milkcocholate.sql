-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: 2018 年 10 月 12 日 08:02
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
-- テーブルの構造 `experiments`
--

CREATE TABLE `experiments` (
  `id` int(11) NOT NULL,
  `genetic_algorithm_id` int(11) NOT NULL,
  `fitness_function_id` int(11) NOT NULL,
  `situation` char(200) NOT NULL,
  `mutation_rate` int(11) NOT NULL,
  `cross_rate` int(11) NOT NULL,
  `population` int(11) NOT NULL,
  `elite_num` int(11) NOT NULL,
  `start_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `execute_time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- テーブルの構造 `fitness_functions`
--

CREATE TABLE `fitness_functions` (
  `id` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `spec` char(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- テーブルの構造 `genetic_algorithms`
--

CREATE TABLE `genetic_algorithms` (
  `id` int(11) NOT NULL,
  `name` char(50) NOT NULL,
  `spec` char(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- テーブルのデータのダンプ `genetic_algorithms`
--

INSERT INTO `genetic_algorithms` (`id`, `name`, `spec`) VALUES
(10, 'test', 'test'),
(12, 'test', 'test'),
(13, 'test', 'test'),
(14, 'test', 'test');

-- --------------------------------------------------------

--
-- テーブルの構造 `logs`
--

CREATE TABLE `logs` (
  `id` int(11) NOT NULL,
  `experiment_id` int(11) NOT NULL,
  `position` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `loged_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `experiments`
--
ALTER TABLE `experiments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fitness_functions`
--
ALTER TABLE `fitness_functions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `genetic_algorithms`
--
ALTER TABLE `genetic_algorithms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `experiments`
--
ALTER TABLE `experiments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fitness_functions`
--
ALTER TABLE `fitness_functions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `genetic_algorithms`
--
ALTER TABLE `genetic_algorithms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
