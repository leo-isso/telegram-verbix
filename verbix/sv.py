import bs4
import requests


URL = 'http://www.verbix.com/webverbix/Swedish/{verbet}.html'

RED_FLAG_TEXT = 'The verb does not exist or it is unknown for Verbix.'

SELECT_VERBTABLE = '.verbtable'

SELECT_FORMS = '.pure-u-1-1'

SELECT_TENSES = '.pure-u-1-2'


def get_url(verbet):
    verbet = verbet.lower()

    return URL.format(verbet=verbet)


def build_info(infinitive, supine, gerund, imperative, present, past, url):
    return {
        'forms': {
            'infinitive': (infinitive.text, infinitive.get('class')[0]),
            'supine': (supine.text, supine.get('class')[0]),
            'gerund': (gerund.text, gerund.get('class')[0]),
            'imperative': (imperative.text, imperative.get('class')[0])
        },
        'tenses': {
            'present': (present.text, present.get('class')[0]),
            'past': (past.text, past.get('class')[0])
        },
        'url': url
    }


def get_verb_info(verbet):
    url = get_url(verbet)

    response = requests.get(url)

    if response.status_code != 200:
        return

    if response.text.find(RED_FLAG_TEXT) != -1:
        return

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    verbtable = soup.select_one(SELECT_VERBTABLE)

    forms = verbtable.select(SELECT_FORMS)

    infinitive, supine, gerund = forms[0].select('span')

    imperative = forms[-1].select('span')[1]

    #

    tenses = verbtable.select(SELECT_TENSES)

    present, past = tenses[0], tenses[2]
    present = present.select('span')[1]
    past = past.select('span')[1]

    return build_info(infinitive, supine, gerund, imperative, present, past, url)
