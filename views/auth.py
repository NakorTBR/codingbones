from pyramid.csrf import new_csrf_token # type: ignore
from pyramid.httpexceptions import HTTPSeeOther # type: ignore
from pyramid.security import ( # type: ignore
    remember,
    forget,
)
from pyramid.view import ( # type: ignore
    forbidden_view_config,
    view_config,
)

from .. import models

logged_user = ""
logged_id = -1


@view_config(route_name='login', renderer='codingbones:templates/login.pt')
def login(request):
    message = ''
    login = ''
    next_url = request.route_url('test')  # TODO: Correct this to default / main page
    if request.method == 'POST':
        login = request.params['login']
        password = request.params['password']
        user = (
            request.dbsession.query(models.UsersModel)
            .filter_by(user_name=login)
            .first()
        )
        if user is not None and user.user_pass == password:
            new_csrf_token(request)
            global logged_user
            logged_user = login
            global logged_id
            logged_id = user.id
            print(f"LOGGED ID: {logged_id}")
            print(f"\n\nReq:\n{request}\n\n")
            headers = remember(request, user.id)
            request.response.headers.extend(headers)
            print(f"Headers: \n{headers}")
            next_url = request.route_url('test') # TODO: Correct this to default / main page
            print(f"Logging in user... ({user.id})")
            return HTTPSeeOther(location=next_url, headers=headers)
        print("Login has somehow failed.")
        message = 'Failed login'
        request.response.status = 400

    return dict(
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
    )

@view_config(route_name='logout')
def logout(request):
    next_url = request.route_url('/test')
    if request.method == 'POST':
        new_csrf_token(request)
        headers = forget(request)
        return HTTPSeeOther(location=next_url, headers=headers)

    return HTTPSeeOther(location=next_url)

# @forbidden_view_config(renderer='codingbones:templates/login.pt')
# def forbidden_view(exc, request):
#     if not request.is_authenticated:
#         next_url = request.route_url('login', _query={'next': request.url})
#         return HTTPSeeOther(location=next_url)

#     request.response.status = 403
#     return {}