from pyramid.config import Configurator

# DB error:  Not properly configured.  (does not exist).
# TODO: Redo DB setup with better instructions.
# Bit of an emergency, doing a push because I can't remember what I've changed.
# I think most of it is outside the repo, but here we are.
# Taking the day off.  Haven't taken a day off in 47 days.
# I know if someone looks at these commits it will look like I've just been pretending to work,
# but all of the work was in files that do not get commited due to security.  Everything is currently 
# working (finally), and tommorrow I can start pushing actual code.
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.models')
        config.scan()
    return config.make_wsgi_app()
