import ast
import json

from .errors import ErrMessages


def is_spider(filename: str) -> tuple:
    folder_path, _, spider = filename.rpartition("/")
    if folder_path.endswith("spiders"):
        const = f"{folder_path}/constants/{spider}"
        return filename, const
    elif folder_path.endswith("constants"):
        spiders_folder = folder_path.rpartition("/")[0]
        return f"{spiders_folder}/{spider}", filename


def check_terms_n_urls(parsed_tree: ast.Module, constant_path: str, errors_list: list):
    files_to_fix = []
    for fields in parsed_tree.body:
        dump_node = ast.dump(fields)
        if "START_URLS" in dump_node:
            start_urls = ast.walk(fields).__next__().value.elts
            if start_urls:
                files_to_fix.append({"err_type": "start_urls", "where": constant_path})
        if "SEARCH_TERMS" in dump_node:
            search_terms = ast.walk(fields).__next__().value.elts
            if search_terms:
                files_to_fix.append({"err_type": "search_terms", "where": constant_path})
    if files_to_fix:
        for error_file in files_to_fix:
            errors_list += (
                ErrMessages.comment_urls_or_terms.format(error_type=error_file['err_type'],
                                                         error_location=error_file['where'])
            )


def find_spider_info(parsed_tree: ast.Module, constant_path: str, errors_list: list):
    for fields in parsed_tree.body:
        dump_node = ast.dump(fields)
        if "SPIDERS_INFO" in dump_node:
            json_dict = {}
            try:
                spiders_info = ast.walk(fields).__next__().value.value
            except AttributeError:
                spiders_info_dicts = ast.walk(fields).__next__().value.values
                spiders_info_keys = ast.walk(fields).__next__().value.keys
                for dict_name, dict_value in zip(spiders_info_keys, spiders_info_dicts):
                    sinfo_keys = dict_value.keys
                    sinfo_vals = dict_value.values
                    subdict = zip(sinfo_keys, sinfo_vals)
                    json_dict[dict_name.value] = {
                        key.value: value.value for key, value in subdict
                    }
                return json_dict
            else:

                return json.loads(spiders_info.partition("=")[-1])

    errors_list += (
        ErrMessages.spiders_info.format(constant_path=constant_path)
    )
