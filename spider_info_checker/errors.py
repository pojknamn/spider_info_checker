from sys import platform


class NoSpiderInfo(BaseException):
    pass


class NotValidSpiderInfo(BaseException):
    pass


class StartUrlsAreNotEmpty(BaseException):
    pass


class ErrMessages:
    spiders_info = "Проверь спайдерс инфо в {constant_path}, некорректное название, либо его нет"
    comment_urls_or_terms = "Пожалуйста закомментируй все {error_type} в {error_location}\n"
    spiders_info_invalid = "Спайдерс инфо {message}"
    remove_or_rename = ' удали или переименуй!'
    list_of_errors = "Cписок ошибок: \n\n"
    wish_message = "Все поправимо!"
    missing_info = "Тут нехватает инфы для {spiders_without_info}"
    wrong_spider_names = "Это здесь лишнее {wrong_names_in_info}"
    if platform != 'linux':
        spiders_info = "Check spiders info in {constant_path}, its missed or wrong name"
        comment_urls_or_terms = "Please, comment all {error_type} in {error_location}\n"
        spiders_info_invalid = "Spiders info {message}"
        remove_or_rename = ' remove or rename!'
        list_of_errors = "Errors list: \n\n"
        wish_message = "There is no big deal!"
        missing_info = "There is missing items in spiders info {spiders_without_info}"
        wrong_spider_names = "This isn`t from here {wrong_names_in_info}"
