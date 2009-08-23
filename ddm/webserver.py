"""
The boilerplate behind the resources.  Start services and shit like that.
"""
from twisted.application import internet
from twisted.python import log

from nevow import appserver
from util import RESOURCE

from nevow import (rend, url, static, loaders, athena)

class Root(rend.Page):
    """
    Adds child nodes for things common to anonymous and logged-in root
    resources.
    """
    addSlash = True # yeah, we really do need this, otherwise 404 on. /
    
    def child_static(self, ctx):
        return static.File(RESOURCE('static'))

    def child_app(self, ctx):
        return static.File(RESOURCE('template/sample.html'))

    def renderHTTP(self, ctx):
        return url.root.child("app")

class WebSite(appserver.NevowSite):
    """Website with <80 column logging"""
    def __init__(self, *a, **kw):
        appserver.NevowSite.__init__(self, Root(), *a, **kw)

    def log(self, request):
        uri = request.uri

        if 'jsmodule' in uri:
            uris = uri.split('/')
            n = uris.index('jsmodule')
            uris[n-1] = uris[n-1][:3] + '...'
            uri = '/'.join(uris)

        if len(uri) > 38:
            uri = '...' + uri[-35:]

        code = request.code
        if code != 200:
            code = '!%s!' % (code, )

        log.msg('%s %s' % (code, uri), system='HTTP', )


class WebServer(internet.TCPServer):
    def startService(self, *a, **kw):
        internet.TCPServer.startService(self, *a, **kw)


