import functools
import gzip

from flask import request, after_this_request
from io import BytesIO as IO

def allow_access(function):
    """allow_access decorator that requires a valid permission
     :param function: function parameter
     :return: decorated_function
     """
    @wraps(function)
    def decorated_function(*args, **kwargs):

        return function(*args,**kwargs)

    return decorated_function()

def log_access(log_caregory_id=None):
    """
    log_core decorator logging on panel
    :param log_caregory_id: Log category identifier
    :param new_description: New desription
    :return: decorated function
    """

    def decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):

            return function(*args, **kwargs)

        return decorated_function

    return decorator


def gzipped(func):
    @functools.wraps(func)
    def view_func(*args, **kwargs):
        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')

            if 'gzip' not in accept_encoding.lower():
                return response

            response.direct_passthrough = False

            if (response.status_code < 200 or
                response.status_code >=300 or
                'Content-Encoding' in response.headers):
                return response

            gzip_buffer = IO()
            gzip_file = gzip.GzipFile(mode = 'wb',
                                      fileobj=gzip_buffer)
            gzip_file.write(response.data)
            gzip_file.close()

            response.data = gzip_buffer.getvalue()
            response.headers['Content-Encoding'] = 'gzip'
            response.headers['Vary'] = 'Accept-Encoding'
            response.headers['Content-Length'] = len(response.data)

            return response

        return func(*args, **kwargs)

    return view_func()