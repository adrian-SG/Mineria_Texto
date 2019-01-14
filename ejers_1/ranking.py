from ejers_1.utils import clean_tonkenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RankingIndex:


    def __init__(self, path_list):
        """
        initializes the new RankingIndex instance by storing path_list
        :param path_list: list of file paths to be indexed
        """
        self.path_list = path_list

    def get_simlilarity(self, text_to_query):
        """
        gets the similarity between corpus and text_to_query
        :param text_to_query: text_to_query in corpus
        :return: similarity between corpus and text_to_query
        """

        texts = []

        for path in self.path_list:
            with open(path) as file:
                texts.append(file.read())
        texts.append(text_to_query)

        tfidf = TfidfVectorizer(tokenizer=clean_tonkenize)
        tfidf_matrix = tfidf.fit_transform(texts)

        return cosine_similarity(tfidf_matrix)



class RankingQuery:

    def __init__(self, ranking_index):
        """
        initializes the new BasicQuery instance by setting the BasicIndex to query
        :param basic_index: index to query
        """
        self.ranking_index = ranking_index

    def query(self, query):
        return self.order_texts(self.ranking_index.get_simlilarity(query))


    # Se ordenan los textos obtenidos para proporcionar los más relacionados al principio de la lista.
    def order_texts(self, similarity):
        # Se obtiene la fila completa.
        sim_rows = similarity[0:, -1]
        index_ordering = {}
        for i in range(0, len(sim_rows)):
            # Se guarda cada valor para no perderlo al ordenar
            index_ordering[sim_rows[i]] = i
            # Se ordena la lista
        sim_cols_ordered = sorted(sim_rows, reverse=True)
        files = []

        for col in sim_cols_ordered:
            # Se recuperan los nombres de los ficheros originales
            # salvo el propio(tiene similaridad 1 consigo mismo).
            if col < 1:
                files.append(self.ranking_index.path_list[index_ordering[col]])
        return files



''' Prueba de concepto'''
print("Ranking: prueba de concepto")
import datetime
t_start = datetime.datetime.now()

t_ranking_index = RankingIndex(['.\corpus\pg135.txt',
                            '.\corpus\pg76.txt',
                            '.\corpus\pg5200.txt'])
t_query = RankingQuery(t_ranking_index)
print(t_query.query("The house was in England"))
t_finish = datetime.datetime.now()
print("Total time: %s" % str(t_finish-t_start))
