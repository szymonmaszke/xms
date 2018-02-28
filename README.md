xms
=============

<p align="center">
    <a href="https://upload.wikimedia.org/wikipedia/commons/6/64/XMind_Logo.png">
        <img height=160 src="https://upload.wikimedia.org/wikipedia/commons/6/64/XMind_Logo.png">
    </a>
</p>


| **Language** | **MySQL** | **Style** |
|--------------------|----------------------------|------------------|
| ![Language](https://img.shields.io/badge/python-3.6-brightgreen.svg) |![Database](https://img.shields.io/badge/MariaDB-10.1.31-blue.svg) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/6f99a332ab8a47499323ae9b88ddb0db)](https://www.codacy.com/app/vyz/XMind-Searcher?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vyzyv/XMind-Searcher&amp;utm_campaign=Badge_Grade) |

Command line mind map searcher.

Parse your mind maps, create hierarchical database and search against it using keyword.
After installation use the command below:

```bash
xms <keyword> [-c --color] [-k --keep] [--s --secret SECRET]
```
To display help use standard ***-h*** parameter.

# Demo

You can easily find the keyword and open mind map containing it as shown below:

![gif](https://user-images.githubusercontent.com/20703378/36677183-dc9eaa36-1b0d-11e8-81fa-1ccd13b49981.gif)

- First line: path to the mind map with found keyword
- Second line: name of the mind map (root)
- Following lines: Consecutive branches pointing to keyword

# Why?

Let's say the **average mind map** may have around **100-200 branches**. According to standards one **branch** should consist of **1-5 words**.

If you have a lot of mind maps (e.g. 100) **total amount of words will be around 50.000**.
In such case it's easy to forget where certain important informations are located. 

Thanks to this plugin your trouble is gone as it **scans through all of them and gives you the exact branch and mind map for any sought keyword**.

# Installation

Install required dependencies, run install.sh from terminal and follow the
instructions displayed on the screen.

## Dependencies

- **[XMind 7+](https://www.xmind.net)**
- **[Python 3.6.1+](https://www.python.org/downloads/release/python-363/)**
- MySQL implementation 5.1 or higher (advised: **[MariaDB 10.1.31+](https://www.python.org/downloads/release/python-363/)**)
- Optional: **[pipenv](https://github.com/pypa/pipenv)** or install pip packages located in ***Pipfile*** directly
