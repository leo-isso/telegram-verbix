import os
import configparser

import telepot

import misc
import verbix
import templates


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'project.ini'))

bot = telepot.Bot(config.get('bot', 'token'))


def _get_verb_info(verb):
    try:
        verb_info = verbix.sv.get_verb_info(verb)
    except:
        return 'Verbet `%s` hittades inte.' % verb

    if verb_info is None:
        return 'Verbet `%s` hittades inte.' % verb

    def format(tuple):
        v, f = tuple
        if f == 'orto':
            return '_%s_' % v
        elif f == 'irregular':
            return '*%s*' % v
        else:
            return v

    infinitive = format(verb_info['forms']['infinitive'])
    supine = format(verb_info['forms']['supine'])
    gerund = format(verb_info['forms']['gerund'])
    imperative = format(verb_info['forms']['imperative'])
    present = format(verb_info['tenses']['present'])
    past = format(verb_info['tenses']['past'])

    url = verb_info['url']

    return templates.swedish.template \
        % (infinitive, supine, gerund, imperative, present, past) % url


@misc.threaded
def handle_message(msg):
    verb = msg['text']
    chat_id = msg['chat']['id']

    bot.sendChatAction(chat_id, 'typing')

    info = _get_verb_info(verb)

    bot.sendMessage(chat_id, info, parse_mode='markdown',
                    disable_web_page_preview=True)


def handle_inline(query):
    id = query['id']
    verb = query['query']

    if verb == '':
        return

    unique_id = os.urandom(10).hex()

    bot.answerInlineQuery(id, cache_time=0, results=[{
        'type': 'article',
        'id': unique_id,
        'title': verb,
        'description': 'verbet "%s"' % verb,
        'input_message_content': {
            'message_text': 'Verbet: %s\n_Läser in..._' % verb,
            'parse_mode': 'markdown'
        }
    }])


def handle_chosen_inline(result):
    print(result)
    info = _get_verb_info(result['query'])

    print(info)

    bot.editMessageText(result['result_id'], text=info, parse_mode='markdown')


if __name__ == '__main__':
    bot.message_loop(
        handle_message, relax=0.5, timeout=5, run_forever='Listening...')
