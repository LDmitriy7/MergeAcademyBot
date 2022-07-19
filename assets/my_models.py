from dataclasses import dataclass, field

from assets.texts import duplicate_option
from core import UserProxyModel


@dataclass
class Institution(UserProxyModel):
    region: str = None
    city: str = None
    type: str = None
    name: str = None
    address: str = None


@dataclass
class Vacancy(UserProxyModel):
    num: int = None
    title: str = None
    work_experience: str = None
    salary: str = None
    schedule: str = None
    working_hours: str = None


@dataclass
class Ad(UserProxyModel):
    institution: Institution = None
    vacancies: list[Vacancy] = field(default_factory=list)
    extra_info: str = None
    contact_phone: str = None
    photo_url: str = None
    pin_option: bool = None
    post_date: int = None
    duplicate_option: bool = None


@dataclass
class Order(UserProxyModel):
    id: str = None
    ad: Ad = None
    price: int = None


@dataclass
class Invoice:
    vacancies_price: int
    pin_price: int = 0
    duplicate_price: int = 0

    @property
    def total_price(self) -> int:
        return self.vacancies_price + self.pin_price + self.duplicate_price
