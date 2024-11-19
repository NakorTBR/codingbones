from pyramid.config import Configurator

# DB error:  Not properly configured.  (does not exist).
# TODO: Redo DB setup with better instructions.
# Bit of an emergency, doing a push because I can't remember what I've changed.
# I think most of it is outside the repo, but here we are.
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.models')
        config.scan()
    return config.make_wsgi_app()
