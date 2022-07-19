from itertools import chain

from core.objects import InlineKeyboard, CallbackButton, UrlButton, Keyboard, KeyboardButton
from . import config
from . import texts

BACK_BUTTON = texts.back


class MainMenu(InlineKeyboard):
    create_ad = CallbackButton(texts.create_ad)
    my_ads = CallbackButton(texts.my_ads)
    tech_support = UrlButton(texts.tech_support, 'https://t.me/LFeedbackBot')
    our_site = UrlButton(texts.our_site, 'https://horeca-job.com.ua/')
    change_lang = CallbackButton(texts.change_lang)

    def __init__(self, lang: str | None):
        self.add_row(self.create_ad, self.my_ads)
        self.add_row(self.tech_support, self.our_site)

        flag = {'ua': '🇷🇺', 'ru': '🇺🇦'}.get(lang, '🇺🇦')
        self.add_row(self.change_lang(flag=flag))


class Regions(Keyboard):
    buttons = list(config.CITY_BY_REGION.keys())

    def __init__(self):
        self.add_rows(*self.buttons, row_width=2)


class Cities(Keyboard):
    buttons = list(chain(*config.CITY_BY_REGION.values()))

    def __init__(self, region: str):
        for key, value in config.CITY_BY_REGION.items():
            if region in key:
                self.add_rows(*value, row_width=2)
                return
        raise ValueError("Invalid region")


class VacanciesAmount(Keyboard):
    one = texts.one_vacancy_price
    two = texts.two_vacancies_price
    three = texts.three_vacancies_price

    buttons = [one, two, three]

    def __init__(self):
        self.add_rows(*self.buttons)


class Skip(Keyboard):
    button = texts.skip

    def __init__(self):
        self.add_row(self.button)


class SendContact(Keyboard):
    button = KeyboardButton(texts.send_self_phone, request_contact=True)

    def __init__(self):
        self.add_row(self.button)


class PinOption(Keyboard):
    no = texts.not_pin
    yes = texts.pin_for

    def __init__(self):
        self.add_rows(self.no, self.yes)


class DuplicateOption(Keyboard):
    no = texts.not_duplicate
    yes = texts.duplicate_for

    def __init__(self, vacancies_num: int):
        self.add_rows(
            self.no,
            self.yes.format(price=config.DUPLICATE_PRICE_BY_VACANCIES_AMOUNT[vacancies_num]),
        )


class EditAd(Keyboard):
    institution = texts.change_institution_info
    vacancy = texts.change_vacancy_num
    other_info = texts.change_other_info
    finish = texts.all_correct

    def __init__(self, vacancies_amount: int):
        self.add_rows(self.institution)
        self.add_rows(*[self.vacancy.format(num=i) for i in range(1, vacancies_amount + 1)])
        self.add_rows(self.other_info, self.finish)


class EditInstitution(Keyboard):
    city = texts.city
    type = texts.institution_type
    name = texts.institution_name
    address = texts.institution_address

    def __init__(self):
        self.add_rows(self.city, self.type, self.name, self.address, BACK_BUTTON)


class EditVacancy(Keyboard):
    title = texts.vacancy_title
    work_experience = texts.work_experience
    salary = texts.salary
    schedule = texts.schedule
    working_hours = texts.working_hours

    def __init__(self):
        self.add_rows(self.title, self.work_experience, self.salary, self.schedule, self.working_hours, BACK_BUTTON)


class EditOtherInfo(Keyboard):
    extra_info = texts.extra_info
    contact_phone = texts.contact_phone
    photo = texts.institution_photo
    post_date = texts.post_date
    pin_option = texts.pin_option
    duplicate_option = texts.duplicate_option

    def __init__(self):
        self.add_rows(self.extra_info, self.contact_phone, self.photo, self.post_date, self.pin_option,
                      self.duplicate_option, BACK_BUTTON)


class Payment(InlineKeyboard):
    url = UrlButton(texts.pay_up, url='{payment_url}')

    def __init__(self, payment_url: str):
        self.add_row(self.url(payment_url=payment_url))
