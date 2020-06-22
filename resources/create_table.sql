-- 0. create schema
CREATE SCHEMA 'security-trading';

-- 1. account_type_code
CREATE TABLE `account_type_code` (
  `code` varchar(15) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB;

-- 2. transaction_type_code
CREATE TABLE `transaction_type_code` (
  `code` varchar(1) NOT NULL,
  `description` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB;

-- 3. security_type_code
CREATE TABLE `security_type_code` (
  `code` varchar(20) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB;

-- 4. yes_no_code
CREATE TABLE `yes_no_code` (
  `code` varchar(1) NOT NULL,
  `description` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB;

-- 5. account_master
CREATE TABLE `account_master` (
  `account_id` int NOT NULL,
  `account_type` varchar(15) DEFAULT NULL,
  `open_date` datetime DEFAULT NULL,
  `is_active` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`account_id`),
  KEY `account_type_idx` (`account_type`),
  CONSTRAINT `account_type` FOREIGN KEY (`account_type`) REFERENCES `account_type_code` (`code`),
  CONSTRAINT `is_active_account_master` FOREIGN KEY (`is_active`) REFERENCES `yes_no_code` (`code`)
) ENGINE=InnoDB;

-- 6. account_balance
CREATE TABLE `account_balance` (
  `account_id` int DEFAULT NULL,
  `balance_amount` decimal(10,4) DEFAULT NULL,  
  KEY `account_id_idx` (`account_id`),
  CONSTRAINT `account_id` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`account_id`)
) ENGINE=InnoDB;

-- 7. security_holding
CREATE TABLE `security_holding` (
  `account_id` int NOT NULL,
  `security_symbol` varchar(10) NOT NULL,
  `security_type_code` varchar(20) DEFAULT NULL,
  `holding_qty` int DEFAULT NULL,
  `purchase_price` decimal(10,4) DEFAULT NULL,
  PRIMARY KEY (`account_id`,`security_symbol`),
  KEY `security_symbol_holding_idx` (`security_symbol`),
  CONSTRAINT `account_id_holding` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`account_id`),
  CONSTRAINT `security_type_code` FOREIGN KEY (`security_type_code`) REFERENCES `security_type_code` (`code`)
) ENGINE=InnoDB;

-- 8. user_master
CREATE TABLE `user_master` (
  `user_id` varchar(20) NOT NULL,
  `name` varchar(45) DEFAULT NULL,  
  `is_active` varchar(1) DEFAULT NULL,
  `profile_create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `is_active_user_master` FOREIGN KEY (`is_active`) REFERENCES `yes_no_code` (`code`)
) ENGINE=InnoDB;

-- 9. user_account
CREATE TABLE `user_account` (
  `user_id` varchar(20) NOT NULL,
  `account_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `account_id_idx` (`account_id`),
  CONSTRAINT `user_id_user_account` FOREIGN KEY (`user_id`) REFERENCES `user_master` (`user_id`),
  CONSTRAINT `account_id_user_account` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`account_id`)  
) ENGINE=InnoDB;

-- 10. trade_activity
CREATE TABLE `trade_activity` (
  `account_id` int DEFAULT NULL,
  `security_symbol` varchar(10) NOT NULL,
  `transaction_qty` int NOT NULL,
  `transaction_price` decimal(10,4) NOT NULL,
  `transaction_type_code` varchar(1) NOT NULL,
  `transaction_date` datetime NOT NULL,
  KEY `transaction_type_code_idx` (`transaction_type_code`),
  KEY `security_symbol_tran_log_idx` (`security_symbol`),
  KEY `account_id_tran_log` (`account_id`),
  CONSTRAINT `account_id_tran_log` FOREIGN KEY (`account_id`) REFERENCES `account_master` (`account_id`),  
  CONSTRAINT `transaction_type_code` FOREIGN KEY (`transaction_type_code`) REFERENCES `transaction_type_code` (`code`)
) ENGINE=InnoDB;