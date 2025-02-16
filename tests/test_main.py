import pytest
from main import Dictionary, Word, load_known_lemmas, save_known_lemma, get_unknown_words, get_lemmas_from_text

def test_get_lemma():
    word = Word("running")
    assert word.lemma == "run"

def test_add_word_to_dictionary():
    dictionary = Dictionary()
    word = Word("running")
    dictionary.add(word)
    assert len(dictionary.words) == 1
    assert dictionary.words[0].lemma == "run"

def test_save_load_known_lemmas():
    lemma = "run"
    file_path = "/tmp/test_known_lemmas.txt"
    save_known_lemma(lemma, file_path)
    known_lemmas = load_known_lemmas(file_path)
    assert "run" in known_lemmas

def test_get_unknown_words():
    dictionary = Dictionary()
    dictionary.add(Word("running"))
    dictionary.add(Word("burning"))
    known_lemmas = {"run"}
    unknown_words = get_unknown_words(dictionary, known_lemmas)
    assert unknown_words == [Word("burning")]

def test_get_lemmas_from_text():
    text = "I am running in the park."
    dictionary = get_lemmas_from_text(text)
    assert len(dictionary.words) == 6
    assert dictionary.words[0].lemma == "i"
    assert dictionary.words[1].lemma == "be"
    assert dictionary.words[2].lemma == "run"
    assert dictionary.words[3].lemma == "in"
    assert dictionary.words[4].lemma == "the"
    assert dictionary.words[5].lemma == "park"
