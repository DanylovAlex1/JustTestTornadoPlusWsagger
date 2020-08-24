import os
import psycopg2
from tornado.options import define

define("port", default=8888, help="run on the given port", type=int)
define("db_host", default="127.0.0.1", help="document database host")
define("db_port", default=5432, help="document database port")
define("db_database", default="document", help="document database name")
define("db_user", default="document", help="document database user")
define("db_password", default="document", help="document database password")

appsettings = dict(
    # document_title=u"Tornado",
    # template_path=os.path.join(os.path.dirname(__file__), "templates"),
    # static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=False,
    cookie_secret="__VERY_VERY_SECRET_KEY_HERE__",
#    login_url="/auth/login",
    debug=True,
)

async def create_table(db):
    try:
        with (await db.cursor()) as cur:
            await cur.execute("SELECT COUNT(*) FROM document LIMIT 1")
            await cur.fetchone()
    except psycopg2.ProgrammingError:
        with open("schema.sql") as f:
            schema = f.read()
        with (await db.cursor()) as cur:
            await cur.execute(schema)
