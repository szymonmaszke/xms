# XMind-Searcher

# [ALPHA STAGE W.I.P.]

Processes XMind mind maps and translates them into MySQL's
hierarchical database.

Afterwards xms.py allows searching through the database.
Query is a keyword, program returns exact branch where the
searched query is located (full path starting from mind map name).

Setting up the database is mediocre complicated as the product
is still in alpha stage. All of it is described in README in src/

# [REQUIRED DEPENDENCIES]

	- Python3 (tested on Python3.6)
	- MySQL 5.1 or higher (tested on MySQL 5.6)

	- Oracle's Python db-connector
	[Installation: pip install mysql-connector-python or reference]
	- Github

# [OPTIONAL DEPENDENCIES]

	- xmllint
	(experimental -e flag in src/init/init.py validating .xmind files with schema)
	- github3 Python API: https://github.com/sigmavirus24/github3.py
	(Available via pip as well)
