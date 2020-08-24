import aiopg
from tornado import web, locks
from tornado.options import options
import tornado
#import tornado_json.api_doc_gen
from tornado_swagger.setup import setup_swagger

from settings import appsettings, create_table
from urls import handlers


class Application(web.Application):
    def __init__(self, db):
        self.db = db
        setup_swagger(handlers)
        super(Application, self).__init__(handlers, **appsettings)


async def main():

    tornado.options.parse_command_line()
    # Create the global connection pool.
    async with aiopg.create_pool(
        host=options.db_host,
        port=options.db_port,
        user=options.db_user,
        password=options.db_password,
        dbname=options.db_database,
    ) as db:
        await create_table(db)
        app = Application(db)
        app.listen(options.port)

        shutdown_event = locks.Event()
        await shutdown_event.wait()


if __name__ == "__main__":
    print('listening to  http://localhost:%i%s' %(options.port, '/list'))
#    tornado_json.api_doc_gen.api_doc_gen(handlers)  # Get and write API documentation for routes to file
    tornado.ioloop.IOLoop.current().run_sync(main)
