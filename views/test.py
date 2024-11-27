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
                # try to validate the submitted values
                controls = self.request.POST.items()
                captured = form.validate(controls)
                if success:
                    response = success()
                    if response is not None:
                        return response
                html = form.render(captured)
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

        # reqts = form.get_widget_resources()

        # printer = pprint.PrettyPrinter()
        # printer.format = my_safe_repr
        # output = printer.pformat(captured)
        # captured = highlight(output, PythonLexer(), formatter)

        # values passed to template for rendering
        return {
            # "form": html,
            # "captured": captured,
            # "code": code,
            # "start": start,
            # "end": end,
            # "is_i18n": is_i18n,
            # "locale": locale_name,
            # "demos": self.get_demos(),
            # "title": self.get_title(),
            # "css_links": reqts["css"],
            # "js_links": reqts["js"],
        }
    
    @view_config(route_name='test', renderer='codingbones:templates/test_template.pt')
    def ajaxform(self):
        # return Response("Thanks!")
        class Mapping(colander.Schema):
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
            mapping = Mapping()
            richtext = colander.SchemaNode(
                colander.String(), widget=deform.widget.RichTextWidget()
            )
        
        schema = Schema()
        form = deform.Form(schema, buttons=("submit",), use_ajax=True)

        def succeed():
            return Response('<div id="thanks">Thanks!</div>')

        # Have drilled down to this as the cuplrit.
        # Getting a name error "NameError: project" (whatever that means).
        # It seems that when this is being returned it is clasing with the PT?  Not sure.
        # Still feeling terrible from yesterday's hospital stay.
        return self.render_form(form, success=succeed)