# Magazine ORM Project

A simple Python + SQLite3 ORM-based CLI app to manage authors, articles, and magazines. Built using Python classes and raw SQL queries.

## Features

- Add and retrieve authors, articles, and magazines
- Get all magazines an author has written for
- List articles by a magazine or author
- Find the top author by article count

## Technologies

- Python 3
- SQLite3
- Raw SQL (no ORM libraries like SQLAlchemy)
- `pytest` for testing

## Setup Instructions
```bash
git clone https://github.com/Kabogo-Maverick/magazine.git
cd magazine
python3 -m venv venv
source venv/bin/activate
pip install pytest
pytest test_all.py
