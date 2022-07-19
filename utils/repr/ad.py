import re

from assets import my_models, texts
from ..misc import safe_html


def _repr_institution(obj: my_models.Institution, lang: str) -> str:
    if obj.city != obj.region:
        address = f'{obj.city}, {obj.address}'
    else:
        address = obj.address

    return texts.ad_institution_template.get(lang).format(
        type=obj.type,
        name=obj.name,
        address=address,
    ).strip()


def _repr_vacancy(vacancy: my_models.Vacancy, lang: str) -> str:
    # make digits bold
    salary = re.sub(r'(\d+)', r'<b>\1</b>', vacancy.salary)
    schedule = re.sub(r'(\d+)', r'<b>\1</b>', vacancy.schedule)
    working_hours = re.sub(r'(\d+)', r'<b>\1</b>', vacancy.working_hours)

    return texts.ad_vacancy_template.get(lang).format(
        title=vacancy.title,
        work_experience=vacancy.work_experience,
        salary=salary,
        schedule=schedule,
        working_hours=working_hours,
    ).strip()


def _repr_other_info(ad: my_models.Ad, lang: str) -> str:
    return texts.ad_other_info_template.get(lang).format(
        extra_info=ad.extra_info or '',
        photo_url=ad.photo_url,
        contact_phone=ad.contact_phone,
    ).strip()


def _repr_ad(ad: my_models.Ad, lang: str):
    ad = texts.ad_template.format(
        institution=_repr_institution(ad.institution, lang),
        vacancies='\n\n'.join([_repr_vacancy(v, lang) for v in ad.vacancies]),
        other_info=_repr_other_info(ad, lang),
    )
    return safe_html(ad)


def repr_ad(ad: my_models.Ad) -> texts.T:
    return texts.T(_repr_ad(ad, 'ru'), _repr_ad(ad, 'ua'))
