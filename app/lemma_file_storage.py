class LemmaFileStorage:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def load_lines_to_set(self) -> set[str]:
        """Wczytuje znane słowa z pliku."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return set(file.read().splitlines())
        except FileNotFoundError:
            return set()

    def save(self, lemma: str) -> None:
        """Dodaje nowe słowo do bazy znanych słów."""
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(lemma + "\n")
