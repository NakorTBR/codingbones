from pyramid.config import Configurator # type: ignore
from pyramid.session import SignedCookieSessionFactory # type: ignore

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
    with Configurator(settings=settings, session_factory=my_session_factory) as config:
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.models')
        config.scan()
    return config.make_wsgi_app()
