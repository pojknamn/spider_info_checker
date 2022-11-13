import pprint

import libcst as cst

SUPER_COMMA = cst.Comma(whitespace_after=cst.ParenthesizedWhitespace(indent=True))

EPMTY_SPIDERS_INFO_STATEMENT = """_SPIDERS_INFO = {
}"""

class SpiderInfoTemplates:
    def __init__(self):
        self.base = {
            "PROXY_TYPE": "",
            "LOCAL_SPIDER": False,
            "EAN_COLLECT": False,
            "GEO_SPIDER": "",
            "RPC_SPIDER": "",
            "STOCK_SPIDER": "",
            "REGIONS_SPIDER": "",
            "SITE_SECURITY": "",
            "RATE_SECURITY": 0,
            "VARIANTS_SPIDER": True,
            "MARKETPLACE_SPIDER": True,
            "PROMO_INFO": False,
            "SET_INFO": False,
            "COUNT_INFO": True,
            "GEO_COUNT_INFO": False,
            "REVIEWS_INFO": True,
            "RATING_INFO": True,
            "COMMENTS": ""
        }
        self.search = {
            "PROXY_TYPE": "",
            "VARIANTS": True,
            "DEEP_LIMITER": True,
            "QTY_GOODS": 0,
            "CUSTOM_QTY": False,
            "COMMENTS": ""
        }
        self.category = {
            "PROXY_TYPE": "",
            "VARIANTS": True,
            "QTY_GOODS": 0,
            "CUSTOM_QTY": False,
            "COMMENTS": ""
        }
        self.reviews = {
            "PROXY_TYPE": "",
            "EXPECT_REVIEW": "",
            "RATING": True,
            "LIKE_DISLIKE": True,
            "COLLECTING_COMMENTS": False,
            "COM_REV": False,
            "SPLIT_REV": False,
            "COMMENTS": ""
        }
        self._make_cst_template_dicts()
        self.EMPTY_SPIDERS_INFO = cst.parse_statement(EPMTY_SPIDERS_INFO_STATEMENT)

    def _make_cst_template_dicts(self):
        class_attributes = list(self.__dict__.keys())
        for template_namr in class_attributes:
            cst_dict = cst.parse_statement(
                "\n" + pprint.pformat(self.__getattribute__(template_namr),
                                      indent=4,
                                      sort_dicts=False)
            ).body[0].value
            self.__setattr__(f"{template_namr}_cst", cst_dict)




def get_dict_from_spider_name(spider_name):
    templates = SpiderInfoTemplates()
    if "_search" in spider_name:
        sinfo_dict = templates.search_cst
    elif "_category" in spider_name:
        sinfo_dict = templates.cat_cst
    elif "_reviews" in spider_name:
        sinfo_dict = templates.reviews_cst
    else:
        sinfo_dict = templates.base_cst
    return sinfo_dict
