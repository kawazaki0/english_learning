from typing import Iterator

from nltk import word_tokenize

from app.word import Word


class Dictionary:
    def __init__(self) -> None:
        self.words: list[Word] = []

    def import_raw_text(self, text: str) -> None:
        words = word_tokenize(text.lower())
        words_from_text = [Word(word) for word in words if word.isalpha()]
        for word in words_from_text:
            self._add_word(word)

    def _add_word(self, word: Word) -> None:
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
