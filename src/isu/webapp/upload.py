from isu.webapp import views

_ = views._


class View(views.View):
    title = _('File upload')

    def response(self, **kwargs):
        answer = {
            "context": self.context,
            "request": self.request,
            "view":self
        }
        answer.update(kwargs)
        return answer

    def form(self):
        return self.response()

    def upload(self):
        request = self.request
        post = request.POST
        response = request.response
        response.status_code=201
        file = post.get('file', None)
        if file is None or file.filename is None:
            response.status_code=400
            return {'error': 'no file',
                    'result': 'KO',
                    'explanation':
                    _('check input form if it contains "file" field of type file')}
        self.file = file
        return {'error':None, 'result':'OK', 'filename':file.filename}

    def doc_list(self):
        return self.response()
