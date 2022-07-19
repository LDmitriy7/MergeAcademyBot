import re
import time

from assets import *
from core import *
from utils import PhotoEditor, uncapitalize, parse_phone, parse_post_date, repr_ad
from .entry_point import EDIT_MODE

conv = states.CreateAd


def show_ad_or(func):
    if ctx.data[EDIT_MODE]:
        send_ad_preview()
    else:
        func()


# ===

def process_region():
    with my_models.Institution.proxy() as institution:
        institution.region = ctx.text


def ask_city():
    institution = my_models.Institution.get()
    ctx.state = conv.city
    bot.send_message(texts.ask_city, reply_markup=kb.Cities(institution.region))


@on.button(kb.Regions.buttons, state=conv.region)
def _():
    process_region()
    ask_city()


# ===

def process_city():
    with my_models.Institution.proxy() as institution:
        institution.city = ctx.text


def ask_institution_type():
    ctx.state = conv.institution_type
    bot.send_message(texts.ask_institution_type, reply_markup=objects.ReplyKeyboardRemove())


@on.button(kb.Cities.buttons, state=conv.city)
def _():
    process_city()
    show_ad_or(ask_institution_type)


# ===

def process_institution_type():
    with my_models.Institution.proxy() as institution:
        institution.type = uncapitalize(ctx.text)


def ask_institution_name():
    ctx.state = conv.institution_name
    bot.send_message(texts.ask_institution_name, reply_markup=objects.ReplyKeyboardRemove())


@on.text(state=conv.institution_type)
def _():
    process_institution_type()
    show_ad_or(ask_institution_name)


# ===

def process_institution_name():
    with my_models.Institution.proxy() as institution:
        institution.name = ctx.text


def ask_institution_address():
    ctx.state = conv.institution_address
    bot.send_message(texts.ask_institution_address, reply_markup=objects.ReplyKeyboardRemove())


@on.text(state=conv.institution_name)
def _():
    process_institution_name()
    show_ad_or(ask_institution_address)


# ===

def process_institution_address():
    with my_models.Institution.proxy() as institution:
        institution.address = uncapitalize(ctx.text)


def ask_vacancies_amount():
    ctx.state = conv.vacancies_amount
    bot.send_message(texts.ask_vacancies_amount, reply_markup=kb.VacanciesAmount())


@on.text(state=conv.institution_address)
def _():
    process_institution_address()
    show_ad_or(ask_vacancies_amount)


# ===

def process_vacancies_amount():
    my_models.Vacancy(num=1).save()
    ctx.data[C.vacancies_amount] = int(ctx.text.split(' ')[0])


def ask_vacancy_title():
    vacancy = my_models.Vacancy.get()
    ctx.state = conv.vacancy_title
    bot.send_message(texts.vacancy_num.format(vacancy.num))
    bot.send_message(texts.ask_vacancy_title, reply_markup=objects.ReplyKeyboardRemove())


@on.button(kb.VacanciesAmount.buttons, state=conv.vacancies_amount)
def _():
    process_vacancies_amount()
    ask_vacancy_title()


# ===

def process_vacancy_title():
    with my_models.Vacancy.proxy() as vacancy:
        vacancy.title = ctx.text


def ask_work_experience():
    ctx.state = conv.work_experience
    bot.send_message(texts.ask_work_experience, reply_markup=objects.ReplyKeyboardRemove())


@on.text(state=conv.vacancy_title)
def _():
    process_vacancy_title()
    show_ad_or(ask_work_experience)


# ===

def process_work_experience():
    with my_models.Vacancy.proxy() as vacancy:
        vacancy.work_experience = uncapitalize(ctx.text)


def ask_salary():
    ctx.state = conv.salary
    bot.send_message(texts.ask_salary, reply_markup=objects.ReplyKeyboardRemove())


@on.text(state=conv.work_experience)
def _():
    process_work_experience()
    show_ad_or(ask_salary)


