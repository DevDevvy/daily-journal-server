CREATE TABLE `Entries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
	`mood_id`	INTERGER NOT NULL,
	`date` TEXT NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `moods`(`id`)

);


CREATE TABLE `Moods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label` TEXT NOT NULL
);


CREATE TABLE `Entry_tags` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tag_id` INTERGER NOT NULL,
	`journal_entry_id`	TEXT NOT NULL,
	FOREIGN KEY(`tag_id`) REFERENCES `tags`(`id`),
	FOREIGN KEY(`journal_entry_id`) REFERENCES `entries`(`id`)

);



CREATE TABLE `Tags` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tag_name` TEXT NOT NULL
);

INSERT INTO `Tags` VALUES (null, "coding");
INSERT INTO `Tags` VALUES (null, "developing");
INSERT INTO `Tags` VALUES (null, "life");
INSERT INTO `Tags` VALUES (null, "problems");
INSERT INTO `Tags` VALUES (null, "celebrations");

INSERT INTO `Entries` VALUES (null, "Python", "Learning to put all of this together", 1, "April 11, 2022");
INSERT INTO `Entries` VALUES (null, "Python", "Second entry for showing I can do it", 2, "April 11, 2022");
INSERT INTO `Entries` VALUES (null, "Python", "And a third", 1, "April 11, 2022");
INSERT INTO `Entries` VALUES (null, "Python", "last and least", 3, "April 11, 2022");


INSERT INTO `Entry_tags` VALUES (null, 1, 1);
INSERT INTO `Entry_tags` VALUES (null, 2, 3);
INSERT INTO `Entry_tags` VALUES (null, 1, 1);
INSERT INTO `Entry_tags` VALUES (null, 3, 1);
INSERT INTO `Entry_tags` VALUES (null, 3, 4);


INSERT INTO `Moods` VALUES (null, "Happy");
INSERT INTO `Moods` VALUES (null, "Sad");
INSERT INTO `Moods` VALUES (null, "Angry");
INSERT INTO `Moods` VALUES (null, "Ok");
INSERT INTO `Moods` VALUES (null, "Excited");
INSERT INTO `Moods` VALUES (null, "Discouraged");

SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id,
            m.label,
            t.tag_name
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        LEFT JOIN Entry_tags et
            ON et.journal_entry_id = e.id
        LEFT JOIN Tags t
            ON t.id = et.tag_id