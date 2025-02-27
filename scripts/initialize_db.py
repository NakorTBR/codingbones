import argparse
from datetime import datetime
import sys

from pyramid.paster import bootstrap, setup_logging # type: ignore
from sqlalchemy.exc import OperationalError # type: ignore

# from .. import models
from ..models import MyModel, UsersModel, TemplatesModel


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    model = MyModel(name='one', value=1)
    dbsession.add(model)
    test_user = UsersModel(user_name = "Nakor", user_pass = "FakePass", 
                                             user_email = "null@null.com", user_join_date = datetime.now())
    dbsession.add(test_user)
    test_model = TemplatesModel(base_template = "int main()")
    dbsession.add(test_model)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
