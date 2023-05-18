import tornado
import tornado.ioloop
import tornado.web
import os, uuid, json
import asyncio
import aiofiles
from tornado.web import MissingArgumentError, HTTPError, Application, StaticFileHandler

__UPLOADS__ = "uploads/"

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")

docmap = {}

class DefaultHandler(tornado.web.RequestHandler):
    ## Test with $ curl -F 'filearg=@/home/labcomputer/aiquizmaster/README.md' http://localhost:8888/backend/doc
    async def get(self):
        self.write(json.dumps({}))


class DocHandler(tornado.web.RequestHandler):
    ## Test with $ curl -F 'filearg=@/home/labcomputer/aiquizmaster/README.md' http://localhost:8888/backend/doc
    async def post(self):
        #https://technobeans.com/2012/09/17/tornado-file-uploads/
        fileinfo = self.request.files['filearg'][0]
        print ("fileinfo is", fileinfo)
        fname = fileinfo['filename']
        extn = os.path.splitext(fname)[1]
        uuid_str = str(uuid.uuid4())
        cname = uuid_str + extn
        async with aiofiles.open(__UPLOADS__ + cname, mode='wb') as f:
            await f.write(fileinfo['body'])
        docmap[uuid_str] = {"fullname":fname, "extn": extn, "cname": cname, "id":uuid_str}
        print(cname + " is uploaded!! Check %s folder" %__UPLOADS__)
        self.write(json.dumps(docmap[uuid_str]))

    async def get(self, did = None):
        if self.get_query_argument('file',None):
            ### Test with curl http://localhost:8888/backend/doc/af50cf65-5869-4b22-a15e-e6dd41b7e3a5/?file=True
            chunkSize = 1024 * 1024 * 1 # 1 Mib
            with open(__UPLOADS__ + docmap[did]["cname"], 'rb') as f:
                while True:
                    chunk = f.read(chunkSize)
                    if not chunk:
                        break
                    try:
                        self.write(chunk) # write the chunk to the response
                        await self.flush()# send the chunk to the client
                    except iostream.StreamClosedError:
                        break
                    finally:
                        del chunk
                        await gen.sleep(0.000000001)
            self.finish()
        else:
            ### Test with curl http://localhost:8888/backend/doc/7e5cc450-ad6b-4475-9cbd-859a02d28e5e/
            self.write(json.dumps(docmap[did]))


async def main():
    application = Application([
        (r"/", DefaultHandler),
        (r"/backend/doc", DocHandler),
        (r"/backend/doc/(?P<did>.+)/", DocHandler),
    ], autoreload=True)
    application.listen(8888)
    shutdown_event = asyncio.Event()
    print("Listening on 8888")
    await shutdown_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
