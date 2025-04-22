from pdfminer.high_level import extract_text
import json

text = "../"

path_corpus = "../artigos_serializados.json"

dados = {
    "conferencia_principal": [
    ]
    }

with open(path_corpus, "r", encoding="utf-8") as file:
    articles_json = json.load(file)

conf_principal = articles_json["Conferência Principal"]

for conf in conf_principal:
    artigo_path = text + conf["storage_key"]
    conf["artigo_completo"] = extract_text(artigo_path)
    dados["conferencia_principal"].append(conf)

with open("corpus_artigos.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)