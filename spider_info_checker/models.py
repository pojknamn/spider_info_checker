from typing import Any

from pydantic import BaseModel

from .errors import NotValidSpiderInfo


class PossiblyStrictModel(BaseModel):
    def __init_subclass__(cls):
        if getattr(cls.__config__, "strict", False):

            def __init__(__pydantic_self__, **data: Any) -> None:
                errors = []
                for k, v in data.items():
                    field = __pydantic_self__.__fields__[k]
                    if not isinstance(v, field.type_):
                        errors.append(
                            f"Некорректный аргумент {v!r} в поле {field.name}"
                            f" получили {type(v).__name__} "
                            f"вместо {field.type_.__name__}"
                        )
                if errors:
                    raise NotValidSpiderInfo(errors)
                super().__init__(**data)

            cls.__init__ = __init__


class SpidersInfoTrue(PossiblyStrictModel):
    PROXY_TYPE: str
    LOCAL_SPIDER: bool
    EAN_COLLECT: bool
    GEO_SPIDER: str
    RPC_SPIDER: str
    STOCK_SPIDER: str
    REGIONS_SPIDER: str
    SITE_SECURITY: str
    RATE_SECURITY: int
    VARIANTS_SPIDER: bool
    MARKETPLACE_SPIDER: bool
    PROMO_INFO: bool
    SET_INFO: bool
    COUNT_INFO: bool
    GEO_COUNT_INFO: bool
    REVIEWS_INFO: bool
    RATING_INFO: bool
    COMMENTS: str

    class Config:
        strict = True


class SpidersInfoCat(PossiblyStrictModel):
    PROXY_TYPE: str
    VARIANTS: bool
    QTY_GOODS: int
    CUSTOM_QTY: bool
    COMMENTS: str

    class Config:
        strict = True


class SpidersInfoSearch(PossiblyStrictModel):
    PROXY_TYPE: str
    VARIANTS: bool
    DEEP_LIMITER: bool
    QTY_GOODS: int
    CUSTOM_QTY: bool
    COMMENTS: str

    class Config:
        strict = True


class SpidersInfoReviews(PossiblyStrictModel):
    PROXY_TYPE: str
    EXPECT_REVIEW: str
    RATING: bool
    LIKE_DISLIKE: bool
    COLLECTING_COMMENTS: bool
    COM_REV: bool
    SPLIT_REV: bool
    COMMENTS: str

    class Config:
        strict = True
