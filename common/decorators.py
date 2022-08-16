from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from marshmallow import Schema


def request_schema(schema: Schema):
    def decorator(func):
        def _wrapper(request):
            request_data = schema().loads(request)
            return func(**request_data)

        return _wrapper

    return decorator


def response_schema(
    schema: Schema, *, many: Optional[bool] = False, status_code: Optional[int] = 200
):
    def decorator(func):
        def _wrapper(*args, **kwargs):
            response_data = func(*args, **kwargs)
            response = schema().dumps(response_data, many=many)
            return response

        return _wrapper

    return decorator
