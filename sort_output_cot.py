import json
import re

# This file is use to format the Chain of thought prompting output from LlaMa, 
# in order to used for further measurement
# The formatted output will be sorted_answer_cot.json

with open('D:\\UVA\\NLP\\NLP-Tiny-Project\\answers_chain-of-thought.json', 'r') as answers_file:
    answers_data = json.load(answers_file)
sorted_answers = {}
sorted_file_path = 'D:\\UVA\\NLP\\NLP-Tiny-Project\\sorted_answer_cot.json'

###############################################################################
# Sort the responses based on the receipts
for key, sentences in answers_data.items():
    match_responses = []
    for response in answers_data.get("answers", []):
        if any(sentence in response for sentence in sentences):
            match_responses.append(response)
    sorted_answers[key] = match_responses

with open(sorted_file_path, 'w') as sorted_file:
    json.dump(sorted_answers, sorted_file, indent=4)


###############################################################################
# clean the extra, and inrrelavant content in response
with open(sorted_file_path, 'r') as file:
    sorted_answers_data = json.load(file)
# Function to clean up extra content and keep sentences start with numbers
def clean_content(content):
    numbered_lines = re.findall(r'\n\d+\..*', content)
    return "\n".join(line.strip() for line in numbered_lines)

cleaned_answers = [clean_content(answer) for answer in sorted_answers_data.get("answers", [])]
sorted_answers_data["answers"] = cleaned_answers
with open(sorted_file_path, 'w') as file:
    json.dump(sorted_answers_data, file, indent=4)


###############################################################################
# remove the duplicate in response
with open(sorted_file_path, 'r') as file:
    sorted_answers_data = json.load(file)
# Function to remove duplicates in each answer
def remove_duplicates(content):
    sentences = content.split("\n")
    # Use a set to track unique sentences
    seen = set()
    unique_sentences = []
    for sentence in sentences:
        if sentence not in seen:
            seen.add(sentence)
            unique_sentences.append(sentence)
    return "\n".join(unique_sentences)

deduplicated_answers = [remove_duplicates(answer) for answer in sorted_answers_data.get("answers", [])]
sorted_answers_data["answers"] = deduplicated_answers

with open(sorted_file_path, 'w') as file:
    json.dump(sorted_answers_data, file, indent=4)


###############################################################################
# Reformat the responses into each sentences property that contains an array of sentences, represent sequence of cooking steps
with open(sorted_file_path, 'r') as file:
    data = json.load(file)

processed_data = []
for answer in data["answers"]:
    # Split by line breaks
    sentences = answer.split("\n")
    # Remove empty strings and spaces
    cleaned_sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    processed_data.append({"sentences": cleaned_sentences})

output_path = sorted_file_path
with open(output_path, 'w') as output_file:
    json.dump(processed_data, output_file, indent=4)


###############################################################################
# Remove the repeated cooking step in each response sentence array
with open(sorted_file_path, 'r') as file:
    data = json.load(file)

processed_data = []

for entry in data:
    appearance = set()
    processed_sentences = []
    sentences_array = entry['sentences']
    for i in range(0, len(sentences_array)):
        if sentences_array[i][0:2] not in appearance:
            appearance.add(sentences_array[i][0:2])
            processed_sentences.append(sentences_array[i])
    processed_data.append({"sentences": processed_sentences})
    
with open(sorted_file_path, 'w') as output_file:
    json.dump(processed_data, output_file, indent=4)

###############################################################################
# Remove the number, and transfer to lowercase to match with format of sentences.json
with open(sorted_file_path, 'r') as file:
    data = json.load(file)

final_data = []

for entry in data:
    appearance = set()
    final_sentences = []
    sentences_array = entry['sentences']
    for i in range(0, len(sentences_array)):
        cleaned = sentences_array[i].split(". ", 1)[-1].lower()
        final_sentences.append(cleaned)
    final_data.append({"sentences": final_sentences})
    
with open(sorted_file_path, 'w') as output_file:
    json.dump(final_data, output_file, indent=4)