SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES';

USE xmindmaps;

DELIMITER //
DROP PROCEDURE IF EXISTS add_node;
//

CREATE DEFINER = CURRENT_USER PROCEDURE add_node (
		IN parent_id BIGINT,
		IN text_content TEXT
)

proc: BEGIN

	DECLARE parent_lft BIGINT DEFAULT NULL;
	DECLARE parent_rgt BIGINT DEFAULT NULL;
	DECLARE temp BIGINT DEFAULT NULL;

	SELECT content_id, lft, rgt INTO parent_id, parent_lft, parent_rgt
	FROM tree
	WHERE content_id = parent_id;

	-- inserting node:

	START TRANSACTION;

			UPDATE tree SET lft = CASE WHEN lft >  parent_rgt THEN lft + 2 ELSE lft END
											,rgt = CASE WHEN rgt >= parent_rgt THEN rgt + 2 ELSE rgt END
			WHERE rgt >= parent_rgt;

			INSERT INTO tree (content, lft, rgt)
					 VALUES (text_content, parent_rgt , parent_rgt + 1);

			SELECT LAST_INSERT_ID() INTO temp;

	COMMIT;

	-- return value

	SELECT temp AS child_id;

END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS find_node;
//

CREATE DEFINER = CURRENT_USER PROCEDURE find_node (
		IN searched TEXT
)

proc: BEGIN

	SELECT parent.content
	FROM tree AS node,
			 tree AS parent
	WHERE node.lft BETWEEN parent.lft AND parent.rgt AND node.content = searched
	ORDER BY parent.lft;

END //
DELIMITER ;

SET sql_mode=@OLD_SQL_MODE;
