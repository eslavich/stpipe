import sys

import traitlets

from .extern.configobj import validate


def config_obj_to_traitlets(config_obj):
    validator = validate.Validator()

    traitlets = {}
    for parameter, check in config_obj.items():
        fun_name, fun_args, fun_kwargs, default = validator._parse_check(check)
        if default is None:
            default = traitlets.Undefined
            allow_none = False
        else:
            default = validator._handle_none(default)
            allow_none = default is None

        inline_comment = config_obj.inline_comments.get(parameter)
        if inline_comment is None:
            help = None
        else:
            help = inline_comment.lstrip("#").strip()

        if fun_name in _CONFIG_OBJ_FUNC_TO_HANDLER:
            traitlets[parameter] = _CONFIG_OBJ_FUNC_TO_HANDLER[fun_name](default, allow_none, help, *fun_args, **fun_kwargs)
        else:
            raise ValueError(f"Unsupported Step spec function: {fun_name}")

    return traitlets


def _handle_pass(default, allow_none, help):
    return traitlets.Any(
        default_value=default,
        allow_none=allow_none,
        help=help,
    )


def _handle_integer(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_integer(default, min=min, max=max)

    return traitlets.Integer(
        default_value=default,
        allow_none=allow_none,
        help=help,
        min=min,
        max=max,
    )


def _handle_float(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_float(default, min=min, max=max)

    return traitlets.Float(
        default_value=default,
        allow_none=allow_none,
        help=help,
        min=min,
        max=max,
    )


def _handle_boolean(default, allow_none, help):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_boolean(default)

    return traitlets.Bool(
        default_value=default,
        allow_none=allow_none,
        help=help,
    )


def _handle_string(default, allow_none, help, min=None, max=None):
    if min is not None or max is not None:
        raise ValueError("Step spec string with min or max is unsupported")

    if default is not traitlets.Undefined and default is not None:
        default = validate.is_string(default)

    return traitlets.Unicode(
        default_value=default,
        allow_none=allow_none,
        help=help,
    )


def _handle_list(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_list(default, min=min, max=max)

    return traitlets.List(
        default_value=default,
        allow_none=allow_none,
        help=help,
        minlen=min or 0,
        maxlen=max or sys.maxsize,
    )


def _handle_int_list(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_int_list(default, min=min, max=max)

    return traitlets.List(
        traitlets.Integer(),
        default_value=default,
        allow_none=allow_none,
        help=help,
        minlen=min or 0,
        maxlen=max or sys.maxsize,
    )


def _handle_float_list(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_float_list(default, min=min, max=max)

    return traitlets.List(
        traitlets.Float(),
        default_value=default,
        allow_none=allow_none,
        help=help,
        minlen=min or 0,
        maxlen=max or sys.maxsize,
    )


def _handle_bool_list(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_float_list(default, min=min, max=max)

    return traitlets.List(
        traitlets.Bool(),
        default_value=default,
        allow_none=allow_none,
        help=help,
        minlen=min or 0,
        maxlen=max or sys.maxsize,
    )


def _handle_string_list(default, allow_none, help, min=None, max=None):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_string_list(default, min=min, max=max)

    return traitlets.List(
        traitlets.Unicode(),
        default_value=default,
        allow_none=allow_none,
        help=help,
        minlen=min or 0,
        maxlen=max or sys.maxsize,
    )


def _handle_option(default, allow_none, help, *options):
    if default is not traitlets.Undefined and default is not None:
        default = validate.is_option(default, *options)

    return traitlets.Enum(
        options,
        default_value=default,
        allow_none=allow_none,
        help=help,
    )


# ip_addr, ip_addr_list, mixed_list, and force_list are unsupported:
_CONFIG_OBJ_FUNC_TO_HANDLER = {
    "": _handle_pass,
    "integer": _handle_integer,
    "float": _handle_float,
    "boolean": _handle_boolean,
    "string": _handle_string,
    "list": _handle_list,
    "tuple": _handle_list,
    "int_list": _handle_int_list,
    "float_list": _handle_float_list,
    "bool_list": _handle_bool_list,
    "string_list": _handle_string_list,
    "pass": _handle_pass,
    "option": _handle_option,
    # Hmm.. what to do about these:
    "input_file": _handle_string,
    "output_file": _handle_string,

}