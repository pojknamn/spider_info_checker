class SpiderInfo:
    base = {
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
    search = {
        "PROXY_TYPE": "",
        "VARIANTS": True,
        "DEEP_LIMITER": True,
        "QTY_GOODS": 0,
        "CUSTOM_QTY": False,
        "COMMENTS": ""
    }
    category = {
        "PROXY_TYPE": "",
        "VARIANTS": True,
        "QTY_GOODS": 0,
        "CUSTOM_QTY": False,
        "COMMENTS": ""
    }
    reviews = {
        "PROXY_TYPE": "",
        "EXPECT_REVIEW": "",
        "RATING": True,
        "LIKE_DISLIKE": True,
        "COLLECTING_COMMENTS": False,
        "COM_REV": False,
        "SPLIT_REV": False,
        "COMMENTS": ""
    }


def spider_info_from_template(names: set) -> dict:
    spider_info_missed = {}
    for name in names:
        if "_search" in name:
            spider_info_missed.update({name: SpiderInfo.search})
        elif "_category" in name:
            spider_info_missed.update({name: SpiderInfo.category})
        elif '_reviews' in name:
            spider_info_missed.update({name: SpiderInfo.reviews})
        else:
            spider_info_missed.update({name: SpiderInfo.base})
    return spider_info_missed
