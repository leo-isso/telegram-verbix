from urllib.parse import quote as urlquote

import bs4
import requests


# Exceptions
VerbixError = type('VerbixError', (Exception,), {})
VerbNotFoundError = type('VerbNotFoundError', (Exception,), {})


class Verbix:
    # Url to query for verb conjugations;
    # must be populated with language and verb
    URL = 'http://www.verbix.com/webverbix/{language}/{verb}.html'

    # Text indicating that the queried verb does not exist in Verbix
    # database
    RED_FLAG_TEXT = 'The verb does not exist or it is unknown for Verbix.'

    # Base css class
    SELECT_VERBTABLE = '.verbtable'

    # Forms div class
    SELECT_FORMS = '.pure-u-1-1'

    # Tenses div class
    SELECT_TENSES = '.pure-u-1-2'

    def __init__(self):
        self.language = self.__class__.__name__

    def get_url(self, verb):
        return self.URL.format(language=self.language,
                               verb=verb.lower())

    def query_verb(self, verb):
        """
        Query verbix for the given verb. Returns a BeautifulSoup
        instance.
        """
        url = self.get_url(verb)

        response = requests.get(url)

        if response.status_code != 200:
            raise VerbixError(response.text)

        if response.text.find(self.RED_FLAG_TEXT) != -1:
            raise VerbNotFoundError(verb)

        return bs4.BeautifulSoup(response.content.decode(), 'html.parser')

    def conjugate(self, verb):
        # implement this in subclasses
        raise NotImplementedError

    def _build_info(self):
        # implement this in subclasses; make it return a dictionary
        # containing information about the verb's conjugations,
        # inflections, etc
        raise NotImplementedError

    def _verb_safe_url(self, verb):
        return urlquote(self.get_url(verb), safe=':/')
