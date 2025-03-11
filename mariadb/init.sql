SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


--
-- Base de données : `Logs_fw`
--
DROP DATABASE IF EXISTS `Logs_fw`;
CREATE DATABASE IF NOT EXISTS `Logs_fw` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `Logs_fw`;

-- --------------------------------------------------------

--
-- Structure de la table `FW`
--

CREATE TABLE `FW` (
  `date` datetime NOT NULL,
  `ipsrc` text NOT NULL,
  `ipdst` text NOT NULL,
  `proto` text NOT NULL,
  `portsrc` int NOT NULL,
  `portdst` int NOT NULL,
  `regle` int NOT NULL,
  `action` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;
