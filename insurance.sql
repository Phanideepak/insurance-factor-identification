create database insurance;

use insurance;


CREATE TABLE insurance.users (
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

CREATE TABLE insurance.insurance_plan(
   id int NOT NULL AUTO_INCREMENT,
   insurance_name VARCHAR(255) not null unique,
   insurance_type enum('LIFE', 'CHILD', 'RETIREMENT', 'SAVINGS', 'INVESTMENT') NOT NULL,
   description text not null,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`)
);

CREATE TABLE insurance.life_insurance_details(
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
   FOREIGN KEY (`insurance_id`) REFERENCES insurance.insurance_plan(id) 
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


CREATE TABLE insurance.agents(
   id int NOT NULL AUTO_INCREMENT,
   firstname varchar(100) not null,
   lastname VARCHAR(100) not null,
   email varchar(100) not null unique,
   phone varchar(20) not null unique,
   created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (id)    
);

CREATE TABLE insurance.orders(
   id int NOT NULL AUTO_INCREMENT,
   customer_id int NOT NULL,
   insurance_id int NOT NULL,
   sub_insurance_id int NOT NULL,
   amount_to_pay float NOT NULL,
   amount_paid float NOT NULL DEFAULT 0,
   order_status enum('UNDER_REVIEW','PENDING', 'PAYMENT_FAILED', 'CONFIRMED', 'CANCELLED') NOT NULL, 
   payment_status enum('NOT_PAID', 'PAID') NOT NULL,
   premium_type enum('MONTHLY','QUARTERLY', 'HALF_YEARLY', 'ANNUAL') NOT NULL,
   created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   created_by int NOT NULL,
   approved_by int NULL,
   updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   FOREIGN KEY(customer_id) REFERENCES insurance.customers(id),
   FOREIGN KEY(insurance_id) REFERENCES insurance.insurance_plan(id),
   FOREIGN KEY(created_by) REFERENCES insurance.users(id),
   FOREIGN KEY(approved_by) REFERENCES insurance.users(id),
   PRIMARY KEY (id),
   CONSTRAINT customer_insurance_sub_uk UNIQUE KEY (customer_id,insurance_id,sub_insurance_id) 
);

CREATE TABLE insurance.tasks(
   id int NOT NULL AUTO_INCREMENT,
   order_id int NOT NULL,
   premium_amount_to_pay float NOT NULL,
   premium_amount_paid float NOT NULL DEFAULT 0,
   premium_type enum('MONTHLY','QUARTERLY', 'HALF_YEARLY', 'ANNUAL') NOT NULL,
   premium_penalty float NOT NULL DEFAULT 0,
   task_status enum('INITIALISED','DELAYED', 'DELAYED_PAYMENT','AWAITING_PAYMENT', 'INFORCE') NOT NULL,
   payment_status enum('NOT_PAID', 'PAID') NOT NULL,
   paid_at timestamp NULL,
   created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
   updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (id)    
);