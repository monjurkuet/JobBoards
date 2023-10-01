CREATE TABLE `linkedinjobs` ( 
  `job_title` TEXT NULL,
  `company` TEXT NULL,
  `company_linkedin` TEXT NULL,
  `job_location` TEXT NULL,
  `job_posted_time` TEXT NULL,
  `job_url` VARCHAR(250) NOT NULL,
  CONSTRAINT `PRIMARY` PRIMARY KEY (`job_url`)
);
