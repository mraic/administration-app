import os

from sqlalchemy import and_
from werkzeug.utils import secure_filename


def filter_data_result_with_operator(filter_name=None, attribute=None,
                                     filter_data=None):
    filter_main = and_()
    if all(v is not None for v in [attribute, filter_name, filter_data]):
        if check_filter_data(filter_name, filter_data):
            value = filter_data[filter_name]['value']
            operator = filter_data[filter_name]['operator']
            if value:
                filter_main = and_(
                    filter_main,
                    attribute.ilike(check_like_filter_operator(
                        operator, value
                    )))
    else:
        pass
    return filter_main


def filter_data_result_between_two_value(
        filter_name=None, filter_date_from=None, filter_date_to=None,
        attribute=None, filter_data=None):
    from src import AppLogException
    from src.general import Status

    filter_main = and_()
    if all(v is not None for v in [attribute, filter_name,
                                   filter_date_to, filter_data,
                                   filter_date_from]):

        if filter_name in filter_data:
            if filter_date_from in filter_data[filter_name]:
                if filter_date_to in filter_data[filter_name]:
                    date_from = filter_data[filter_name][filter_date_from] if \
                        filter_data[filter_name][filter_date_from] != '' \
                        else None
                    date_to = filter_data[filter_name][filter_date_to] if \
                        filter_data[filter_name][filter_date_to] != '' else None

                    if date_from is None:
                        if date_to is None:
                            pass
                        else:
                            filter_main = and_(
                                filter_main,
                                attribute <= date_to
                            )

                    elif date_to is None:
                        if date_from is None:
                            pass
                        else:
                            filter_main = and_(
                                filter_main,
                                attribute >= date_from)

                    else:
                        filter_main = and_(
                            filter_main,
                            attribute >= date_from,
                            attribute <= date_to
                        )
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        raise AppLogException(
            Status(400,
                   "All parameters are mandatory in filter_data_"
                   "between value function")
        )
    return filter_main


def filter_data_result_between_two_dates(
        filter_name=None, filter_date_from=None, filter_date_to=None,
        attribute=None, filter_data=None):
    from src import AppLogException
    from src.general import Status

    filter_main = and_()
    if all(v is not None for v in [attribute, filter_name,
                                   filter_date_to, filter_data,
                                   filter_date_from]):

        if filter_name in filter_data:
            if filter_date_from in filter_data[filter_name]:
                if filter_date_to in filter_data[filter_name]:
                    date_from = filter_data[filter_name][filter_date_from] if \
                        filter_data[filter_name][filter_date_from] != '' \
                        else None
                    date_to = filter_data[filter_name][filter_date_to] if \
                        filter_data[filter_name][filter_date_to] != '' else None

                    if date_from is None:
                        if date_to is None:
                            pass
                        else:
                            filter_main = and_(
                                filter_main,
                                attribute <= date_to
                            )

                    elif date_to is None:
                        if date_from is None:
                            pass
                        else:
                            filter_main = and_(
                                filter_main,
                                attribute >= date_from)

                    else:
                        filter_main = and_(
                            filter_main,
                            attribute >= date_from,
                            attribute <= date_to
                        )
                else:
                    pass
            else:
                pass
        else:
            pass
    else:
        raise AppLogException(
            Status(400,
                   "All parameters are mandatory in filter_data_"
                   "between value function")
        )
    return filter_main


def filter_data_by_condition(filter_name=None, attribute=None,
                             filter_data=None):
    filter_main = and_()
    if all(v is not None for v in [attribute, filter_name, filter_data]):
        if check_filter_data(filter_name, filter_data):
            value = filter_data[filter_name]['value']
            operator = filter_data[filter_name]['operator']

            if value:
                filter_main = and_(
                    filter_main,
                    attribute.ilike(check_like_exact_filter_operator(
                        operator, value
                    ))
                )
    else:
        pass
    return filter_main


# def filter_data_by_both_date_and_value(
#         filter_name=None, filter_date_from=None, filter_date_to=None,
#         attribute=None, filter_data=None, filter_value_from=None,
#         filter_value_to=None, attribute_2=None):
#     from src import AppLogException
#     from src.general import Status
#
#     filter_main = and_()
#
#     if all(v is not None for v in [attribute, filter_name, filter_date_to,
#                                    filter_data, filter_date_from,
#                                    attribute_2,
#                                    filter_value_from, filter_value_to]):
#
#         if filter_name in filter_data:
#             if filter_date_from in filter_data[filter_name]:
#                 if filter_date_to in filter_data[filter_name]:
#                     date_from = filter_data[filter_name][filter_date_from] if \
#                         filter_data[filter_name][filter_date_from] != '' \
#                         else None
#                     date_to = filter_data[filter_name][filter_date_to] if \
#                         filter_data[filter_name][filter_date_to] != '' else None
#
#                     if date_from is None:
#                         if date_to is None:
#                             pass
#                         else:
#                             filter_main = and_(
#                                 filter_main,
#                                 attribute <= date_to
#                             )
#                     elif date_to is None:
#                         if date_from is None:
#                             pass
#                         else:
#                             filter_main = and_(
#                                 filter_main,
#                                 attribute >= date_from)
#
#                     else:
#                         filter_main = and_(
#                             filter_main,
#                             attribute >= date_from,
#                             attribute <= date_to
#                         )
#
#                 else:
#                     pass
#             else:
#                 pass
#         else:
#             pass
#
#         if filter_name in filter_data:
#             if filter_value_from in filter_data[filter_name]:
#                 if filter_value_to in filter_data[filter_name]:
#                     value_from = filter_data[filter_name][filter_value_from] if \
#                         filter_data[filter_name][filter_value_from] != '' \
#                         else None
#                     value_to = filter_data[filter_name][filter_value_to] if \
#                         filter_data[filter_name][
#                             filter_value_to] != '' else None
#
#                     if value_from is None:
#                         if value_to is None:
#                             pass
#                         else:
#                             filter_main = and_(
#                                 filter_main,
#                                 attribute_2 <= value_to
#                             )
#                     elif value_to is None:
#                         if value_from is None:
#                             pass
#                         else:
#                             filter_main = and_(
#                                 filter_main,
#                                 attribute_2 >= value_from
#                             )
#
#                     else:
#                         filter_main = and_(
#                             filter_main,
#                             attribute_2 >= value_from,
#                             attribute_2 <= value_to
#                         )
#                 else:
#                     pass
#             else:
#                 pass
#         else:
#             pass
#     else:
#         raise AppLogException(
#             Status(400,
#                    "All parameters are mandatory in filter_data_"
#                    "between value function")
#         )
#
#     return filter_main


def check_filter_data(key, filter_data):
    if filter_data is not None:
        if key in filter_data:
            if 'value' in filter_data[key]:
                if 'operator' in filter_data[key]:
                    return True
    return False


def check_like_filter_operator(operator, value):
    if operator == 'START':
        return value + '%'
    elif operator == 'CONTAINS':
        return '%' + value + '%'
    elif operator == 'EXACT':
        return value
    elif operator == 'FINISH':
        return '%' + value


def check_like_exact_filter_operator(operator, value):
    if operator == 'EXACT':
        return value
    else:
        pass


def import_file(path=None, file=None, file_name=None):
    from src import AppLogException
    from src.general import Status
    try:
        filename = secure_filename(file_name)
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file.stream.seek(0)
        file.save(os.path.join(file_dir, path + filename))
    except Exception as e:
        raise AppLogException(
            Status.error_on_loading_file())