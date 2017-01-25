import mysql.connector

__all__ = ['setup_procedures']

def setup_procedures(cursor, table):
    #ADD NODE adds node to specified parent and returns childs_id

    cursor.execute('''
                DELIMITER //
                DROP PROCEDURE IF EXISTS add_node;
                //

                CREATE DEFINER = CURRENT_USER PROCEDURE add_node (
                    IN parent_id BIGINT,
                    IN text_content TEXT
                )

                BEGIN

                DECLARE parent_lft BIGINT DEFAULT NULL;
                DECLARE parent_rgt BIGINT DEFAULT NULL;
                DECLARE temp BIGINT DEFAULT NULL;

                SELECT content_id, lft, rgt INTO parent_id, parent_lft, parent_rgt
                FROM '''+ table +
            ''' WHERE content_id = parent_id;

                -- inserting node:

                START TRANSACTION;

                    UPDATE ''' + table + ''' SET lft = CASE WHEN lft >  parent_rgt THEN lft + 2 ELSE lft END
                                    ,rgt = CASE WHEN rgt >= parent_rgt THEN rgt + 2 ELSE rgt END
                    WHERE rgt >= parent_rgt;

                    INSERT INTO ''' + table + ''' (content, lft, rht)
                         VALUES (text_content, parent_rgt , parent_rgt + 1);

                    SELECT LAST_INSERT_ID() INTO temp;

                COMMIT;

                SELECT temp AS child_id;

                END //
                DELIMITER ;
                '''
    )

    #find full path to node, later transformed in xms as path
    cursor.execute('''
                DELIMITER //
                DROP PROCEDURE IF EXISTS find_node;
                //

                CREATE DEFINER = CURRENT_USER PROCEDURE find_node (
                    IN searched TEXT
                )

                BEGIN

                SELECT parent.name
                FROM ''' + table + ''' AS node'''
                         + table + ''' AS parent
                WHERE node.lft BETWEEN parent.lft AND parent.rgt AND node.name = searched
                ORDER BY parent.lft
                AS path


                END //
                DELIMITER ;
                '''
    )
