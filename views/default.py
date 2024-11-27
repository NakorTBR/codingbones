from pyramid.view import view_config # type: ignore
from pyramid.response import Response # type: ignore
from sqlalchemy.exc import SQLAlchemyError # type: ignore
import deform # type: ignore
import colander # type: ignore

from .. import models

class ExampleSchema(deform.schema.CSRFSchema):

    name = colander.SchemaNode(
        colander.String(),
        title="Name")

    age = colander.SchemaNode(
        colander.Int(),
        default=18,
        title="Age",
        description="Your age in years")
    
    ntemplate = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(max=800),
        widget=deform.widget.TextAreaWidget(rows=10, cols=60),
        title = "Template",
        description = "Modify template if you wish for a different structure"
    )

@view_config(route_name='home', renderer='codingbones:templates/mytemplate.pt')
def my_view(request):
    
    try:
        query = request.dbsession.query(models.MyModel)
        one = query.filter(models.MyModel.name == 'one').one()

        # Testing code.
        schema = ExampleSchema().bind(request=request)
        process_btn = deform.form.Button(name='process', title="Process")
        form = deform.form.Form(schema, buttons=(process_btn,), use_ajax=True)
        rendered_form = form.render()
        # Testing accessing the data from the post.
        # print(list(request.POST.items()))

        # def succeed():
        #     return Response('<div id="thanks">Thanks!</div>')

        # return render_form(form, success=succeed)

        if 'submit' in request.POST: # detect that the submit button was clicked
            print("VERY NOTICEABLE TEXT HERE")
            controls = request.POST.items() # get the form controls

            try:
                appstruct = form.validate(controls)  # call validate
            except ValidationFailure as e: # catch the exception
                return {'form':e.render()} # re-render the form with an exception

            print(f"Base template is: {appstruct['base_template']}")
            # the form submission succeeded, we have the data
            return {'form':None, 'appstruct':appstruct}
        
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {
        'one': one, 
        'project': 'codingbones',
        "rendered_form": rendered_form,
        }


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
