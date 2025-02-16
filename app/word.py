import nltk
from nltk import WordNetLemmatizer


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
