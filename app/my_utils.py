
from flask import redirect, url_for
from werkzeug.wrappers import Response


def redirect_to(view, **v_values) -> Response:
    return redirect(url_for(view, **v_values))
