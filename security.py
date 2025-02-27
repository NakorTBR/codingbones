from pyramid.authentication import AuthTktCookieHelper # type: ignore
from pyramid.csrf import CookieCSRFStoragePolicy # type: ignore
from pyramid.request import RequestLocalCache # type: ignore

from . import models

import logging
logger = logging.getLogger(__name__)

# TEST
# No print or logger statements are being output from this file.
# Likely indication something is wrong af.
# FA2248
import sys
print(sys.path)

class MySecurityPolicy:
    def __init__(self, secret):
        self.authtkt = AuthTktCookieHelper(secret)
        self.identity_cache = RequestLocalCache(self.load_identity)
        logger.debug(f"-=-=-=-=-=-=-Log level: {logger.level}") 

    def load_identity(self, request):
        identity = self.authtkt.identify(request)
        if identity is None:
            return None

        userid = identity['userid']
        user = request.dbsession.query(models.UsersModel).get(userid)
        # Update the cache
        if user:
            self.identity_cache.put(request, user)
        return user

    def identity(self, request):
        return self.identity_cache.get_or_create(request)

    def authenticated_userid(self, request):
        user = self.identity(request)
        if user is not None:
            return user.id

    def remember(self, request, userid, **kw):
        return self.authtkt.remember(request, userid, **kw)

    def forget(self, request, **kw):
        return self.authtkt.forget(request, **kw)

def includeme(config):
    settings = config.get_settings()

    config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
    config.set_default_csrf_options(require_csrf=True)

    config.set_security_policy(MySecurityPolicy(settings['auth.secret']))