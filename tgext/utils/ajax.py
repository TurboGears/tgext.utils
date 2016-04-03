from tg import request, abort, override_template
from tg.decorators import before_validate, before_render


@before_validate
def ajax_only(*args, **kwargs):
    if not request.is_xhr:
        abort(400)


def ajax_expose(template):
    @before_render
    def _ajax_expose(*args, **kwargs):
        if request.is_xhr:
            override_template(request.controller_state.method, template)
    return _ajax_expose
