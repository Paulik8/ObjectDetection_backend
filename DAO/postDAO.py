from tornado import gen
from parser import auth_parse


class PostDAO:
    def __init__(self, db):
        self.db = db

    @gen.coroutine
    def get_post(self, id_tag):
        sql = """
            SELECT * FROM posts 
            JOIN images_posts_tags ipt ON posts.id = ipt.id_post
            WHERE id_tag = %s
        """
        cursor = yield self.db.execute(sql, (id_tag))
        return cursor.fetchall()


    @gen.coroutine
    def get_posts_by_tag(self, tag, page):
        limit_1 = (page - 1) * 5
        limit_2 = 5
        sql = """
            SELECT nickname, age, image, caption, data FROM posts
            JOIN users ON posts.author = users.id
            JOIN images_posts_tags ipt ON posts.id = ipt.id_post
            where id_tag = %s ORDER BY data DESC OFFSET %s LIMIT %s
        """
        cursor = yield self.db.execute(sql, (tag, limit_1, limit_2))
        return cursor.fetchall()

    @gen.coroutine
    def get_posts_by_tags(self, tags, page):
        limit_1 = (page - 1) * 5
        limit_2 = 5
        sql = """
               SELECT nickname, age, image, caption, data FROM posts
                      JOIN 
                        (SELECT posts.id FROM posts
                        JOIN images_posts_tags ipt ON posts.id = ipt.id_post
                        WHERE id_tag IN (%s) GROUP BY posts.id HAVING count(*) > 1) AS a ON a.id = posts.id
                      JOIN users ON posts.author = users.id
        """
        sql2 = """
            ORDER BY data DESC OFFSET %s LIMIT %s
        """
        format_strings = ','.join(['%s'] * len(tags))
        # cursor = yield self.db.execute('SELECT id_post FROM posts JOIN images_posts_tags ipt ON posts.id = ipt.id_post WHERE id_tag IN ({0}) GROUP BY id_post HAVING count(*) > 1'.format(','.join('?' for _ in tags)), tags)
        cursor = yield self.db.execute(sql % format_strings + sql2, (tags[0], tags[1], limit_1, limit_2))
        return cursor.fetchall()

    @gen.coroutine
    def get_id(self, nick):
        sql = """
            SELECT id FROM users WHERE nickname = %s
        """
        cursor = yield self.db.execute(sql, nick)
        return cursor.fetchone()

    @gen.coroutine
    def load_post(self, arr):
        sql = """
            INSERT INTO posts (author, caption, data, image, tags) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """
        cursor = yield self.db.execute(sql, (arr[0], arr[1], arr[2], arr[3], "kek"))
        return cursor.fetchone()

    @gen.coroutine
    def get_posts(self, page):
        limit_1 = (page - 1) * 5
        limit_2 = 5  # 5 записей на страницу
        sql = """
            SELECT nickname, age, image, caption, data FROM posts JOIN users ON author = users.id ORDER BY data DESC OFFSET %s LIMIT %s
        """
        cursor = yield self.db.execute(sql, (limit_1, limit_2))
        return cursor.fetchall()

    @gen.coroutine
    def get_auth(self, arr):
        sql = """
            SELECT id FROM users WHERE nickname = %s AND password = %s
        """
        cursor = yield self.db.execute(sql, (arr[0], arr[1]))
        return cursor.fetchone()

    def create_table_posts(self):
        sql = """
            CREATE TABLE IF NOT EXISTS posts(
            id SERIAL NOT NULL PRIMARY KEY,
            author INTEGER NOT NULL,
            image INTEGER NOT NULL,
            caption CITEXT,
            data TIMESTAMP,
            tags CITEXT,
            FOREIGN KEY (author) REFERENCES "users" (id),
            FOREIGN KEY (image) REFERENCES "images" (id)
            );
        """

    def create_table_images_posts_tags(self):
        sql = """
            CREATE TABLE IF NOT EXISTS images_posts_tags(
            id_image INTEGER,
            id_post INTEGER,
            id_tag INTEGER,
            FOREIGN KEY (id_image) REFERENCES "images" (id),
            FOREIGN KEY (id_post) REFERENCES "posts" (id),
            FOREIGN KEY (id_tag) REFERENCES "tags" (id)
            );
        """

    def create_table_tags(self):
        sql = """
            CREATE TABLE IF NOT EXISTS tags(
            id SERIAL NOT NULL PRIMARY KEY,
            name CITEXT
            );
        """

    def create_fields_tags(self):
        sql = """
            INSERT INTO tags (name) VALUES ('cat cats'),('dog dogs');
        """
