from ejers_1.utils import clean_tonkenize


class InvertexIndex:

    index = {}

    def __init__(self, path_list):
        """
        initializes the new InvertexIndex instance by indexing file content of files from path_list
        :param path_list: list of file paths to be indexed
        """
        for file_path in path_list:
            with open(file_path) as file:
                self.process_file(file, file_path)

    def process_file(self, file, file_path):
        """
        indexes the content of a file
        :param file:
        :param file_path:
        :return:
        """

        # for line in file:
        #     for token in clean_tonkenize(line):
        for token in clean_tonkenize(file.read()):
            token_indexed_values = self.index.get(token, set())
            token_indexed_values.add(file_path)
            self.index[token] = token_indexed_values


class InvertedQuery:
    def __init__(self, invertex_index):
        """
        initializes the new InvertedQuery instance by setting the InvertexIndex to query
        :param invertex_index: index to query
        """
        self.invertex_index = invertex_index

    def query(self, query):
        result_doc_set = set()
        query_token_list = [t for t in clean_tonkenize(query)]

        for token in query_token_list:
            [result_doc_set.add(doc) for doc in self.invertex_index.index[token]]

        return result_doc_set



''' Prueba de concepto'''
print("Invertex: prueba de concepto")
import datetime
t_start = datetime.datetime.now()

t_invertex_index = InvertexIndex(['.\corpus\pg135.txt',
                            '.\corpus\pg76.txt',
                            '.\corpus\pg5200.txt'])
t_query = InvertedQuery(t_invertex_index)

t_index = datetime.datetime.now()
print("index build time: %s" % str(t_index-t_start))
print(t_query.query("The house was in England"))
t_finish = datetime.datetime.now()
print("query time: %s" % str(t_finish-t_index))
print("Total time: %s" % str(t_finish-t_start))
