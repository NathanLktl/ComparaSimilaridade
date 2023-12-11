import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter


def preprocess_text(text):
    tokenizer = RegexpTokenizer(r'[A-z]\w*')
    tokens = tokenizer.tokenize(text)

    stop_words = set(stopwords.words('portuguese'))
    ListaSW = ['[', ']']
    stop_words.update(ListaSW)
    tokens = [palavra for palavra in tokens if palavra.lower() not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(palavra) for palavra in tokens]

    return tokens


def get_synonyms(palavra):
    synonyms = []
    for syn in wordnet.synsets(palavra, lang='por'):
        for lemma in syn.lemmas('por'):
            synonyms.append(lemma.name())
    return synonyms


def calculate_overlap_percentage(text1_keywords, text2_keywords):
    overlap_count = sum((text1_keywords & text2_keywords).values())
    total_terms = sum((text1_keywords | text2_keywords).values())

    if total_terms == 0:
        return 0
    else:
        return (overlap_count / total_terms) * 100


def calculate_occlusion_percentage(occlusion_count, total_keywords):
    if total_keywords == 0:
        return 0
    else:
        return (occlusion_count / total_keywords) * 100


def get_keywords(file_path, n_kw):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    tokens = preprocess_text(text)

    keywords = Counter(tokens)

    keywords = keywords.most_common(n_kw)

    return [keyword[0] for keyword in keywords]


def main():
    print("Importante: Substituir os arquivos abaixo pelos arquivos desejados antes de rodar o código")
    file_path1 = "copafut.txt"
    file_path2 = "copafutfem.txt"

    n_keywords = int(input("Diga a quantidade de palavras-chave desejadas: "))

    keywords1 = get_keywords(file_path1, n_keywords)
    keywords2 = get_keywords(file_path2, n_keywords)

    oclusoes_count = 0

    for palavra1 in keywords1:
        if palavra1 in keywords2:
            oclusoes_count += 1

    consider_synonyms = input("Deseja considerar sinonimos? (S/N): ").lower()
    if consider_synonyms == 's':
        for palavra in set(keywords1):
            synonyms = get_synonyms(palavra)
            for synonym in synonyms:
                if synonym in set(keywords2):
                    keywords2.append(synonym)
                    oclusoes_count += 1

    total_keywords = len(set(keywords1 + keywords2))
    occlusion_percentage = calculate_occlusion_percentage(
        oclusoes_count, total_keywords)

    print("\nPalavras-chave do Texto 1:", keywords1)
    print("\nPalavras-chave do Texto 2:", keywords2)
    print("\nNúmero de Oclusões:", oclusoes_count)
    print("\nPercentual de Oclusão:", occlusion_percentage, "%")


if __name__ == "__main__":
    main()
