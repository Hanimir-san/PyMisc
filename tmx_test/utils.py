import spacy

def load_spacy_nlp(lang, model_size='lg'):
    web_langs = ('en', 'zh')
    if lang in web_langs:
        model_name = f'{lang}_code_web_{model_size}'
    else:
        model_name = f'{lang}_code_news_{model_size}'
    nlp = spacy.load(model_name)
    return nlp