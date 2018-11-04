-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: 2018 年 11 月 04 日 05:17
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
-- テーブルの構造 `crossovers`
--

CREATE TABLE `crossovers` (
  `id` int(11) NOT NULL,
  `name` char(50) COLLATE utf8_bin NOT NULL,
  `spec` char(100) COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- テーブルのデータのダンプ `crossovers`
--

INSERT INTO `crossovers` (`id`, `name`, `spec`) VALUES
(1, 'one_point', NULL),
(2, 'uniform', NULL);

-- --------------------------------------------------------

--
-- テーブルの構造 `experiments`
--

CREATE TABLE `experiments` (
  `id` int(11) NOT NULL,
  `crossover_id` int(11) NOT NULL,
  `fitness_function_id` int(11) NOT NULL,
  `situation` blob NOT NULL,
  `hyper_parameter` blob DEFAULT NULL,
  `mutation_rate` int(11) NOT NULL,
  `cross_rate` int(11) NOT NULL,
  `population` int(11) NOT NULL,
  `elite_num` int(11) NOT NULL,
  `start_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `execute_time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- テーブルの構造 `experiment_logs`
--

CREATE TABLE `experiment_logs` (
  `id` int(11) NOT NULL,
  `population_id` int(11) NOT NULL,
  `position` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `logged_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

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

-- --------------------------------------------------------

--
-- テーブルの構造 `populations`
--

CREATE TABLE `populations` (
  `id` int(11) NOT NULL,
  `experiment_id` int(11) NOT NULL,
  `generation_number` int(11) NOT NULL,
  `genome` blob NOT NULL,
  `fitness` blob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- テーブルの構造 `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` char(50) COLLATE utf8_bin NOT NULL,
  `object` varbinary(1000) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin ROW_FORMAT=COMPACT;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `crossovers`
--
ALTER TABLE `crossovers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experiments`
--
ALTER TABLE `experiments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experiment_logs`
--
ALTER TABLE `experiment_logs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fitness_functions`
--
ALTER TABLE `fitness_functions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `populations`
--
ALTER TABLE `populations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `crossovers`
--
ALTER TABLE `crossovers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `experiments`
--
ALTER TABLE `experiments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `experiment_logs`
--
ALTER TABLE `experiment_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fitness_functions`
--
ALTER TABLE `fitness_functions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `populations`
--
ALTER TABLE `populations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
