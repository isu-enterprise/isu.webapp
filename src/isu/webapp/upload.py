from isu.webapp import views

_ = views._


class View(views.View):
    title = _('File upload')

    def response(self, **kwargs):
        answer = {
            "context": self.context,
            "request": self.request,
        }
        answer.update(kwargs)
        return answer

    def form(self):
        return self.response()

    def upload(self):
        return self.response()

    def doc_list(self):
        return self.response()
