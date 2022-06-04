from .errors import ErrMessages, NotValidSpiderInfo
from .misc import update_errors_list
from .models import (SpidersInfoCat, SpidersInfoReviews, SpidersInfoSearch,
                     SpidersInfoTrue)


def validate_spiders_info(spiders_info: dict, errors_to_fix: list, none_of_there: set):
    for info in spiders_info.items():
        spider_name, spider_info_dict = info
        try:
            if "search" in spider_name:
                SpidersInfoSearch(**spider_info_dict)
            elif "category" in spider_name:

                SpidersInfoCat(**spider_info_dict)
            elif "reviews" in spider_name:
                SpidersInfoReviews(**spider_info_dict)
            else:
                SpidersInfoTrue(**spider_info_dict)
        except NotValidSpiderInfo as err_message:
            if spider_name in none_of_there:
                spider_name += ErrMessages.remove_or_rename
            update_errors_list(err_message, errors_to_fix, spider_name)
