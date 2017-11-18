XMind-Searcher
=============
CLI XMind mind maps searcher!

Parses all of your mindmaps (local or from github!), creates database and allows
you to search through them using keywords via:

```bash
xms <keyword>
```


# [Demo]

First line is the mind map, next indented sentences are consecutive branches leading
to sought keyword

![gif](https://github.com/vyzyv/xmind_searcher/raw/master/xms.gif)

# [Installation]

Install required dependencies, run install.sh from terminal and follow the
instructions.

## [REQUIRED DEPENDENCIES]

	- Python3 (tested on Python3.6)
	- MySQL 5.1 or higher (tested on MySQL 5.6)

	- Oracle's Python db-connector
	[Installation: pip install mysql-connector-python or reference]

## [OPTIONAL DEPENDENCIES]

	- xmllint
	(experimental -e flag in src/init/init.py validating .xmind files with schema)
