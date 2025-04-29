# STIL-2024

Este projeto visa a realização de uma série de atividades de processamento de linguagem natural sobre o corpus criado com os 24 artigos da conferência principal dos Anais do Simpósio Brasileiro de Tecnologia da Informação e da Linguagem Humana (STIL).

## 📚 Etapas Realizadas

### 1. [Tokenização](tokenização/)
- Utilizamos o modelo **BERTimbau** para a tokenização dos artigos.
- Cada artigo tokenizado foi salvo em uma nova chave no corpus chamada `artigo_tokenizado`, contendo uma lista de tokens.

### 2. [POS Tagging (Part-Of-Speech Tagging)](pos_tag/)
- Utilizamos o modelo fine-tunado **`lisaterumi/postagger-portuguese`**, disponível no GitHub, para a tarefa de POS tagging.

#### Tags Utilizadas
| Tag | Descrição |
|:----|:----------|
| ADJ | Adjetivo |
| ADV | Advérbio |
| ADV-KS | Advérbio conjuntivo subordinado |
| ADV-KS-REL | Advérbio relativo subordinado |
| ART | Artigo |
| CUR | Moeda |
| IN | Interjeição |
| KC | Conjunção coordenativa |
| KS | Conjunção subordinativa |
| N | Substantivo |
| NPROP | Substantivo próprio |
| NUM | Número |
| PCP | Particípio |
| PDEN | Palavra denotativa |
| PREP | Preposição |
| PROADJ | Pronome adjetivo |
| PRO-KS | Pronome conjuntivo subordinado |
| PRO-KS-REL | Pronome relativo conectivo subordinado |
| PROPESS | Pronome pessoal |
| PROSUB | Pronome nominal |
| V | Verbo |
| VAUX | Verbo auxiliar |

### 3. [Estatísticas do Corpus](Estatistica/)
Foram extraídas as seguintes informações:
- Número total de sentenças
- Número médio de sentenças por artigo
- Número total de tokens
- Número médio de tokens por artigo
- Top 10 tokens mais frequentes
- Bottom 10 tokens menos frequentes
- Número de substantivos
- Número de verbos
- Número de preposições

> 🔹 [As estatísticas gerais foram salvas em um arquivo `.json`.](Estatistica/estatisticas_gerais_stil.json)
> 🔹 [As estatísticas por artigo foram armazenadas em um arquivo `.csv`.](Estatistica/estatisticas_individuais_stil.csv)

### 4. [Lematização](Lematização/)
- Utilizamos o framework **spaCy**, com um modelo pré-treinado para português.
- Iteramos sobre as sentenças do corpus para lematizar cada token.

### 5. [Análise de Dependência Sintática](analise_de_dependencia)
- Também com o **spaCy**, realizamos a análise de dependência sintática.
- Para cada token, foi gerado um dicionário contendo:
  - A palavra analisada
  - A relação sintática (`dep_`)
  - A palavra da qual o token depende (`head`)

## 🛠️ Tecnologias Utilizadas
- [BERTimbau](https://github.com/neuralmind-ai/portuguese-bert)
- [lisaterumi/postagger-portuguese](https://github.com/lisaterumi/pos-tagger-portuguese)
- [spaCy](https://spacy.io/)

## 🗂 [Organização dos Dados no Corpus](corpus.json)
- **Título do Artigo**: `titulo`
- **Link para as informações do artigo**: `informacoes_url`
- **Idioma do Artigo**: `idioma`
- **PDF do artigo na pasta files**: `storage_key`
- **Nome, Afiliação e Orcid dos Autores**: `autores`
- **Data que foi publicado**: `data_publicacao`
- **Resumo do Artigo**: `resumo`
- **Palavras Chaves**: `keywords`
- **Referências**: `referencias`
- **Artigo completo em formato de string (Texto Cru)**: `artigo_completo`
- **Artigo Tokenizado**: `artigo_tokenizado`
- **Artigo Separado em Sentenças**: `artigo_sentenças`
- **POS Tag**: `pos_tag_artigo`
- **Lemas**: `sentenças_lematizadas`
- **Dependências Sintáticas**: `chave analise_dependencia`
---


