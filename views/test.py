from codingbones.models.testmodel import TestModel
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

import transaction
from codingbones.models import get_tm_session

PY3 = sys.version_info[0] == 3
PY38MIN = sys.version_info[0] == 3 and sys.version_info[1] >= 8

if PY3:

    def unicode(val, encoding="utf-8"):
        return val

formatter = HtmlFormatter(nowrap=True)
css = formatter.get_style_defs()

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

                    # Write to DB
                    # url = URL.create(
                    #     drivername="postgresql",
                    #     username="nakor",
                    #     host="/tmp/postgresql/socket",
                    #     database="codingbones"
                    # )

                    # engine = create_engine(url)
                    # connection = engine.connect()

                    # print(f"-=-=-=-=-=-=-=-=-=- {self.request.tm}")
                    # self.request.config.include('codingbones.models')
                    # tm = transaction.TransactionManager(explicit=True)
                    # tm = self.request.tm
                    # with tm:
                    #     dbsession = get_tm_session(self.request.config.registry['dbsession_factory'], tm)

                    # Data went into the table on refresh.  Obviously don't love that but whatever.
                    # Now we will have to check for duplicate entries and update template instead if it exists.
                    simple_test = TestModel(name="Test Name", age=446, base_template="int main(foo)")
                    self.request.dbsession.add(simple_test)
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
        class Farking(colander.Schema):
            name = colander.SchemaNode(
                colander.String(), description="Content name"
            )
            date = colander.SchemaNode(
                colander.Date(),
                widget=deform.widget.DatePartsWidget(),
                description="Content date",
            )
        
        class Schema(colander.Schema):
            number = colander.SchemaNode(colander.Integer())
            farking = Farking(title="Open by default",
                widget=deform.widget.MappingWidget(template="mapping_accordion", open=True))
            richtext = colander.SchemaNode(
                colander.String(), widget=deform.widget.RichTextWidget()
            )
        
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