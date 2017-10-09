import os
import quickproxy
import json
import settings

def callback(request):
    request.host = settings.HOST
    request.port = settings.PORT
    return request

rules = json.loads(open(settings.RULES_FILE).read())

quickproxy.run_proxy(port=settings.PORT, req_callback=callback)
