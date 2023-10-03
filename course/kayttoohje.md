# Käyttöohje

## Poetry

Projektin riippuvuuksia hallitaan Poetryn avulla, mutta ohjelman suorituksessa käytetään ainoastaan _Click_-pakkausta lukuunottamatta Pythonin sisäänrakennettuja moduuleja. Lisäksi Poetryllä on asennettu testikattavuuden seuraamiseen _Coverage.py_, sekä koodityylin automaattiseen korjaamiseen _autopep8_. Ts., mikäli Click on saatavilla jotakin toista kautta, ei Poetryä tarvita ohjelman suorittamiseen. Sama pätee Coverageen testikattavuusraportin osalta.


## Click

Click luo automaattisesti ohjelman komennolla `python -m tiratiivistys --help` tulostaman käyttöohjeen:

```text
Usage: python -m tiratiivistys [OPTIONS] FILE

  Restore previously compressed FILE to original, or compress FILE.

Options:
  -a, --algorithm [huffman|lempel-ziv]
                                  compression algorithm to use  [required]
  -c, --compress                  compress FILE
  --help                          Show this message and exit.
```


## Testit

Testit suoritetaan komennolla `python -m unittest discover --verbose`.


## Koodityyli

Koodityylin voi tarkistaa komennolla `python -m pycodestyle .`.


## Testikattavuus

Rivikattavuus selviää komennolla `coverage run -m unittest discover`, haaraumakattavuus komennolla `coverage run --branch -m unittest discover`. Kattavuusraportti tulostuu komennolla `coverage report`.
