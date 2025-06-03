from search_db_conn import get_connection

class Author:
    def __init__(self, id=None, name=None, bio=None):
        self.id = id
        self.name = name
        self.bio = bio

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name = ?, bio = ? WHERE id = ?", (self.name, self.bio, self.id))
        else:
            cursor.execute("INSERT INTO authors (name, bio) VALUES (?, ?)", (self.name, self.bio))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(
                id=row["id"],
                name=row["name"],
                bio=row["bio"] if "bio" in row.keys() else None
            )
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        rows = cursor.fetchall()
        conn.close()
        return [
            cls(
                id=row["id"],
                name=row["name"],
                bio=row["bio"] if "bio" in row.keys() else None
            )
            for row in rows
        ]

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def add_article(self, magazine, title):
        from lib.models.article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row["category"] for row in rows]

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("""
            SELECT a.*, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """).fetchone()
        conn.close()
        if row:
            return cls(
                id=row["id"],
                name=row["name"],
                bio=row["bio"] if "bio" in row.keys() else None
            )
        return None
