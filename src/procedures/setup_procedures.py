import mysql.connector

__all__ = ['setup_procedures']

def setup_procedures(cursor, db, table, database):
    #ADD NODE adds node to specified parent and returns childs_id

    procedures = ('''
                SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='STRICT_TRANS_TABLES';
                USE ''' + db + ''';

                DROP PROCEDURE IF EXISTS add_node;

                CREATE DEFINER = CURRENT_USER PROCEDURE add_node (IN parent_id BIGINT, IN text_content TEXT)

                proc: BEGIN

                DECLARE parent_lft BIGINT DEFAULT NULL;
                DECLARE parent_rgt BIGINT DEFAULT NULL;
                DECLARE temp BIGINT DEFAULT NULL;

                SELECT content_id, lft, rgt INTO parent_id, parent_lft, parent_rgt FROM ''' + table + ''' WHERE content_id = parent_id;

                START TRANSACTION;

                    UPDATE ''' + table + ''' SET lft = CASE WHEN lft >  parent_rgt THEN lft + 2 ELSE lft END ,rgt = CASE WHEN rgt >= parent_rgt THEN rgt + 2 ELSE rgt END WHERE rgt >= parent_rgt;

                    INSERT INTO ''' + table + ''' (content, lft, rgt) VALUES (text_content, parent_rgt , parent_rgt + 1);

                    SELECT LAST_INSERT_ID() INTO temp;

                COMMIT;

                SELECT temp AS child_id;

                END

                DROP PROCEDURE IF EXISTS find_node;

                CREATE DEFINER = CURRENT_USER PROCEDURE find_node (IN searched TEXT)

                proc: BEGIN

                    SELECT parent.content FROM ''' + table + ''' AS node, '''+ table + ''' AS parent WHERE node.lft BETWEEN parent.lft AND parent.rgt AND node.content = searched ORDER BY parent.lft;

                END
                SET sql_mode=@OLD_SQL_MODE;
                ''')
    print(procedures)
    cursor.execute(procedures, multi=True)
    database.commit()
