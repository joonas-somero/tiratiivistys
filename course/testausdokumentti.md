# Testausdokumentti

## Yksikkötestaus

Testit suoritetaan komennolla `python -m unittest discover --verbose`.


### Testikattavuus

Rivikattavuus selviää komennolla `coverage run -m unittest discover`, haaraumakattavuus komennolla `coverage run --branch -m unittest discover`. Kattavuusraportti tulostuu komennolla `coverage report`.


#### Kattavuusraportti

[![codecov](https://codecov.io/gh/joonas-somero/tiratiivistys/graph/badge.svg?token=ES3YTXJVHD)](https://codecov.io/gh/joonas-somero/tiratiivistys)

Raportti on nähtävillä Codecov-palvelussa, osoitteessa [https://app.codecov.io/gh/joonas-somero/tiratiivistys](https://app.codecov.io/gh/joonas-somero/tiratiivistys).


## Staattinen analyysi

Koodityylin voi tarkistaa komennolla `python -m pycodestyle .`.
