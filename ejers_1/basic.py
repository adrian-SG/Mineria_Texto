from ejers_1.utils import clean_tonkenize


class BasicIndex:

    index = {}

    def __init__(self, path_list):
        """
        initializes the new BasicIndex instance by indexing file content of files from path_list
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

        file_indexed_values = self.index.get(file_path, set())

        # for line in file:
        #     for token in clean_tonkenize(line):
        for token in clean_tonkenize(file.read()):
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
print("Basic: prueba de concepto")
import datetime
t_start = datetime.datetime.now()

t_basic_index = BasicIndex(['.\corpus\pg135.txt',
                            '.\corpus\pg76.txt',
                            '.\corpus\pg5200.txt'])
t_query = BasicQuery(t_basic_index)

t_index = datetime.datetime.now()
print("index build time: %s" % str(t_index-t_start))
print(t_query.query("The house was in England"))
t_finish = datetime.datetime.now()
print("query time: %s" % str(t_finish-t_index))
print("Total time: %s" % str(t_finish-t_start))


