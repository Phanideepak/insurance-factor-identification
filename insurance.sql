create database insurance;

use insurance;


CREATE TABLE users (
  `id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  `role` enum('ROLE_ADMIN','ROLE_CUSTOMER','ROLE_AGENT') NOT NULL DEFAULT 'ROLE_ADMIN',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
);

CREATE TABLE insurance_plan(
   id int NOT NULL AUTO_INCREMENT,
   insurance_name VARCHAR(255) not null unique,
   insurance_type enum('LIFE', 'CHILD', 'RETIREMENT', 'SAVINGS', 'INVESTMENT') NOT NULL,
   description text not null,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
);

CREATE TABLE life_insurance_details(
   id int NOT NULL AUTO_INCREMENT,
   insurance_id int not null,
   plan_code varchar(100) not null unique,
   basic_sum_assured int not null,
   duration int not null,
   interest decimal not null,
   interest_type enum('SIMPLE', 'COMPOUND'),
   `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`),
   FOREIGN KEY (`insurance_id`) REFERENCES insurance.insurance_plan(id),  
)

CREATE TABLE insurance.customers(
   id int NOT NULL AUTO_INCREMENT,
   firstname varchar(100) not null,
   lastname VARCHAR(100) not null,
   healthy enum('EXCELLENT','GOOD','FAIR','POOR') not null,
   life_style enum('SEDENTARY','MODERATELY_ACTIVE', 'ACTIVE') NOT NULL,
   occupation varchar(100) not null,
   occupation_type enum('HIGH_RISK','MEDIUM_RISK', 'LOW_RISK') NOT NULL,
   city varchar(100) not null,
   pincode varchar(10) not null,
   lat varchar(20) not null,
   lng varchar(20) not null,
   first_line varchar(20) not null,
   last_line varchar(20) null,
   land_mark varchar(20) not null,
   email varchar(100) not null unique,
   phone varchar(20) not null unique,
   is_deleted tinyint(1) NOT NULL DEFAULT '0',
   created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (id)    
);