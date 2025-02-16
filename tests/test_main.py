from main import Dictionary, Word, LemmaFileStorage


def test_get_lemma():
    word = Word("running")
    assert word.lemma == "run"

def test_add_word_to_dictionary():
    dictionary = Dictionary()
    word = Word("running")
    dictionary._add_word(word)
    assert len(dictionary.words) == 1
    assert dictionary.words[0].lemma == "run"

def test_save_load_known_lemmas():
    lemma = "run"
    file_path = "/tmp/test_known_lemmas.txt"
    l_store = LemmaFileStorage(file_path)
    l_store.save(lemma)
    known_lemmas = l_store.load_lines_to_set()
    assert "run" in known_lemmas

def test_get_unknown_words():
    dictionary = Dictionary()
    dictionary._add_word(Word("running"))
    dictionary._add_word(Word("burning"))
    known_lemmas = {"run"}
    words = [word for word in dictionary if word.lemma not in known_lemmas]
    # group by lemma
    unknown_words = words
    assert unknown_words == [Word("burning")]

def test_get_lemmas_from_text():
    text = "I am running in the park."
    dictionary = Dictionary()
    dictionary.import_raw_text(text)
    assert len(dictionary.words) == 6
    assert dictionary.words[0].lemma == "i"
    assert dictionary.words[1].lemma == "be"
    assert dictionary.words[2].lemma == "run"
    assert dictionary.words[3].lemma == "in"
    assert dictionary.words[4].lemma == "the"
    assert dictionary.words[5].lemma == "park"
