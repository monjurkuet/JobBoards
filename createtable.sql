CREATE TABLE `glassdoorjobs` ( 
  `job_title` TEXT NULL,
  `company` TEXT NULL,
  `company_link` TEXT NULL,
  `job_location` TEXT NULL,
  `job_posted_time` TEXT NULL,
  `job_url` VARCHAR(250) NOT NULL,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`job_url`)
);
CREATE TABLE `indeedjobs` ( 
  `job_title` TEXT NULL,
  `company` TEXT NULL,
  `job_location` TEXT NULL,
  `job_posted_time` TEXT NULL,
  `job_url` VARCHAR(250) NOT NULL,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`job_url`)
);
CREATE TABLE `linkedin_jobs_details` ( 
  `job_url` VARCHAR(250) NOT NULL,
  `applicants` INT NULL,
  `employee_headcount` TEXT NULL,
  `industry` LONGTEXT NULL,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`job_url`)
);
CREATE TABLE `linkedincrawler_company` ( 
  `company_linkedin` VARCHAR(250) NOT NULL,
  `domain` VARCHAR(250) NULL,
  `updatedAt` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`company_linkedin`)
);
CREATE TABLE `linkedinjobs` ( 
  `job_title` TEXT NULL,
  `company` TEXT NULL,
  `company_linkedin` TEXT NULL,
  `job_location` TEXT NULL,
  `job_posted_time` DATE NULL,
  `job_url` VARCHAR(250) NOT NULL,
  `salary` LONGTEXT NULL,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`job_url`)
);
CREATE VIEW `companytodaywithjobs` AS with `rankeddata` as (select `lc`.`company_linkedin` AS `lc_company_linkedin`,`lc`.`domain` AS `domain`,`lc`.`updatedAt` AS `lc_updatedAt`,`lj`.`job_title` AS `job_title`,`lj`.`company` AS `lj_company`,`lj`.`company_linkedin` AS `lj_company_linkedin`,`lj`.`job_location` AS `job_location`,`lj`.`job_posted_time` AS `job_posted_time`,`lj`.`job_url` AS `job_url`,row_number() OVER (PARTITION BY `lj`.`company_linkedin` ORDER BY `lc`.`updatedAt` desc )  AS `rowrank` from (`jobboards`.`linkedinjobs` `lj` left join `jobboards`.`linkedincrawler_company` `lc` on((`lc`.`company_linkedin` = `lj`.`company_linkedin`))) where (cast(`lj`.`job_posted_time` as date) = curdate())) select `rankeddata`.`lc_company_linkedin` AS `lc_company_linkedin`,`rankeddata`.`domain` AS `domain` from `rankeddata` where (`rankeddata`.`rowrank` = 1);
CREATE VIEW `todayjobs` AS select `jobboards`.`linkedinjobs`.`job_title` AS `job_title`,`jobboards`.`linkedinjobs`.`company` AS `company`,`jobboards`.`linkedinjobs`.`company_linkedin` AS `company_linkedin`,`jobboards`.`linkedinjobs`.`job_location` AS `job_location`,`jobboards`.`linkedinjobs`.`job_posted_time` AS `job_posted_time`,`jobboards`.`linkedinjobs`.`job_url` AS `job_url` from `jobboards`.`linkedinjobs` where (cast(`jobboards`.`linkedinjobs`.`job_posted_time` as date) = curdate());
