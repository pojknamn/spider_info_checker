import ast

import libcst as cst

from .checkers import is_spider
from .errors import ErrMessages
from .visitors import CollectSpiderNames


def update_errors_list(error_msg, error_list, spider_name):
    err_msg = "\n".join(error_msg.args[0])
    error_list.append(ErrMessages.spiders_info_invalid.format(message=f"{spider_name}\n{err_msg}"))


def load_pairs(diff_list: list) -> set:
    pairs = set()
    for file in diff_list:
        if pair := is_spider(file):
            pairs.add(pair)
    return pairs


def update_sprider_names(spider: str, spider_names: set) -> None:
    with open(spider, 'r') as spider_file:
        spider_syntax_tree = cst.parse_module(spider_file.read())
        spider_syntax_tree.visit(CollectSpiderNames(spider_names))


def ast_from_constant(constant: str) -> ast.Module:
        with open(constant, "r") as constant_file:
            constant_syntax_tree = ast.parse(constant_file.read())
        return constant_syntax_tree
