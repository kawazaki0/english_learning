from typing import Iterator

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string
# from typing import List, Set

class Word:
    def __init__(self, word: str):
        self.lemma = self.get_lemma(word)
        self.known_variants = {word}

    def __str__(self) -> str:
        return f"{self.lemma} ({', '.join(self.known_variants)})"

    def __repr__(self) -> str:
        return f"{self.lemma} ({', '.join(self.known_variants)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return NotImplemented
        return self.lemma == other.lemma

    @staticmethod
    def get_lemma(word: str) -> str:
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

class Dictionary:
    def __init__(self) -> None:
        self.words: list[Word] = []

    def add(self, word: Word) -> None:
        for i, w in enumerate(self.words):
            if word == w:
                self.words[i].known_variants = w.known_variants.union(word.known_variants)
                return
        self.words.append(word)

    def __iter__(self) -> Iterator[Word]:
        return iter(self.words)

    def __str__(self) -> str:
        return ", ".join(str(word.lemma) for word in self.words)

    def __repr__(self) -> str:
        return f"WordSet({self.words})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Dictionary):
            return NotImplemented
        return self.words == other.words

def load_known_lemmas(filename: str = "known_lemmas.txt") -> set[str]:
    """Wczytuje znane słowa z pliku."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def save_known_lemma(lemma: str, filename: str = "known_lemmas.txt") -> None:
    """Dodaje nowe słowo do bazy znanych słów."""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(lemma + "\n")

def get_unknown_words(word_set: Dictionary, known_lemmas: set[str]) -> list[Word]:
    unknown_words = [word for word in word_set if word.lemma not in known_lemmas]
    # group by lemma
    return unknown_words

def get_lemmas_from_text(text: str) -> Dictionary:
    words = word_tokenize(text.lower())
    words_from_text = [Word(word) for word in words if word.isalpha()]
    words_grouped: Dictionary = Dictionary()
    for word in words_from_text:
        words_grouped.add(word)
    return words_grouped


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

    word_set: Dictionary = get_lemmas_from_text(text)
    # print(lemmas_from_text)
    known_lemmas: set[str] = load_known_lemmas()
    unknown_lemmas: list[Word] = get_unknown_words(word_set, known_lemmas)
    print(f"Rozpoznane nieznane słowa: {unknown_lemmas}")
    saved_lemmas: list[str] = []
    for word in unknown_lemmas:
        save: str = input(f"Czy chcesz dodać '{word.lemma}' do znanych słów (orig={', '.join(word.known_variants)})? (tak/nie/exit): ")
        if save.lower() == "tak":
            saved_lemmas.append(word.lemma)
            save_known_lemma(word.lemma)
        elif save.lower() == "exit":
            break
        else:
            print("Nie dodano do listy znanych słów.")

    print(f"Dodano do listy znanych słów: {', '.join(saved_lemmas)}")
    print(f"Pozostało do nauki: {len(unknown_lemmas) - len(saved_lemmas)}")