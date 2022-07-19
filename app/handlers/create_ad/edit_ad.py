from assets import *
from core import *
from . import fill_ad

conv = states.CreateAd


@on.button(kb.EditAd.institution, state=conv.ad_preview)
def _():
    bot.send_message('...', reply_markup=kb.EditInstitution())


@on.button(kb.EditAd.vacancy, state=conv.ad_preview)
def _():
    vacancy_num = int(ctx.text.split(' ')[-1])
    vacancies_amount = ctx.data[C.vacancies_amount]

    if vacancy_num > vacancies_amount:
        bot.send_message(texts.no_such_vacancy)
        raise exc.ExitHandler()

    with my_models.Ad.proxy() as ad:
        ad.vacancies[vacancy_num - 1].save()

    bot.send_message('...', reply_markup=kb.EditVacancy())


@on.button(kb.EditAd.other_info, state=conv.ad_preview)
def _():
    bot.send_message('...', reply_markup=kb.EditOtherInfo())


@on.button(kb.BACK_BUTTON, state=conv.ad_preview)
def _():
    vacancies_amount = ctx.data[C.vacancies_amount]
    bot.send_message('...', reply_markup=kb.EditAd(vacancies_amount))


# ===

@on.button(kb.EditInstitution.city, state=conv.ad_preview)
def _():
    fill_ad.ask_city()


@on.button(kb.EditInstitution.type, state=conv.ad_preview)
def _():
    fill_ad.ask_institution_type()


@on.button(kb.EditInstitution.name, state=conv.ad_preview)
def _():
    fill_ad.ask_institution_name()


@on.button(kb.EditInstitution.address, state=conv.ad_preview)
def _():
    fill_ad.ask_institution_address()


@on.button(kb.EditVacancy.title, state=conv.ad_preview)
def _():
    fill_ad.ask_vacancy_title()


@on.button(kb.EditVacancy.work_experience, state=conv.ad_preview)
def _():
    fill_ad.ask_work_experience()


@on.button(kb.EditVacancy.salary, state=conv.ad_preview)
def _():
    fill_ad.ask_salary()


@on.button(kb.EditVacancy.schedule, state=conv.ad_preview)
def _():
    fill_ad.ask_schedule()


@on.button(kb.EditVacancy.working_hours, state=conv.ad_preview)
def _():
    fill_ad.ask_working_hours()


@on.button(kb.EditOtherInfo.extra_info, state=conv.ad_preview)
def _():
    fill_ad.ask_extra_info()


@on.button(kb.EditOtherInfo.contact_phone, state=conv.ad_preview)
def _():
    fill_ad.ask_contact_phone()


@on.button(kb.EditOtherInfo.photo, state=conv.ad_preview)
def _():
    fill_ad.ask_photo()


@on.button(kb.EditOtherInfo.post_date, state=conv.ad_preview)
def _():
    fill_ad.ask_post_date()


@on.button(kb.EditOtherInfo.pin_option, state=conv.ad_preview)
def _():
    fill_ad.ask_pin_option()


@on.button(kb.EditOtherInfo.duplicate_option, state=conv.ad_preview)
def _():
    fill_ad.ask_duplicate_option()
