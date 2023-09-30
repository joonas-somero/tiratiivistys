# Toteutusdokumentti

**Viikolla 4 alkavaan vertaisarviointiin mennessä ainoastaan komento `python -m tiratiivistys --algorithm lempel-ziv --compress <tiedoston nimi>` tekee mitään konkreettista. Komento `python -m tiratiivistys --algorithm huffman --compress <tiedoston nimi>` rakentaa muistiin Huffman-puun, mutta ei tee sillä mitään.**


## Ohjelman yleisrakenne

Ohjelman lähdekoodi löytyy hakemistosta `src/tiratiivistys/`, jonka sisältö on pääpiirteittäin seuraavanlainen. Yliviivatuista puuttuu toteutus kokonaan.

- `classes.py`: Abstraktit luokat
- `constants.py`: Ohjelman käyttämät vakiot
- `user_interface.py`: Click-pakkauksen avulla toteutettu ohjelman käyttöliittymä
- `huffman/`: Huffman-koodauksen toteuttava moduuli
    * `decoder.py`
      - ~~`HuffmanDecoder`: Luokka Huffman-koodauksella pakatun tiedoston palauttamiseen~~
    * `encoder.py`
      - ~~`HuffmanEncoder`: Luokka tiedoston pakkaamiseen Huffman-koodauksella~~
    * `tree.py`
      - `Node`, `Leaf`: Huffman-puun solmuja esittävät luokat
      - `HuffmanTree`: Huffman-puun toteuttava luokka
- `lempel_ziv/`: Lempel-Ziv LZ77-algoritmin toteuttava moduuli
    * `decoder.py`
        - ~~`LempelZivDecoder`: Luokka LZ77-algoritmilla pakatun tiedoston palauttamiseen~~
    * `encoder.py`
        - `EncodedRange`: LZ77-algoritmin käyttämiä kolmikkoja käsittelevä luokka
        - `LempelZivEncoder`: Luokka tiedoston pakkaamiseen LZ77-algoritmilla
    * `window.py`
        - `SlidingWindow`: LZ77-algoritmin _sliding window_ -tekniikan toteuttava luokka
        - ~~`CodeWordWindow`: Kirjanpitoluokka LZ77-algoritmilla pakatun tiedoston palauttamiseen.~~