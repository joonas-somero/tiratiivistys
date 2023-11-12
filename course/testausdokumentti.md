# Testausdokumentti

## Suorituskykytestaus

Algoritmien toteutuksien suorituskykyä tiedoston pakkaamisessa on vertailtu repositorion juuresta löytyvän tiedoston [_compare.py_](../compare.py) sisältämällä Python-skriptillä.

```bash
$ python compare.py
```

```text
Fetching 'Alice's Adventures in Wonderland' from www.gutenberg.org...
Fetching 'Kalevala' from www.gutenberg.org...
...
```

Skripti noutaa verkosta luonnollista kieltä sisältävää materiaalia, pakkaa sen käyttäen vertailtavia algoritmejä ja kirjoittaa vertailun tulokset tiedostoon. Skriptin sisältämien vakioiden &ndash; `BOOKS` ja `SUPPLEMENTAL` &ndash; esimerkkisisällöllä saadun vertailun tulokset on esitelty toteutusdokumentin kohdassa [_Suorituskykyvertailu_](toteutusdokumentti.md#suorituskykyvertailu).


## Yksikkötestaus

Hakemistosta [_tests_](../tests/) löytyvät yksikkötestit suoritetaan komennolla `python -m unittest discover --verbose`.


### Testikattavuus

Rivikattavuus selviää komennolla `coverage run -m unittest discover`, haaraumakattavuus komennolla `coverage run --branch -m unittest discover`. Kattavuusraportti tulostuu komennolla `coverage report`.


#### Kattavuusraportti

[![codecov](https://codecov.io/gh/joonas-somero/tiratiivistys/graph/badge.svg?token=ES3YTXJVHD)](https://codecov.io/gh/joonas-somero/tiratiivistys)

Raportti on nähtävillä Codecov-palvelussa, osoitteessa [https://app.codecov.io/gh/joonas-somero/tiratiivistys](https://app.codecov.io/gh/joonas-somero/tiratiivistys).


## Staattinen analyysi

Koodityylin voi tarkistaa komennolla `python -m pycodestyle .`.
