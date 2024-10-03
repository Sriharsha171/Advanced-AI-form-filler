import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def encode_text(text):
    return model.encode(text)

def map_fields_to_knowledge_base(form_fields, knowledge_base):
    kb_keys = list(knowledge_base.keys())
    kb_embeddings = encode_text(kb_keys)

    field_mappings = {
        form_field['field_name']: knowledge_base[kb_keys[np.argmin(np.linalg.norm(kb_embeddings - encode_text(form_field['field_name']), axis=1))]]
        for form_field in form_fields
    }

    return field_mappings