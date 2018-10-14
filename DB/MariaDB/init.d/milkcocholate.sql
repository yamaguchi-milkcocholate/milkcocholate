-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: 2018 年 10 月 14 日 03:38
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
  `situation` varbinary(1000) NOT NULL,
  `mutation_rate` int(11) NOT NULL,
  `cross_rate` int(11) NOT NULL,
  `population` int(11) NOT NULL,
  `elite_num` int(11) NOT NULL,
  `start_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `execute_time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- テーブルの構造 `fitness_functions`
--

CREATE TABLE `fitness_functions` (
  `id` int(11) NOT NULL,
  `name` char(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `spec` char(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- テーブルの構造 `genetic_algorithms`
--

CREATE TABLE `genetic_algorithms` (
  `id` int(11) NOT NULL,
  `name` char(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `spec` char(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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

-- --------------------------------------------------------

--
-- テーブルの構造 `test`
--

CREATE TABLE `test` (
  `id` int(11) NOT NULL,
  `name` char(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `object` varbinary(1000) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- テーブルのデータのダンプ `test`
--

INSERT INTO `test` (`id`, `name`, `object`, `time`) VALUES
(1, 'test_1', 0x8003636d6f64756c65732e736974756174696f6e2e736974756174696f6e0a536974756174696f6e0a7100298171017d71022858140000005f6669746e6573735f66756e6374696f6e5f696471034de80358080000005f67656e6f6d657371045d710528580a00000073686f72745f7465726d710658090000006c6f6e675f7465726d710758060000007369676e616c710865580e0000005f67656e6f6d655f72616e67657371097d710a2868064b014b3286710b68074b324b6486710c68084b014b3286710d7575622e, '2018-10-14 03:36:13'),
(2, 'test_2', 0x8003636d6f64756c65732e736974756174696f6e2e736974756174696f6e0a536974756174696f6e0a7100298171017d71022858140000005f6669746e6573735f66756e6374696f6e5f696471034de80358080000005f67656e6f6d657371045d710528580a00000073686f72745f7465726d710658090000006c6f6e675f7465726d710758060000007369676e616c710865580e0000005f67656e6f6d655f72616e67657371097d710a2868064b014b3286710b68074b324b6486710c68084b014b3286710d7575622e, '2018-10-14 03:36:13');

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
-- Indexes for table `test`
--
ALTER TABLE `test`
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `logs`
--
ALTER TABLE `logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `test`
--
ALTER TABLE `test`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
