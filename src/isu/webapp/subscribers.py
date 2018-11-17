from pyramid.renderers import get_renderer


def add_base_template(event):
    """Add base templates.
    """
    main = get_renderer('templates/index.pt').implementation()
    #test = get_renderer('templates/main.pt').implementation()
    #email_main = get_renderer('templates/email/main.pt').implementation()
    email_main = False
    request = event["req"]
    event.update({'main': main,  # 'test': test,
                  "default": True,
                  "nothing": "",
                  "request": request,
                  "response": request.response
                  })
