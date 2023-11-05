# Käyttöohje

## Poetry

Projektin riippuvuuksia hallitaan Poetryn avulla, mutta ohjelman suorituksessa käytetään ainoastaan _Click_-pakkausta lukuunottamatta Pythonin sisäänrakennettuja moduuleja. Lisäksi Poetryllä on asennettu testikattavuuden seuraamiseen _Coverage.py_, sekä koodityylin automaattiseen korjaamiseen _autopep8_. Ts., mikäli Click on saatavilla jotakin toista kautta, ei Poetryä tarvita ohjelman suorittamiseen. Sama pätee Coverageen testikattavuusraportin osalta.


## Click

Click luo automaattisesti ohjelman komennolla `poetry run python -m tiratiivistys --help` tulostaman käyttöohjeen:

```text
Usage: python -m tiratiivistys [OPTIONS] INPUT_FILE OUTPUT_FILE

  Compress or restore INPUT_FILE into OUTPUT_FILE, overwriting existing
  OUTPUT_FILE.

Options:
  -c, --compress / -r, --restore  operation  [required]
  -a, --algorithm [Huffman|Lempel-Ziv]
                                  compression algorithm (case insensitive)
                                  [required]
  --help                          Show this message and exit.
```

Esimerkiksi tiedoston _big\_band.ensemble_ pakkaaminen tiedostoon _quartet.ensemble_ onnistuu _Lempel-Ziv_-algoritmia käyttäen komennolla

```bash
poetry run python -m tiratiivistys -ca lempel-ziv big_band.ensemble quartet.ensemble
```


## Lisätietoa

Toteutuksesta ja testauksesta löytyy lisätietoa [toteutus-](toteutusdokumentti.md) sekä [testausdokumentista](testausdokumentti.md).
