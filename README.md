xms
=============

<p align="center">
    <a href="https://upload.wikimedia.org/wikipedia/commons/6/64/XMind_Logo.png">
        <img height=85 src="https://upload.wikimedia.org/wikipedia/commons/6/64/XMind_Logo.png">
    </a>
</p>


| **Language** | **MySQL** | **Style** |
|--------------------|----------------------------|------------------|
| ![Language](https://img.shields.io/badge/python-3.6-brightgreen.svg) |![Database](https://img.shields.io/badge/MariaDB-10.1.31-blue.svg) |

Command line mind map searcher.

Parse your mind maps, create hierarchical database and search against it using keyword.
After installation use the command below:

```bash
xms <keyword> [-c --color] [-k --keep] [--s --secret SECRET]
```
To display help use standard ***-h*** parameter.

# Demo

![gif](https://github.com/vyzyv/xmind_searcher/raw/master/xms.gif)

- First line: path to the mind map with found keyword
- Second line: name of the mind map (root)
- Following lines: Consecutive branches pointing to keyword

# Installation

Install required dependencies, run install.sh from terminal and follow the
instructions displayed on the screen.

## Dependencies

- **[XMind 7+](https://www.xmind.net)**
- **[Python 3.6.1+](https://www.python.org/downloads/release/python-363/)**
- MySQL implementation 5.1 or higher (advised: **[MariaDB 10.1.31+](https://www.python.org/downloads/release/python-363/)**)
- Optional: **[pipenv](https://github.com/pypa/pipenv)** or install pip packages located in ***Pipfile*** directly
