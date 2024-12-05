create database ems;

use ems;


CREATE TABLE users (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `role` enum('ROLE_ADMIN','ROLE_HR','ROLE_FINANCE','ROLE_EMPLOYEE') NOT NULL DEFAULT 'ROLE_ADMIN',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
);


CREATE TABLE `department` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `is_approved` tinyint(1) NOT NULL DEFAULT '0',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `approved_by` int DEFAULT NULL,
  `approved_at` timestamp NULL DEFAULT NULL,
  `deleted_by` int DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `description` (`description`)
);




-- ems.address definition

CREATE TABLE `address` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_line` varchar(255) NOT NULL,
  `second_line` varchar(255) DEFAULT NULL,
  `land_mark` varchar(255) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `city` varchar(100) NOT NULL,
  `pincode` varchar(20) NOT NULL,
  `state` varchar(20) NOT NULL,
  `is_primary` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `eid` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UC_FIRST_SECOND_CITY` (`first_line`,`second_line`,`city`),
  KEY `address_employee_FK` (`eid`),
  CONSTRAINT `address_employee_FK` FOREIGN KEY (`eid`) REFERENCES `employee` (`id`)
);


CREATE TABLE ems.employee (
  `id` int NOT NULL AUTO_INCREMENT,
   `eid` varchar(20) NOT NULL UNIQUE, 
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `contact` varchar(20) NOT NULL,
  `is_approved` tinyint(1) NOT NULL DEFAULT '0',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `approved_by` int,
  `approved_at` timestamp NULL,
  `deleted_by` int,
  `deleted_at` timestamp NULL,
  `dept_id` int NOT NULL,
  `address_id` int NULL,
  `office_mail` varchar(255) NULL,
  `designation` varchar(255) not null,
  `created_by` int NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`dept_id`) REFERENCES ems.department(id),
  FOREIGN KEY(`address_id`) REFERENCES ems.address(id)
);