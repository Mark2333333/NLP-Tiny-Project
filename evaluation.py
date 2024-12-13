import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Update this path if needed
# The path for reordered_senteces.json, which contain correct standard answer for each receipts
file_path_standard = 'D:\\UVA\\NLP\\NLP-Tiny-Project\\reordered_senteces.json' 
# The path for sorted_answer.json, which contain response answer from llm 
file_path_response = 'D:\\UVA\\NLP\\NLP-Tiny-Project\\sorted_answer.json'

with open(file_path_standard, 'r') as f1, open(file_path_response, 'r') as f2:
    pre_data_s = json.load(f1)
    data_r = json.load(f2)

# First 100 receipts
receipt_keys = list(pre_data_s.keys())[:100]
data_s = {key: pre_data_s[key] for key in receipt_keys}
obj_avgs = []
idx = 0
for key, obj in zip(data_s, data_r):
    idx += 1
    receipt_s = data_s[key]
    receipt_r = obj['sentences']

    # Case where two receipts have different number of sentences
    if len(receipt_s) < len(receipt_r):
        receipt_s += [""] * (len(receipt_r) - len(receipt_s))
    elif len(receipt_r) < len(receipt_s):
        receipt_r += [""] * (len(receipt_s) - len(receipt_r))
    
    # Calculate cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix_s = vectorizer.fit_transform(receipt_s)
    tfidf_matrix_r = vectorizer.transform(receipt_r)

    cosine_similarities = []
    for i in range(len(receipt_s)):
        cosine_similarities.append(cosine_similarity(tfidf_matrix_s[i], tfidf_matrix_r[i])[0][0])
    
    # Calculate the average similarity for each recipet
    obj_avg = 0
    if cosine_similarities:
        obj_avg = np.mean(cosine_similarities)
    obj_avgs.append(obj_avg)
    #print(f"receipt{ idx}: {obj_avg:.4f}")

# Calculate overall average similarity
overall_average = np.mean(obj_avgs)

print(f"Overall cosine similarity for Instruction-based prompting: {overall_average:.4f}")





# COT Evaluation
###############################################################################
# Update this path if needed
# The path for reordered_senteces.json, which contain correct standard answer for each receipts
file_path_standard = 'D:\\UVA\\NLP\\NLP-Tiny-Project\\reordered_senteces.json' 
# The path for sorted_answer.json, which contain response answer from llm 
file_path_response_cot = 'D:\\UVA\\NLP\\NLP-Tiny-Project\\sorted_answer_cot.json'

with open(file_path_standard, 'r') as f1, open(file_path_response_cot, 'r') as f2:
    pre_data_s = json.load(f1)
    data_r = json.load(f2)

# First 100 receipts
receipt_keys = list(pre_data_s.keys())[:100]
data_s = {key: pre_data_s[key] for key in receipt_keys}
obj_avgs = []
idx = 0
for key, obj in zip(data_s, data_r):
    idx += 1
    receipt_s = data_s[key]
    receipt_r = obj['sentences']

    # Case where two receipts have different number of sentences
    if len(receipt_s) < len(receipt_r):
        receipt_s += [""] * (len(receipt_r) - len(receipt_s))
    elif len(receipt_r) < len(receipt_s):
        receipt_r += [""] * (len(receipt_s) - len(receipt_r))
    
    # Calculate cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix_s = vectorizer.fit_transform(receipt_s)
    tfidf_matrix_r = vectorizer.transform(receipt_r)

    cosine_similarities = []
    for i in range(len(receipt_s)):
        cosine_similarities.append(cosine_similarity(tfidf_matrix_s[i], tfidf_matrix_r[i])[0][0])
    
    # Calculate the average similarity for each recipet
    obj_avg = 0
    if cosine_similarities:
        obj_avg = np.mean(cosine_similarities)
    obj_avgs.append(obj_avg)
    #print(f"receipt{ idx}: {obj_avg:.4f}")

# Calculate overall average similarity
overall_average = np.mean(obj_avgs)

print(f"Overall cosine similarity for chain-of-thought prompting: {overall_average:.4f}")