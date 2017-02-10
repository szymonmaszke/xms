XMind-Searcher
=============

# [About]

Processes XMind mind maps and translates them into MySQL's
hierarchical database.

Afterwards xms.py allows searching through the database.
Query is a keyword, program returns exact branch where the
searched query is located (path starting from mind map name).

BUGGED:
Adding nodes, not displaying found keywords correctly

# Warning

Project is not finished, not working properly

## [TO DO]

- Fix node additions
- Add automatic installation (and pip package)
- More output options
- Fix and check experimental XSD validation

## [REQUIRED DEPENDENCIES]

	- Python3 (tested on Python3.6)
	- MySQL 5.1 or higher (tested on MySQL 5.6)

	- Oracle's Python db-connector
	[Installation: pip install mysql-connector-python or reference]
	- Github account
	- git

## [OPTIONAL DEPENDENCIES]

	- xmllint
	(experimental -e flag in src/init/init.py validating .xmind files with schema)
	- github3 Python API: https://github.com/sigmavirus24/github3.py (available in pip)
	(Needed to clone repositories containing mind maps from GitHub)

