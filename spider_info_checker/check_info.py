import sys

from spider_info_checker.checkers import check_terms_n_urls, find_spider_info
from spider_info_checker.errors import ErrMessages, NoSpiderInfo
from spider_info_checker.misc import ast_from_constant, load_pairs, update_spider_names
from spider_info_checker.transformers import update_spiders_info
from spider_info_checker.validators import validate_spiders_info


def main():
    files = sys.argv[1:]
    files = load_pairs(files)
    errors_to_fix = []
    for spider, constant in files:
        spider_names = set()
        wrong_names_in_info = set()
        constant_syntax_tree = ast_from_constant(constant)
        update_spider_names(spider, spider_names)
        check_terms_n_urls(constant_syntax_tree, constant, errors_to_fix)
        spiders_info = find_spider_info(constant_syntax_tree, constant, errors_to_fix)

        if spiders_info:
            spiders_info_names = set(spiders_info.keys())
            spider_names = set(spider_names)
            spiders_without_info = spider_names.difference(spiders_info_names)
            wrong_names_in_info = spiders_info_names.difference(spider_names)
        else:
            spiders_without_info = spider_names

        if spiders_without_info:
            errors_to_fix.append(
                ErrMessages.missing_info.format(spiders_without_info=spiders_without_info)
            )
            update_spiders_info(spiders_info, spiders_without_info, const_file=constant)

        if wrong_names_in_info:
            errors_to_fix.append(
                ErrMessages.wrong_spider_names.format(wrong_names_in_info=wrong_names_in_info)
            )

        if spiders_info and not isinstance(spiders_info, list):
            validate_spiders_info(spiders_info, errors_to_fix, wrong_names_in_info)

    if errors_to_fix:
        print(ErrMessages.list_of_errors)
        print("*" * 20)
        print("\n".join(errors_to_fix))
        print("*" * 20)
        raise NoSpiderInfo(ErrMessages.wish_message)


if __name__ == "__main__":
    main()
