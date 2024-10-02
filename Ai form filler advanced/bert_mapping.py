# bert_mapping.py

import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# Load BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def encode_text(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = torch.mean(outputs.last_hidden_state, dim=1)
    return embeddings

def map_fields_to_knowledge_base(form_fields, knowledge_base):
    field_mappings = {}
    knowledge_base_keys = [key.lower() for key in knowledge_base.keys()]

    kb_embeddings = torch.cat([encode_text(key) for key in knowledge_base_keys])

    for form_field in form_fields:
        field_name = form_field['field_name'].lower()
        form_embedding = encode_text(field_name)

        form_embedding_2d = form_embedding.numpy().reshape(1, -1)
        kb_embeddings_2d = kb_embeddings.numpy()

        similarities = cosine_similarity(form_embedding_2d, kb_embeddings_2d)

        best_match_idx = similarities.argmax()
        best_match_key = knowledge_base_keys[best_match_idx]
        best_match_value = knowledge_base[best_match_key]

        field_mappings[field_name] = best_match_value

    return field_mappings
