from flask_restful import reqparse, abort
from models.base import BaseModel


def add_arguments(args: list) -> reqparse.RequestParser:
    """
    :param args: list of dicts with the arguments to be parsed
    :return: reqparse.RequestParser
    """
    parser = reqparse.RequestParser()
    for arg in args:
        parser_args = {
            'name': arg['name'],
            'type': arg['type'],
            'required': arg['required'],
            'help': arg['help'] if 'help' in arg else None
        }
        if 'location' in arg:
            parser_args['location'] = arg['location']
        parser.add_argument(**parser_args)
    return parser


def check_key(key: str) -> None:
    """
    Check if key is valid
    :param key:
    :raises HTTPException: if key is not valid
    """
    if key != 'verysecretkey':
        abort(401, message='Não autorizado')


def rename_dict_keys(old_dict: dict, old_new_keys: dict) -> dict:
    """
    Rename dict keys based on a dict with pairs of old and new keys
    :param old_new_keys:
    :param old_dict:
    :return: renamed dict
    :raises KeyError: if old key is not found in the dict
    """
    for old_key, new_key in old_new_keys.items():
        if old_dict.get(old_key):
            old_dict[new_key] = old_dict[old_key]
            old_dict.pop(old_key, None)
    return old_dict  # new dict with renamed keys


def update_fields(from_: dict, to: BaseModel | object, fields_to_pop: list = None) -> BaseModel | object:
    """
    Update a model attributes with a dict values
    :param from_: dict with values to update
    :param to: model to update
    :param fields_to_pop: list of fields to pop from the dict
    :return: tuple with the updated dict and the status code
    """
    common_fields_to_pop = ['key', 'id']
    if fields_to_pop:
        common_fields_to_pop.extend(fields_to_pop)

    for field in common_fields_to_pop:
        from_.pop(field, None)

    to.update(**from_)
    to.commit()
    return to


def find_or_abort(model: BaseModel | object, id: int, message: str = None) -> BaseModel | object:
    """
    Find a model by id or abort with 404
    :param model:
    :param id:
    :param message: Message to be displayed in the abort
    :return: model object
    """
    if not message:
        message = f'{model.__name__} não encontrado'
    obj = model.get_by_id(id)
    if not obj:
        abort(404, message=message)
    return obj


# def find_or_abort(model: BaseModel | object, method_name: str, *args, **kwargs) \
#         -> BaseModel | object | list[BaseModel] | list[object]:
#     """
#     Call a method from a model or abort with 404 if not there's no result
#     :param model:
#     :param method_name:
#     :param args:
#     :param kwargs:
#     :return: A model object or a list of model objects
#     """
#     method = getattr(model, method_name, None)
#
#     if not callable(method):
#         abort(500, message=f'Método {method_name} não encontrado em {model.__name__}')
#
#     result = method(*args, **kwargs)
#
#     if not result:
#         abort(404, message=f'{model.__name__} não encontrado')
#
#     return result
