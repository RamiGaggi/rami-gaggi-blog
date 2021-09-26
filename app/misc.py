from flask import redirect, url_for
from werkzeug.wrappers import Response


def redirect_to(view, **v_values) -> Response:
    return redirect(url_for(view, **v_values))


def get_next_url_for_posts(url, posts, **kwargs):
    return url_for(url, page=posts.next_num, **kwargs) if posts.has_next else None


def get_previous_url_for_posts(url, posts, **kwargs):
    return url_for(url, page=posts.prev_num, **kwargs) if posts.has_prev else None
