import tornado
import tornado.ioloop
import tornado.web
import os, uuid, json
import asyncio
import aiofiles
import random
from tornado.web import MissingArgumentError, HTTPError, Application, StaticFileHandler

__UPLOADS__ = "uploads/"

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("fileuploadform.html")

docmap = {}

class BaseHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("say something")

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

class DefaultHandler(tornado.web.RequestHandler):
    ## Test with $ curl -F 'filearg=@/home/labcomputer/aiquizmaster/README.md' http://localhost:8888/backend/doc
    async def get(self):
        self.write(json.dumps({}))

class DocHandler(BaseHandler):
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
        entry = {"fullname":fname, "extn": extn, "cname": cname, "id":uuid_str}
        docmap[uuid_str] = entry
        print(cname + " is uploaded!! Check %s folder" %__UPLOADS__)
        self.write(json.dumps(entry))

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
                        await asyncio.sleep(0.000000001)
            self.finish()
        else:
            ### Test with curl http://localhost:8888/backend/doc/7e5cc450-ad6b-4475-9cbd-859a02d28e5e/
            self.write(json.dumps(docmap[did]))


class QuestionHandler(BaseHandler):
    async def post(self, did):
        qid_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ### Create a question based on the file content in did
        ### Make sure it is async
        question = "What is your name?"
        if not "questions" in docmap[did]:
            docmap[did]["questions"] = {}
        qentry = {"question": question, "id": qid_str}
        docmap[did]["questions"][qid_str] = qentry
        self.write(json.dumps(qentry))

    async def get(self, did, qid ):
        self.write(json.dumps(docmap[did]["questions"][qid]))

class ResponseHandler(BaseHandler):
    async def post(self, did, qid):
        rid_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        response = tornado.escape.json_decode(self.request.body)["response"]
        if not "responses" in docmap[did]["questions"]:
            docmap[did]["questions"]["responses"] = {}
        rentry = {"response": response, "id": rid_str}
        docmap[did]["questions"][qid]["responses"][rid_str] = rentry
        self.write(json.dumps(rentry))

    async def get(self, did, qid, rid):
        self.write(json.dumps(docmap[did]["questions"][qid]["responses"][rid]))

class FeedbackHandler(BaseHandler):
    async def post(self, did, qid, rid):
        fid_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        ### Create a feedback based on the file content, question, answer in did
        ### Make sure it is async
        feedback = "Text feedback"
        feedback_ok = True
        if not "questions" in docmap[did]:
            docmap[did]["questions"][qid]["responses"][rid]["feedback"] = {}
        fentry = {"feedback": feedback,"feedback_ok": feedback_ok, "id": fid_str}
        docmap[did]["questions"][qid]["responses"][rid]["feedback"][fid_str] = fentry
        self.write(json.dumps(fentry))

    async def get(self, did, qid, fid):
        self.write(json.dumps(docmap[did]["questions"][qid]["responses"][rid]["feedback"][fid]))


async def main():
    application = Application([
        (r"/", DefaultHandler),
        (r"/backend/doc", DocHandler),
        (r"/backend/doc/(?P<did>.+)/", DocHandler),
        (r"/backend/doc/(?P<did>.+)/question/", QuestionHandler),
        (r"/backend/doc/(?P<did>.+)/question/(?P<qid>.+)/", QuestionHandler),
        (r"/backend/doc/(?P<did>.+)/question/(?P<qid>.+)/response", ResponseHandler),
        (r"/backend/doc/(?P<did>.+)/question/(?P<qid>.+)/response/(?P<rid>.+)", ResponseHandler),
        (r"/backend/doc/(?P<did>.+)/question/(?P<qid>.+)/response/(?P<rid>.+)/feedback", FeedbackHandler),
        (r"/backend/doc/(?P<did>.+)/question/(?P<qid>.+)/response/(?P<rid>.+)/feedback/(?P<fid>.+)", FeedbackHandler)
    ], autoreload=True)
    application.listen(8888)
    shutdown_event = asyncio.Event()
    print("Listening on 8888")
    await shutdown_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
