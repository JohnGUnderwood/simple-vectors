import math
from sklearn.metrics.pairwise import cosine_similarity

def dotProduct(a,b):
    dotproduct = 0.0
    for k,v in enumerate(a):
        dotproduct+=a[k]*b[k]
    return dotproduct

def normalize(v):
    sum_of_squares = 0.0
    for i in v:
        sum_of_squares+=math.pow(i,2)

    return [x / math.sqrt(sum_of_squares) for x in v]

def vectorSearch(collection,input,inputVector,algo,normalized=True):
  pipeline = [
    {
      "$search": {
        "index": "default",
        "knnBeta": {
          "vector": normalize(inputVector) if normalized else inputVector,
          "path": "2d.{}.{}".format('normalized' if normalized else 'raw',algo),
          "filter": {
            "compound": {
              "must":[
                  {
                    "text":{
                        "query":"animal",
                        "path":"type"
                    }
                  }
              ],
              "mustNot":[
                {
                  "equals":{
                    "value":input["_id"],
                    "path":"_id"
                  }
                }
              ]
            }
          },
          "k": 1
        }
      }
    }
  ]

  return list(collection.aggregate(pipeline))

def maximal_marginal_relevance(sentence_vector, documents, embedding_matrix, lambda_constant=0.5, threshold_docs=10):
    """
    With thanks to: https://gist.github.com/aditya00kumar/011b6ad309de616e15c32b5efcd9f66d#file-mmr-py
    Return ranked documents using MMR. Cosine similarity is used as similarity measure.
    :param sentence_vector: Query vector
    :param phrases: list of candidate documents
    :param embedding_matrix: matrix having index as document ID and values as vector
    :param lambda_constant: 0.5 to balance diversity and accuracy. if lambda_constant is high, then higher accuracy. If lambda_constant is low then high diversity.
    :param threshold_docs: number of terms to include in result set
    :return: Ranked documents with score
    """
    # todo: Use cosine similarity matrix for lookup among phrases instead of making call everytime.
    s = []
    r = documents.index.to_list()
    while len(r) > 0:
        score = 0
        docid_to_add = ''
        for i in r:
            first_part = cosine_similarity([sentence_vector], [embedding_matrix.loc[i]])[0][0]
            second_part = 0
            for j in s:
                cos_sim = cosine_similarity([embedding_matrix.loc[i]], [embedding_matrix.loc[j['_id']]])[0][0]
                if cos_sim > second_part:
                    second_part = cos_sim
            equation_score = lambda_constant*(first_part - (1-lambda_constant)*second_part)
            if equation_score > score:
                score = equation_score
                docid_to_add = i
        if docid_to_add == '':
            docid_to_add = i
        r.remove(docid_to_add)
        doc_to_add = documents.loc[docid_to_add].to_dict()
        doc_to_add['score'] = score
        doc_to_add['_id']=i
        s.append(doc_to_add)
    return (s, s[:threshold_docs])[threshold_docs < len(s)]