-- CREATE SCHEMA IF NOT EXISTS postgres;

CREATE TABLE IF NOT EXISTS authors
(
"id" TEXT,
"retrieved_on" INTEGER,
"name" TEXT UNIQUE,
"created_utc" INTEGER,
"link_karma" INTEGER,
"comment_karma" INTEGER,
"profile_img" TEXT,
"profile_color" TEXT,
"profile_over_18" BOOLEAN,
PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS subreddits(
"banner_background_image" TEXT,
"created_utc" INTEGER,
"description" TEXT,
"display_name" TEXT UNIQUE,
"header_img" TEXT,
"hide_ads" BOOLEAN,
"id" TEXT,
"over18" BOOLEAN,
"public_description" TEXT,
"retrieved_utc" INTEGER,
"name" TEXT UNIQUE,
"subreddit_type" TEXT,
"subscribers" INTEGER,
"title" TEXT,
"whitelist_status" TEXT,
PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS submissions (
"downs" INTEGER,
"url" TEXT,
"id" TEXT,
"edited" BOOLEAN,
"num_reports" INTEGER,
"created_utc" INTEGER,
"name" TEXT,
"title" TEXT,
"author" TEXT,
"permalink" TEXT,
"num_comments" INTEGER,
"likes" BOOLEAN,
"subreddit_id" TEXT,
"ups" INTEGER,

PRIMARY KEY (id),
CONSTRAINT FK_Author_Name FOREIGN KEY(author)
REFERENCES authors(name)
ON DELETE SET NULL,
	
CONSTRAINT FK_Subreddit_id FOREIGN KEY(subreddit_id)
REFERENCES subreddits(name)
ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS comments (
"distinguished" TEXT,
"downs" INTEGER,
"created_utc" INTEGER,
"controversiality" INTEGER,
"edited" BOOLEAN,
"gilded" INTEGER,
"author_flair_css_class" TEXT,
"id" TEXT,
"author" TEXT,
"retrieved_on" INTEGER,
"score_hidden" BOOLEAN,
"subreddit_id" TEXT,
"score" INTEGER,
"name" TEXT,
"author_flair_text" TEXT,
"link_id" TEXT,
"archived" BOOLEAN,
"ups" TEXT,
"parent_id" TEXT,
"subreddit" TEXT,
"body" TEXT,
	
	
PRIMARY KEY (id),
CONSTRAINT FK_Author_Name FOREIGN KEY(author)
REFERENCES authors(name)
ON DELETE SET NULL,
	
CONSTRAINT FK_Subreddit_id FOREIGN KEY(subreddit_id)
REFERENCES subreddits(name)
ON DELETE SET NULL,

CONSTRAINT FK_Subreddit_DP FOREIGN KEY(subreddit)
REFERENCES subreddits(display_name)
ON DELETE SET NULL
);