# ===


def process_salary():
    if not re.search(r'\d', ctx.text):
        bot.send_message(texts.must_contain_digits)
        raise exc.ExitHandler()

    with my_models.Vacancy.proxy() as vacancy:
        vacancy.salary = uncapitalize(ctx.text)


def ask_schedule():
    ctx.state = conv.schedule
    bot.send_message(texts.ask_schedule, reply_markup=objects.ReplyKeyboardRemove())


@on.text(state=conv.salary)
def _():
    process_salary()
    show_ad_or(ask_schedule)


# ===

def process_schedule():
    if not re.search(r'\d', ctx.text):
        bot.send_message(texts.must_contain_digits)
        raise exc.ExitHandler()

    with my_models.Vacancy.proxy() as vacancy:
        vacancy.schedule = ctx.text


def ask_working_hours():
    ctx.state = conv.working_hours
    bot.send_message(texts.ask_working_hours, reply_markup=objects.ReplyKeyboardRemove())


@on.text(state=conv.schedule)
def _():
    process_schedule()
    show_ad_or(ask_working_hours)


# ===


def process_working_hours():
    if not re.search(r'\d', ctx.text):
        bot.send_message(texts.must_contain_digits)
        raise exc.ExitHandler()

    with my_models.Vacancy.proxy() as vacancy:
        vacancy.working_hours = uncapitalize(ctx.text)


def ask_extra_info():
    ctx.state = conv.extra_info
    bot.send_message(texts.vacancies_filled)
    bot.send_message(texts.ask_extra_info, reply_markup=kb.Skip())


def ask_next_vacancy_or_extra_info():
    vacancy = my_models.Vacancy.get()

    with my_models.Ad.proxy() as ad:
        ad.vacancies.append(vacancy)

    if vacancy.num < ctx.data[C.vacancies_amount]:
        my_models.Vacancy(num=vacancy.num + 1).save()
        ask_vacancy_title()
    else:
        ask_extra_info()


@on.text(state=conv.working_hours)
def _():
    process_working_hours()
    show_ad_or(ask_next_vacancy_or_extra_info)


# ===


def process_extra_info_skip():
    with my_models.Ad.proxy() as ad:
        ad.extra_info = None


def process_extra_info():
    max_text_len = 150

    if len(ctx.text) > max_text_len:
        bot.send_message(texts.too_long_text.format(max_text_len))
        raise exc.ExitHandler()

    with my_models.Ad.proxy() as ad:
        ad.extra_info = ctx.text


def ask_contact_phone():
    ctx.state = conv.contact_phone
    bot.send_message(texts.ask_contact_phone, reply_markup=kb.SendContact())


@on.button(kb.Skip.button, state=conv.extra_info)
def _():
    process_extra_info_skip()
    show_ad_or(ask_contact_phone)


@on.text(state=conv.extra_info)
def _():
    process_extra_info()
    show_ad_or(ask_contact_phone)


# ===

def process_phone_contact():
    try:
        contact_phone = parse_phone(ctx.message.contact.phone_number)
    except ValueError:
        bot.send_message(texts.invalid_contact_phone)
        raise exc.ExitHandler()

    with my_models.Ad.proxy() as ad:
        ad.contact_phone = contact_phone


def process_phone_text():
    try:
        contact_phone = parse_phone(ctx.text)
    except ValueError:
        bot.send_message(texts.invalid_contact_phone)
        raise exc.ExitHandler()

    with my_models.Ad.proxy() as ad:
        ad.contact_phone = contact_phone


def ask_photo():
    ctx.state = conv.photo
    bot.send_message(texts.ask_photo, reply_markup=objects.ReplyKeyboardRemove())


@on.contact(state=conv.contact_phone)
def _():
    process_phone_contact()
    show_ad_or(ask_photo)


@on.text(state=conv.contact_phone)
def _():
    process_phone_text()
    show_ad_or(ask_photo)


