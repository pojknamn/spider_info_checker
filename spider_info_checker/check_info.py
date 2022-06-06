from pprint import pprint

from .checkers import check_terms_n_urls, find_spider_info
from .config import *
from .errors import ErrMessages, NoSpiderInfo
from .misc import ast_from_constant, load_pairs, update_sprider_names
from .templates import spider_info_from_template
from .validators import validate_spiders_info


def main():
    files = sys.argv[1:]
    files = load_pairs(files)
    spider_names = set()
    spiders_info = []
    errors_to_fix = []
    wrong_names_in_info = set()
    spiders_without_info = set()
    for spider, constant in files:
        constant_syntax_tree = ast_from_constant(constant)
        update_sprider_names(spider, spider_names)
        check_terms_n_urls(constant_syntax_tree, constant, errors_to_fix)
        try:
            spiders_info = find_spider_info(constant_syntax_tree, constant, errors_to_fix)
            spiders_info_names = set(spiders_info.keys())
            spider_names = set(spider_names)
            spiders_without_info = spider_names.difference(spiders_info_names)
            wrong_names_in_info = spiders_info_names.difference(spider_names)
            if spiders_without_info:
                errors_to_fix.append(
                    ErrMessages.missing_info.format(spiders_without_info=spiders_without_info)
                )
            if wrong_names_in_info:
                errors_to_fix.append(
                    ErrMessages.wrong_spider_names.format(wrong_names_in_info=wrong_names_in_info)
                )
        except NoSpiderInfo as err_message:
            spiders_without_info = spider_names
            errors_to_fix.append(err_message)
        if spiders_info and not isinstance(spiders_info, list):
            validate_spiders_info(spiders_info, errors_to_fix, wrong_names_in_info)

    if errors_to_fix:
        print(ErrMessages.list_of_errors)
        print("*" * 20)
        print("\n".join(errors_to_fix))
        print("*" * 20)
        if spiders_without_info:
            pprint(spider_info_from_template(spiders_without_info), sort_dicts=False)
        raise NoSpiderInfo(ErrMessages.wish_message)


if __name__ == "__main__":
    main()

