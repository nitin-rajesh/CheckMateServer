from datasets import *
from tokenizers import *
from transformers import *
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class sentence_mech:

    def __init__(self) -> None:
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        pass

    def __init__(self, model_path, tokenizer_path) -> None:
        self.model = BertModel.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        pass

    def __init__(self, common_path) -> None:
        self.bertinit = SentenceTransformer('bert-base-nli-mean-tokens')
        self.model = BertModel.from_pretrained(common_path)
        self.tokenizer = AutoTokenizer.from_pretrained(common_path)
        pass

    def compareStrs(self, str1, str2, flag):
        tokens = {'input_ids':[],'attention_mask':[]}
        sentences = [str1,str2]
        for sentence in sentences:
            # encode each sentence and append to dictionary
            new_tokens = self.tokenizer.encode_plus(sentence, max_length=128,
                                            truncation=True, padding='max_length',
                                            return_tensors='pt')
            tokens['input_ids'].append(new_tokens['input_ids'][0])
            tokens['attention_mask'].append(new_tokens['attention_mask'][0])

        # reformat list of tensors into single tensor
        tokens['input_ids'] = torch.stack(tokens['input_ids'])
        tokens['attention_mask'] = torch.stack(tokens['attention_mask'])

        outputs = self.model(**tokens)
        #outputs.keys()
        embeddings = outputs.last_hidden_state

        attention_mask = tokens['attention_mask']
        #attention_mask.shape

        mask = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
        #mask.shape

        masked_embeddings = embeddings * mask
        masked_embeddings.shape

        summed = torch.sum(masked_embeddings, 1)
        #summed.shape

        summed_mask = torch.clamp(mask.sum(1), min=1e-9)
        #summed_mask.shape

        mean_pooled = summed / summed_mask

        mean_pooled = mean_pooled.detach().numpy()

        simVal = cosine_similarity(
            [mean_pooled[0]],
            mean_pooled[1:]
        )

        return simVal[0][0]

    def compareStr(self, str1, str2, flag):
        sentences = [str1,str2]
        sentence_embeddings = self.bertinit.encode(sentences)
        # print(sentence_embeddings)
        # print(sentence_embeddings.shape)

        val = cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])
        
        return val[0][0]

        
if __name__ == '__main__':
    sm = sentence_mech('/Users/nitinrajesh/Code/FantomCode/FC11-404/flask_app/bert_model/custom-bert')
    str = ['We cannot play outside because it is sunny','The world is round']
    print(sm.compareStrs(str[0],str[1],0))
