# Testausdokumentti

## Yksikkötestaus

Testit suoritetaan komennolla `python -m unittest discover --verbose`. Testeihin lukeutuu mm.

* EncodedRange
    - test_decode_returns_appropriate_object
    - test_decode_returns_none_for_wrong_codeword_length
    - test_encode_returns_appropriate_object_if_frame_matches
    - test_encode_returns_none_if_frame_does_not_match
    - test_literal_returns_appropriate_object
* Huffman
    - test_count_occurrences_returns_correct_total
* LempelZiv
    - test_restore

### Testikattavuus

Rivikattavuus selviää komennolla `coverage run -m unittest discover`, haaraumakattavuus komennolla `coverage run --branch -m unittest discover`. Kattavuusraportti tulostuu komennolla `coverage report`.


#### Kattavuusraportti

[![codecov](https://codecov.io/gh/joonas-somero/tiratiivistys/graph/badge.svg?token=ES3YTXJVHD)](https://codecov.io/gh/joonas-somero/tiratiivistys)

Raportti on nähtävillä Codecov-palvelussa, osoitteessa [https://app.codecov.io/gh/joonas-somero/tiratiivistys](https://app.codecov.io/gh/joonas-somero/tiratiivistys).


## Staattinen analyysi

Koodityylin voi tarkistaa komennolla `python -m pycodestyle .`.
