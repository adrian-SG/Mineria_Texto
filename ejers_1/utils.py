import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


def clean_tonkenize(targ_string):

    pnct_translt_table = str.maketrans('', '', string.punctuation)
    eng_stop_words = set(stopwords.words('english'))
    lmtzr = WordNetLemmatizer()

    # tokenize
    for w in word_tokenize(targ_string):

        # lemmatize, remove punctuation and stopwords
        if w.translate(pnct_translt_table) == '' or w in eng_stop_words:
            pass
        else:
            yield lmtzr.lemmatize(
                w.translate(pnct_translt_table)
            )

