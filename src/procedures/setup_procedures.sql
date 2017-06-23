SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES';

DELIMITER //
DROP PROCEDURE IF EXISTS add_node;
//

CREATE DEFINER = CURRENT_USER PROCEDURE add_node (
		IN parent_id BIGINT,
		IN text_content TEXT,
    OUT inserted_id BIGINT
)

BEGIN

  SELECT @new_right := rgt FROM tree WHERE content_id = parent_id;

	START TRANSACTION;
      UPDATE tree SET rgt = rgt + 2 WHERE rgt >= @new_right;
      UPDATE tree SET lft = lft + 2 WHERE lft > @new_right;

			INSERT INTO tree (content, lft, rgt)
					 VALUES (text_content, @new_right , @new_right + 1);
      SELECT LAST_INSERT_ID() INTO inserted_id;

	COMMIT;

END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS find_node;
//

CREATE DEFINER = CURRENT_USER PROCEDURE find_node (
		IN searched TEXT,
		IN off BIGINT
)

proc: BEGIN

	SELECT parent.content
	FROM tree AS node,
			 tree AS parent
	WHERE node.lft BETWEEN parent.lft AND parent.rgt
				AND node.content =
				(SELECT content FROM tree WHERE match(content) AGAINST(searched IN BOOLEAN MODE) LIMIT 1 OFFSET off)
	ORDER BY parent.lft;

END //
DELIMITER ;

SET sql_mode=@OLD_SQL_MODE;
