import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string

class Word:
    def __init__(self, word: str):
        self.word = word
        self.lemma = self.get_lemma(word)

    def __str__(self):
        return f"{self.word} ({self.lemma})"

    def __repr__(self):
        return f"Word({self.word}, {self.lemma})"

    def __eq__(self, other):
        return self.lemma == other.lemma

    @staticmethod
    def get_lemma(word):
        """Zwraca formę podstawową słowa."""
        lemmatizer = WordNetLemmatizer()
        tag = nltk.pos_tag([word])[0][1]
        if tag.startswith("V"):
            pos = "v"
        elif tag.startswith("J"):
            pos = "a"
        elif tag.startswith("R"):
            pos = "r"
        elif tag.startswith("N"):
            pos = "n"
        else:
            pos = "n"
        return lemmatizer.lemmatize(word, pos=pos)


def load_known_lemmas(filename="known_lemmas.txt"):
    """Wczytuje znane słowa z pliku."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def save_known_lemma(lemma, filename="known_lemmas.txt"):
    """Dodaje nowe słowo do bazy znanych słów."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(lemma + "\n")

def get_unknown_lemmas(lemmas_grouped: dict[str, list[str]], known_lemmas: set[str]) -> list[tuple[str,list[str]]]:
    unknown_lemmas = [(lemma, orig_words_dict) for lemma, orig_words_dict in lemmas_grouped.items() if lemma not in known_lemmas]
    # group by lemma
    return unknown_lemmas

def get_lemmas_from_text(text: str) -> dict[str, set[str]]:
    words = word_tokenize(text.lower())
    lemmas_from_text = [(get_lemma(word), {word}) for word in words if word.isalpha()]
    lemmas_grouped = {}
    for lemma, word_set in lemmas_from_text:
        if lemma not in lemmas_grouped:
            lemmas_grouped[lemma] = set()
        lemmas_grouped[lemma] = lemmas_grouped[lemma].union(word_set)
    return lemmas_grouped


if __name__ == "__main__":
    # nltk.download("punkt")
    # nltk.download("punkt_tab")
    # nltk.download("averaged_perceptron_tagger_eng")
    # nltk.download("wordnet")  # Pobiera lematizer dla nltk

    # print(get_lemma('mathematics'))
    # print(get_lemma('dogs'))
    # print(get_lemma('very'))
    # print(get_lemma('better'))

    text = """
    I live in a houses near the mountains. I have two brothers and one sister, and I was born last. 
    My father teaches mathematics, and my mother is a nurse at a big hospital. 
    My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. 
    My grandmother also lives with us. She came from Italy when I was two years old. 
    She has grown old, but she is still very strong. She cooks the best food! 
    """

    lemmas_from_text = get_lemmas_from_text(text)
    # print(lemmas_from_text)
    known_lemmas = load_known_lemmas()
    unknown_lemmas = get_unknown_lemmas(lemmas_from_text, known_lemmas)
    print(f"Rozpoznane nieznane słowa: {unknown_lemmas}")
    saved_lemmas = []
    for lemma, orig_words_dict in unknown_lemmas:
        save = input(f"Czy chcesz dodać '{lemma}' do znanych słów (orig={', '.join(orig_words_dict)})? (tak/nie/exit): ")
        if save.lower() == "tak":
            for word in orig_words_dict:
                saved_lemmas.append(lemma)
                save_known_lemma(lemma)
        elif save.lower() == "exit":
            break
        else:
            print("Nie dodano do listy znanych słów.")

    print(f"Dodano do listy znanych słów: {', '.join(saved_lemmas)}")
    print(f"Pozostało do nauki: {len(unknown_lemmas) - len(saved_lemmas)}")