# ===

def process_photo_document():
    bot.send_message(texts.ask_photo_not_document)


def process_photo():
    bot.send_chat_action('typing')

    photo_url = bot.get_file_url()
    photo_url = PhotoEditor.open(photo_url).crop(min_ratio=config.AD_PHOTO_MIN_RATIO).upload()

    with my_models.Ad.proxy() as ad:
        ad.photo_url = photo_url


def ask_pin_option():
    ctx.state = conv.pin_option
    bot.send_message(texts.ask_pin_option, reply_markup=kb.PinOption())

    # TODO
    # text = texts.whether_pin_ad
    # pin_until = await api.check_pinning_availability()
    #
    # if pin_until > time.time():  # add note about delaying
    #     text += '\n' + texts.pinning_will_be_delayed_until.format(
    #         date=utils.misc.repr_timestamp_as_date(pin_until)
    #     )


@on.document(state=conv.photo)
def _():
    process_photo_document()


@on.photo(state=conv.photo)
def _():
    process_photo()
    show_ad_or(ask_pin_option)


# ===

def process_pin_option_yes():
    with my_models.Ad.proxy() as ad:
        ad.pin_option = True


def process_pin_option_no():
    with my_models.Ad.proxy() as ad:
        ad.pin_option = False


def ask_post_date():
    ctx.state = conv.post_date
    bot.send_message(texts.ask_post_date, reply_markup=kb.Skip())


@on.button(kb.PinOption.yes, state=conv.pin_option)
def _():
    process_pin_option_yes()
    show_ad_or(ask_post_date)


@on.button(kb.PinOption.no, state=conv.pin_option)
def _():
    process_pin_option_no()
    show_ad_or(ask_post_date)


# ===

def process_post_date_skip():
    with my_models.Ad.proxy() as ad:
        ad.post_date = None


def process_post_date():
    try:
        post_date = parse_post_date(ctx.text)
    except ValueError:
        bot.send_message(texts.invalid_post_date)
        raise exc.ExitHandler()

    if post_date < time.time():
        bot.send_message(texts.ask_later_post_date)
        raise exc.ExitHandler()

    with my_models.Ad.proxy() as ad:
        ad.post_date = post_date


def ask_duplicate_option():
    ctx.state = conv.duplicate_option
    vacancies_amount = ctx.data[C.vacancies_amount]
    bot.send_message(texts.ask_duplicate_option, reply_markup=kb.DuplicateOption(vacancies_amount))


@on.button(kb.Skip.button, state=conv.post_date)
def _():
    process_post_date_skip()
    show_ad_or(ask_duplicate_option)


@on.text(state=conv.post_date)
def _():
    process_post_date()
    show_ad_or(ask_duplicate_option)


# ===


def process_duplicate_option_yes():
    with my_models.Ad.proxy() as ad:
        ad.duplicate_option = True


def process_duplicate_option_no():
    with my_models.Ad.proxy() as ad:
        ad.duplicate_option = False


@on.button(kb.DuplicateOption.yes, state=conv.duplicate_option)
def _():
    process_duplicate_option_yes()
    send_ad_preview()


@on.button(kb.DuplicateOption.no, state=conv.duplicate_option)
def _():
    process_duplicate_option_no()
    send_ad_preview()


# ===

def send_ad_preview():
    ctx.data[EDIT_MODE] = True
    ctx.state = conv.ad_preview

    vacancies_amount = ctx.data[C.vacancies_amount]
    vacancy = my_models.Vacancy.get()

    with my_models.Ad.proxy() as ad:
        ad.institution = my_models.Institution.get()
        ad.vacancies[vacancy.num - 1] = vacancy

    bot.send_message(repr_ad(ad))
    bot.send_message(texts.ask_whether_to_edit_ad, reply_markup=kb.EditAd(vacancies_amount))

# ===
