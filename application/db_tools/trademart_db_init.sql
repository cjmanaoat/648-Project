CREATE SCHEMA `trademart_test`;

/***** CREATING USER TABLE *****/
CREATE TABLE `trademart_test`.`user` (
  `user_id` INT NOT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `user_name` VARCHAR(45) NULL,
  `user_addr` VARCHAR(45) NULL,
  `user_pass` VARCHAR(45) NULL,
  `reg_status` INT NULL,
  `user_rating` INT NULL,
  `user_listings` INT NULL,
  `is_admin` TINYINT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_email_UNIQUE` (`user_email` ASC) VISIBLE);

	CREATE TABLE `trademart_test`.`object` (
  `object_id` INT NOT NULL,
  `obj_name` VARCHAR(45) NULL,
  `department` VARCHAR(45) NULL,
  `course` VARCHAR(45) NULL,
  `term` VARCHAR(45) NULL,
  `section` INT NULL,
  `version` INT NULL,
  `isbn` BIGINT NULL,
  PRIMARY KEY (`object_id`));

/***** CREATING CATEGORY TABLE *****/

CREATE TABLE `trademart_test`.`category` (
	`category_name` VARCHAR(45) NOT NULL,
	PRIMARY KEY (`category_name`));

	/***** CREATING LISTING TABLE *****/

	CREATE TABLE `trademart_test`.`listing` (
  `list_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `object_id` INT NULL,
  `list_title` VARCHAR(45) NOT NULL,
  `list_category` VARCHAR(45) NOT NULL,
  `pref_location` VARCHAR(45) NULL,
  `list_desc` VARCHAR(100) NULL,
  `approval_status` INT NOT NULL,
  `offer_type` VARCHAR(45) NULL,
  `list_date` DATE NULL,
  `list_time` TIME NULL,
  `image` LONGBLOB NULL,
  `suggest_price` DECIMAL(10,0) NOT NULL,
  `condition` VARCHAR(45) NULL,
  PRIMARY KEY (`list_id`),
  INDEX `obj_id_idx` (`object_id` ASC) VISIBLE,
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `obj_id`
    FOREIGN KEY (`object_id`)
    REFERENCES `trademart_test`.`object` (`object_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `trademart_test`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
/*had to alter to add foreign key constraint*/
ALTER TABLE `trademart_test`.`listing`
ADD INDEX `list_categ_idx` (`list_category` ASC) VISIBLE;
;
ALTER TABLE `trademart_test`.`listing`
ADD CONSTRAINT `list_categ`
	FOREIGN KEY (`list_category`)
	REFERENCES `trademart_test`.`category` (`category_name`)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION;

/***** CREATING OFFER TABLE *****/

	CREATE TABLE `trademart_test`.`offer` (
	  `offer_id` INT NOT NULL,
	  `seller_id` INT NOT NULL,
	  `buyer_id` INT NOT NULL,
	  `listing_id` INT NOT NULL,
	  `offer_amount` DECIMAL(10,0) NOT NULL,
	  `location` VARCHAR(45) NULL,
	  PRIMARY KEY (`offer_id`, `listing_id`),
	  INDEX `buyer_id_idx` (`buyer_id` ASC) VISIBLE,
	  INDEX `seller_id_idx` (`seller_id` ASC) VISIBLE,
	  INDEX `listing_id_idx` (`listing_id` ASC) VISIBLE,
	  CONSTRAINT `buyer_id`
	    FOREIGN KEY (`buyer_id`)
	    REFERENCES `trademart_test`.`user` (`user_id`)
	    ON DELETE NO ACTION
	    ON UPDATE NO ACTION,
	  CONSTRAINT `seller_id`
	    FOREIGN KEY (`seller_id`)
	    REFERENCES `trademart_test`.`user` (`user_id`)
	    ON DELETE NO ACTION
	    ON UPDATE NO ACTION,
	  CONSTRAINT `listing_id`
	    FOREIGN KEY (`listing_id`)
	    REFERENCES `trademart_test`.`listing` (`list_id`)
	    ON DELETE NO ACTION
	    ON UPDATE NO ACTION);


/***** CREATING MESSAGE TABLE *****/

CREATE TABLE `trademart_test`.`message` (
  `sender_id` INT NOT NULL,
  `receiver_id` INT NOT NULL,
  `offer_id` INT NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `text` TEXT NOT NULL,
  `msg_datetime` DATETIME NULL,
  PRIMARY KEY (`sender_id`, `receiver_id`, `offer_id`),
  INDEX `offer_id_idx` (`offer_id` ASC) VISIBLE,
  INDEX `receiver_id_idx` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `offer_id`
    FOREIGN KEY (`offer_id`)
    REFERENCES `trademart_test`.`offer` (`offer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `sender_id`
    FOREIGN KEY (`sender_id`)
    REFERENCES `trademart_test`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `receiver_id`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `trademart_test`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

/***** Adding data to tables ****/
INSERT INTO User
VALUES (373967284, "kahleed@mail.sfsu.edu", "Khaleed",  "1 A Dr, San Francisco, CA", "password", 1, 3, NULL, 0),
	     (265926826, "donald@mail.sfsu.edu", "Donald", "123 Sesame St, San Francisco, CA", "password", 1, 5, NULL, 0),
       (266926598, "pugman@mail.sfsu.edu", "Pugman", "66 Broken Dreams Blvd, San Francisco, CA", "password", 1, 4, NULL, 0),
       (194724822, "ken@mail.sfsu.edu", "Ken", "321 Street St, San Francisco, CA", "password", 1, 5, NULL, 0),
       (572957392, "charlie@mail.sfsu.edu", "Charlie", "934 Submarine St, San Francisco, CA", "password", 0, 0, NULL, 0),
			 (834728592, "lisa@mail.sfsu.edu", "Lisa", "25 Ocean Ave, San Francisco, CA", "password", 1, 0, NULL, 1);

INSERT INTO Object
	VALUES (12341, "Shakespearean Curses", "ENG", "101", "FALL2020", 2, 1, 3847383828205),
				 (34583, "Legos: Beginner's Guide", "ENGR", "203", "FALL2020", 5, 7, 8573729205732),
				 (37262, "Cool Math Games", "MATH", "100", "FALL2020", 1, 3, 1010101010101),
			 	 (39472, "Easy Pointers", "CSC", "200", "FALL2020", 4, 1, 1837462846728),
			 	 (98234, "iClicker", "PHYS", "271", "FALL2020", 1, 1, NULL);

INSERT INTO Category
		VALUES ("Books"),
				 	 ("Electronics"),
				 	 ("Furniture"),
				 	 ("Tutoring"),
				 	 ("Editing");

INSERT INTO Listing
VALUES (12381, 265926826, 37262, "Math 100 Book for Sale", "Books", "Gym", "required textbook for math 100 with Professor Prof", 1, "bid", '2020-01-01', '12:39:19', NULL, 50.00, "good"),
			 (19273, 194724822, NULL, "Sofa for Sale", "Furniture", "Dorms", "***Need to get rid of this couch", 0, "bid", '2020-01-01', '23:43:12', NULL, 70.00, "great"),
			 (23484, 266926598, 98234, "take my iclicker", "Electronics", "Quad", NULL, 1, "fixed", '2020-10-02', '12:53:24', NULL, 40, "fair"),
			 (27472, 373967284, 34583, "engineering textbook, hardcover", "Books", "Entrance", "no notes written inside", 1, "fixed", '2020-01-01', '01:43:12', NULL, 40.00, "great"),
			 (29472, 265926826, NULL, "Essay Editing", "Editing", NULL, "I will edit any essay for you, max 15 pages.", 1, "fixed", '2020-03-12', '23:00:00', NULL, 10.00, NULL),
			 (58374, 265926826, 98234, "iclicker for any class", "Electronics", "Park", "works well, slightly scratched on the corner", 0, "bid", '2020-04-26','23:12:32', NULL, 20.00, "fair"),
			 (78234, 373967284, NULL, "Physics Tutoring (1 hour)", "Tutoring", "Library", "Tutoring for any Physics class by a Physics Grad student", 1, "fixed", '2020-01-28', '05:23:40', NULL, 20.00, NULL),
			 (23421, 194724822, 39472, "pointer textbook for classes in c/c++", "Books", "Park", NULL, 0, "fixed", '2020-01-01', '11:23:12', NULL, 10000.00, "great");

INSERT INTO Offer
	VALUES (23847, 373967284, 266926598, 78234, 40.00, "Library"),
				 (12927, 265926826, 373967284, 12381, 40.00, "Parking Garage"),
			   (18361, 265926826, 194724822, 12381, 25.00, "Cafe"),
			   (12522, 373967284, 265926826, 27472, 40.00, "Thornton Hall");

SET @@time_zone = 'SYSTEM';
INSERT INTO Message
	VALUES (373967284, 266926598, 23847, "Intertested in iClicker", "Please message me at (555)555-555. I'm cool with meeting at the library.", '2020-01-01 10:10:10');

/*Use this query to see all data currently in any table

SELECT * FROM <table name>;

*/
