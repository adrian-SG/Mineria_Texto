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


class BasicIndex:

    index = {}

    def __init__(self, path_list):
        """
        initializes the new BasicIndex instance by indexing file content of files from path_list
        :param path_list: list of file paths to be indexed
        """
        for file_path in path_list:
            with open(file_path) as file:
                # Obtener nombre del archivo desde el path
                self.process_file(file, file_path)

    def process_file(self, file, file_path):
        """
        indexes the content of a file
        :param file:
        :param file_path:
        :return:
        """

        file_indexed_values = self.index.get(file_path, set())

        for line in file:
            for token in clean_tonkenize(line):
                file_indexed_values.add(token)

        self.index[file_path] = file_indexed_values

class BasicQuery:

    def __init__(self, basic_index):
        """
        initializes the new BasicQuery instance by setting the BasicIndex to query
        :param basic_index: index to query
        """
        self.basic_index = basic_index

    def query(self, query):
        result_doc_list = []
        query_token_list = [t for t in clean_tonkenize(query)]

        for key, value_list in self.basic_index.index.items():
            for token in query_token_list:
                if token in value_list:
                    result_doc_list.append(key)
                    break
        return result_doc_list



''' Prueba de concepto'''

import datetime
t_start = datetime.datetime.now()

t_basic_index = BasicIndex(['.\corpus\pg135.txt',
                            '.\corpus\pg76.txt',
                            '.\corpus\pg5200.txt'])
t_query = BasicQuery(t_basic_index)
print(t_query.query("The house was in England"))
t_finish = datetime.datetime.now()
print("Query total time: %s" % str(t_finish-t_start))


