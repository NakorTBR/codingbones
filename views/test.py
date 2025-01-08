from codingbones.models.templatesmodel import TemplatesModel
from pyramid.view import view_config # type: ignore
from pyramid.response import Response # type: ignore
from sqlalchemy.exc import SQLAlchemyError # type: ignore
import deform # type: ignore
import colander # type: ignore
import pprint
import sys
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
import datetime

from .. import models

# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL
# from sqlalchemy.orm import sessionmaker

import transaction # type: ignore
from codingbones.models import get_tm_session

from sqlalchemy import select # type: ignore

PY3 = sys.version_info[0] == 3
PY38MIN = sys.version_info[0] == 3 and sys.version_info[1] >= 8

if PY3:

    def unicode(val, encoding="utf-8"):
        return val

formatter = HtmlFormatter(nowrap=True)
css = formatter.get_style_defs()

from .auth import logged_user, logged_id

# def my_safe_repr(obj, context, maxlevels, level, sort_dicts=True):
#     if type(obj) == unicode:
#         obj = obj.encode("utf-8")

#     # Python 3.8 changed the call signature of pprint._safe_repr.
#     # by adding sort_dicts.
#     if PY38MIN:
#         # return pprint._safe_repr(obj, context, maxlevels, level, sort_dicts)
#         return pprint.pp(obj, stream=context, depth=maxlevels, indent=level)
#     else:
#         return pprint._safe_repr(obj, context, maxlevels, level)


class DeformDemo(object):
    def __init__(self, request):
        self.request = request
        # self.macros = get_renderer("templates/main.pt").implementation().macros

    def render_form(
        self,
        form,
        appstruct=colander.null,
        submitted="submit",
        success=None,
        readonly=False,
        is_i18n=False,
    ):

        captured = None

        if submitted in self.request.POST:
            # the request represents a form submission
            try:
                controls = self.request.POST.items()
                captured = form.validate(controls)
                if success:
                    success_message = success()  # Call the success function
                    sesh = self.request.dbsession

                    print(captured)

                    # NOTE: This WILL cause an error if it already exists.  Always check first,
                    # although really the user should be created when an account is opened, and 
                    # a model should never be added to a user that does not exist.  Idealy.
                    # simple_test = TestModel(name="Nakor", age=44, base_template="int main(foo)")
                    # self.request.dbsession.add(simple_test)

                    # Doing a query to retrieve a specific entry
                    q = sesh.query(TemplatesModel)
                    # located = q.filter(TestModel.name == "Test Name").first()
                    # print(f"Located record template is: {located.base_template}")
                    # exist_test = q.filter(TemplatesModel.name == captured["farking"]["name"]).first() # Name is being removed
                    # if exist_test:
                    #     print(f"User found:  {exist_test.name}")
                    # else:
                        # Not creating a new user here.  When an account is created the user will
                        # be added to the DB there.
                        # print("User does not exist!")

                    # Doing a query to update an entry
                    # update_me = q.filter(TemplatesModel.name == captured["farking"]["name"])
                    
                    # Whatver form was submitted all that will need to change will be the first 
                    # dictionary name (as in "farking" here).
                    # update_me.update({TemplatesModel.base_template: captured["farking"]["template"]})

                    # Select owned by user
                    # User ID can be cached and user objects can be selected using it
                    template_by_owner = q.filter(TemplatesModel.user_id == 1).first()
                    print(f"Selected: {template_by_owner.class_template}")

                    # exists_criteria = (
                    #     select(TemplatesModel.base_template).where(TemplatesModel.user_id == 1).exists()
                    # )
                    # stmt = select(TemplatesModel.base_template).where(exists_criteria)
                    # print(stmt)

                    # Invalid entry attempt
                    fail = q.filter(TemplatesModel.base_template == "Does Not Exist").first()
                    if fail:
                        print(f"How will it fail?  {fail.base_template}")
                    else:
                        print("Object was invalid")

                    # print(captured["template"])

                    # Must use this rather than dbsession to commit.
                    transaction.commit()
                    # self.request.dbsession.commit()
                    # self.request.dbsession.flush()

                    return {
                        "rendered_form": form.render(captured),
                        "captured": captured,
                        "css_links": form.get_widget_resources()["css"],
                        "js_links": form.get_widget_resources()["js"],
                        "project": "codingbones",
                        "success_message": success_message, # Include the success message
                    }
                html = form.render(captured) # This is the line that was missing before.
            except deform.ValidationFailure as e:
                # the submitted values could not be validated
                html = e.render()

        else:
            # the request requires a simple form rendering
            html = form.render(appstruct, readonly=readonly)

        if self.request.is_xhr:
            return Response(html)

        # code, start, end = self.get_code(2)
        # locale_name = get_locale_name(self.request)

        reqts = form.get_widget_resources()

        printer = pprint.PrettyPrinter()
        # printer.format = my_safe_repr
        output = printer.pformat(captured)
        captured = highlight(output, PythonLexer(), formatter)

        # if success is not None and callable(success):
        #     success_message = success()
        #     print(f"-=-=-=-=-=-=--={success_message}=-=-=-=-=-=-=-=-=-=")

        # values passed to template for rendering
        return {
            "rendered_form": html, # Important that this matches the var name in the PT.
            "captured": captured,
            "css_links": reqts["css"],
            "js_links": reqts["js"],
            "project": "codingbones",
            "success_message": None,
        }
    
    @view_config(route_name='test', renderer='codingbones:templates/test_template.pt')
    def ajaxform(self):
        # return Response("Thanks!")
        # This class can be named whatever, but what it is named will be shown as the section title.
        # Maybe this can be disabled, I'm not sure yet.
        user = self.request.identity
        if user is None:
            print("User is not logged in!")
        else:
            print(f"{user} is logged in.")

        # Login testing.  Still no good.
        # KA_$47
        if logged_id != -1 and logged_user != "":
            print(f"{logged_user} is logged in with the user ID of {logged_id}")
        else:
            print(f"Fail: User is {logged_user} with ID of {logged_id}")
        
        # def is_authenticated():
        #     if logged_id != -1 and logged_user != "":
        #         return True
        #     else:
        #         return False

        class Farking(colander.Schema):
            name = colander.SchemaNode(
                colander.String(), description="Content name"
            )
            date = colander.SchemaNode(
                colander.Date(),
                widget=deform.widget.DatePartsWidget(),
                description="Content date",
            )
            template = colander.SchemaNode(
                colander.String(), widget=deform.widget.RichTextWidget()
            )
        
        class Schema(colander.Schema):
            # Each mapping object (like Farking) will be included in the schema here.
            farking = Farking(title="Template Update",
                widget=deform.widget.MappingWidget(template="mapping_accordion", open=True))
            
        
        schema = Schema()
        form = deform.Form(schema, buttons=("submit",), use_ajax=True)

        def succeed():
            now = datetime.datetime.now()
            # timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            return f'Template updated @{timestamp}'
        
        # No longer getting an exception, but the form return is NOT inline.
        # TODO: MUST be inline return.
        # One colour for success, and red or something for error.
        # So it is technically inline, except that it is rewriting the entire page that is rendered.
        # Will have to figure it out tomorrow I think.
        # Or tomorrow lol.
        return self.render_form(form, success=succeed)