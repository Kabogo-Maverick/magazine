from search_db_conn import get_connection

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in one transaction.
    articles_data: list of dicts with 'title' and 'magazine_id'
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        author_id = cursor.lastrowid

        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return False
    finally:
        conn.close()
