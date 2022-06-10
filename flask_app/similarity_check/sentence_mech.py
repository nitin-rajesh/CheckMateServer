from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class sentence_mech:
    def __init__(self) -> None:
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        pass

    def compare(self, str1, str2):
        sentences = [str1,str2]
        sentence_embeddings = self.model.encode(sentences)
        print(sentence_embeddings)
        print(sentence_embeddings.shape)

        val = cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])
        
        return str(val[0][0])