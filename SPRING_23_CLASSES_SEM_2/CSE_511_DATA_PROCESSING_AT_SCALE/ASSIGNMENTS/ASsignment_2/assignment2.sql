-- Query - 1
CREATE TABLE "query1" AS
	(
		SELECT COUNT(1) AS "count of comments" 
		FROM authors a 
		JOIN comments c ON a.name = c.author 
		WHERE a.name = 'xymemez'
	);

-- Query - 2
CREATE TABLE "query2" AS
	(
		SELECT subreddit_type AS "subreddit type", 
			   COUNT(*) AS "subreddit count"
		FROM subreddits
		GROUP BY subreddit_type
	);

-- Query - 3
CREATE TABLE "query3" AS
	(
		SELECT subreddit AS name, COUNT(*) AS "comments count", 
			   ROUND(AVG(score), 2) AS "average score"
		FROM comments
		GROUP BY subreddit
		ORDER BY "comments count" DESC
		LIMIT 10
	);


-- QUery 4
CREATE TABLE "query4" AS
	(
		SELECT name, 
			   link_karma AS "link karma", 
			   comment_karma AS "comment karma",
			   (CASE WHEN link_karma >= comment_karma THEN 1 ELSE 0 END) AS "label"
		FROM authors
		WHERE (link_karma + comment_karma) / 2 > 1000000
	);

-- Query 5
CREATE TABLE "query5" AS
	(
		SELECT sr.subreddit_type AS "sr type", 
			   COUNT(uc.*) AS "comments num"
		FROM comments uc JOIN 
			 subreddits sr 
			 ON uc.subreddit_id = sr.name
		WHERE uc.author = '[deleted_user]'
		GROUP BY sr.subreddit_type
	);
	
-- Query 6
CREATE TABLE "query6" AS
	(SELECT (TO_TIMESTAMP(created_utc) AT TIME ZONE 'utc') AS "utc time",
		   subreddit AS "subreddit",
		   body AS "comment"
	FROM comments
	WHERE author = 'xymemez'
		  AND subreddit = 'starcraft');
  
-- Query 7 
CREATE TABLE "query7" AS
		(
			WITH oldest_subreddits AS
			(
				SELECT name, 
					   display_name, 
					   to_timestamp(created_utc) AS ts
				FROM subreddits
				WHERE over_18 = 'false'
				ORDER BY ts LIMIT 4
			),
		
			top_4 AS 
			(
				SELECT sb.title, 
				       sr.display_name, 
					   sb.ups, 
					   sb.subreddit_id,
					   row_number() over(partition by sb.subreddit_id ORDER BY sb.ups desc) AS rn
				FROM oldest_subreddits sr 
					JOIN submissions sb
					ON sr.name = sb.subreddit_id
			)
		
			SELECT title AS "submission", 
				   ups AS "ups", 
				   display_name AS "subreddit" 
		    FROM top_4
			WHERE rn < 5
		);
	
-- Query 8

CREATE TABLE "query8" AS
	(
		WITH Max_cte AS
		(
			SELECT author, ups AS upvotes
			FROM comments
			ORDER BY upvotes desc LIMIT 1
		),
		
		Min_cte AS
		(	
			SELECT author, ups AS upvotes
			FROM comments
			ORDER BY upvotes asc LIMIT 1
		)
		
		
		SELECT * FROM Max_cte union Select * FROM Min_cte
	);

-- Query 9
CREATE TABLE "query9" AS
	(
		SELECT  TO_CHAR(TO_TIMESTAMP(created_utc) AT TIME ZONE 'utc', 'YYYY-MM-DD') AS "date",
				COUNT(name) AS "count"
		FROM comments
		WHERE author = 'xymemez'
		GROUP BY date
		ORDER BY date
	);

-- Query 10
CREATE TABLE "query10" AS
(
	SELECT 
	EXTRACT(MONTH FROM to_timestamp(created_utc)) AS month, 
	subreddit, 
	COUNT(id) AS "count"
	FROM comments
	GROUP BY subreddit, EXTRACT(MONTH FROM to_timestamp(created_utc))
	ORDER BY "count" desc
	LIMIT 10
 );

