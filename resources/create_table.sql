
-- 1. account_type_code
CREATE TABLE `account_type_code` (
  `code` varchar(20) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. transaction_type_code
CREATE TABLE `transaction_type_code` (
  `code` varchar(1) NOT NULL,
  `description` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. account_master
CREATE TABLE `account_master` (
  `id` int NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `open_date` datetime DEFAULT NULL,
  `is_active` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `type_idx` (`type`),
  CONSTRAINT `type` FOREIGN KEY (`type`) REFERENCES `account_type_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. account_balance
CREATE TABLE `account_balance` (
  `account_id` int NOT NULL,
  `balance_amount` decimal(10,4) DEFAULT NULL,
  `as_of_date` datetime DEFAULT NULL,
  KEY `account_id_idx` (`account_id`),
  CONSTRAINT `id` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. stock_master
CREATE TABLE `stock_master` (
  `symbol` varchar(10) NOT NULL,
  `name` varchar(45) DEFAULT NULL,  
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. stock_holding
CREATE TABLE `stock_holding` (
  `account_id` int NOT NULL,
  `security_symbol` varchar(10) NOT NULL,
  `holding_qty` int DEFAULT NULL,
  `purchase_price` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`account_id`,`stock_symbol`),
  KEY `stock_symbol_holding_idx` (`stock_symbol`),
  CONSTRAINT `account_id_holding` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`id`),
  CONSTRAINT `stock_symbol_holding` FOREIGN KEY (`stock_symbol`) REFERENCES `stock_master` (`stock_symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. user_master
CREATE TABLE `user_master` (
  `id` varchar(20) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `ssn` varchar(15) DEFAULT NULL,
  `is_active` varchar(1) DEFAULT NULL,
  `profile_create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. user_account
CREATE TABLE `user_account` (
  `user_id` varchar(20) NOT NULL,
  `account_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `account_id_idx` (`account_id`),
  CONSTRAINT `account_id` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user_master` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. trade_activity
CREATE TABLE `trade_activity` (
  `account_id` int DEFAULT NULL,
  `stock_symbol` varchar(10) NOT NULL,
  `transaction_qty` int NOT NULL,
  `transaction_price` decimal(10,4) NOT NULL,
  `transaction_type_code` varchar(1) NOT NULL,
  `transaction_date` datetime NOT NULL,
  KEY `transaction_type_code_idx` (`transaction_type_code`),
  KEY `stock_symbol_tran_log_idx` (`stock_symbol`),
  KEY `account_id_tran_log` (`account_id`),
  CONSTRAINT `account_id_tran_log` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`id`),
  CONSTRAINT `stock_symbol_tran_log` FOREIGN KEY (`stock_symbol`) REFERENCES `stock_master` (`stock_symbol`),
  CONSTRAINT `transaction_type_code` FOREIGN KEY (`transaction_type_code`) REFERENCES `transaction_type_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;