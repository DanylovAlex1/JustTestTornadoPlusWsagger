import json
import tornado
#from tornado_json import schema


class NoResultError(Exception):
    pass

class BaseHandler(tornado.web.RequestHandler):

    def row_to_obj(self, row, cur):
        """Convert a SQL row to an object supporting dict and attribute access."""
        obj = tornado.util.ObjectDict()
        for val, desc in zip(row, cur.description):
            obj[desc.name] = val
        return obj

    async def queryone(self, stmt, *args):
        results = await self.query(stmt, *args)
        if len(results) == 0:
            raise NoResultError()
        elif len(results) > 1:
            raise ValueError("Expected 1 result, got %d" % len(results))
        return results[0]

    async def query(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)
            return [self.row_to_obj(row, cur) for row in await cur.fetchall()]

    async def execute(self, stmt, *args):
        with (await self.application.db.cursor()) as cur:
            await cur.execute(stmt, args)


class DocumentListAPIView(BaseHandler):
    """DocumentListAPIView"""
    async def get(self):
        """
        Description end-point
        ---
        tags:
        - Documents list
        summary: list of documents ordering by created desc
        description: list of documents ordering by created desc
        produces:
        - application/json
        parameters: none

        responses:
        "200":
          description: successful operation

        """
        documents = await self.query("SELECT id,title,text FROM document ORDER BY created DESC")
        self.write(json.dumps(documents))


class DocumentGetAPIView(BaseHandler):
    """DocumentGetAPIView"""

    async def get(self, idd):
        """
           Description end-point
           ---
           tags:
           - Get Document
           summary: Get document by id
           produces:
           - application/json
           parameters:
           - in: request
             name: idd
           - in: body
             name: body
             description: return document by id
             required: true
             """
        if id:
            try:
                documents = await self.queryone("SELECT id,title,text FROM document WHERE id=%i" %int(idd))
            except NoResultError:
                raise tornado.web.HTTPError(404)

        self.write(documents)


class DocumentCreateAPIView(BaseHandler):

    async def post(self):
        """
        Description end-point
        ---
        tags:
        - New Document
        summary: Create new document
        description: This can only be done by the logged in user.

        produces:
        - application/json
        parameters:
        - in: body
          name: document
          description: Created new document
          required: true
          schema:
            type: object
            properties:
              idd:
                type: integer
                format: int64
              title:
                type: string
              text:
                type: string
        responses:
        "201":
          description: successful operation
        """
        doc = json.loads(self.request.body)
        idd = doc['idd']
        title = doc["title"]
        text = doc["text"]
        await self.execute(
            "INSERT INTO document (id,title,text,created,updated)"
            "VALUES (%s,%s,%s,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)",
            idd, title, text)
        self.write(doc)

class DocumentDeleteAPIView(BaseHandler):
    """DocumentDeleteAPIView"""
    async def delete(self, idd):
        """
           Description end-point
           ---
           tags:
           - Delete Document
           summary: delete document by id
           produces:
           - application/json
           parameters:
           - in: request
             name: idd
           - in: body
             name: body
             required: true
             """
        await self.execute("DELETE FROM document WHERE id=%i" %int(idd))
        self.redirect('/')
