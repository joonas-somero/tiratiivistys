# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelman lähdekoodi löytyy hakemistosta `src/tiratiivistys/`, jonka sisältö on pääpiirteittäin seuraavanlainen.

- `bit_io.py`: Tiedoston sisällön lukemista/kirjoittamista mm. bitti kerrallaan toteuttava moduuli
    * `BitReader` ja `BitWriter`
- `classes.py`: Abstrakteja luokkia sekä dataluokkia
- `compressor.py`
    * `Compressor`: Algoritmien toteutuksia tiedostojen pakkaamiseen/purkamiseen käyttävä luokka
- `constants.py`: Ohjelman käyttämät vakiot
- `user_interface.py`: Click-pakkauksen avulla toteutettu ohjelman käyttöliittymä
- `huffman/`: Huffman-koodauksen toteuttava moduuli
    * `decoder.py`
      - `HuffmanDecoder`: Luokka Huffman-koodauksella pakatun tiedoston purkamiseen
    * `encoder.py`: 
      - `HuffmanEncoder`: Luokka tiedoston pakkaamiseen Huffman-koodauksella
    * `io.py`: Moduulin _bit_io.py_ luokista perivät tiedoston luku-/kirjoitusluokat
      - `HuffmanReader` ja `HuffmanWriter`
    * `node_queue.py`
      - `NodeQueue`: Huffman-puun lehtisolmuista rakentava luokka
    * `node.py`
      - `HuffmanNode`: Huffman-puun solmuja esittävä luokka
    * `tree.py`
      - `HuffmanTree`: Huffman-puun toteuttava luokka
- `lempel_ziv/`: Lempel-Ziv LZ77-algoritmin toteuttava moduuli
    * `decoder.py`
        - `LempelZivDecoder`: Luokka LZ77-algoritmilla pakatun tiedoston purkamiseen
    * `encoder.py`
        - `LempelZivEncoder`: Luokka tiedoston pakkaamiseen LZ77-algoritmilla
    * `io.py`: Moduulin _bit_io.py_ luokista perivät tiedoston luku-/kirjoitusluokat
      - `ZempelZivReader` ja `LempelZivWriter`
    * `token.py`
        - `LempelZivToken`: LZ77-algoritmin käyttämiä kolmikkoja käsittelevä luokka
    * `window.py`
        - `SlidingWindow`: LZ77-algoritmin _sliding window_ -tekniikan toteuttava luokka
        - `TokenWindow`: Kirjanpitoluokka LZ77-algoritmilla pakatun tiedoston palauttamiseen


## Suorituskykyvertailu

Testauksessa käytettyjen luonnollista kieltä sisältävien tiedostojen koot ovat varsin maltillisia.

Tiedosto | KiB
--- | ---
Green Eggs and Ham | 1.71
Alice's Adventures in Wonderland | 173.28
Kalevala | 849.92
War and Peace | 3280.89

Kuten ovat myös saavutetut tiivistyssuhteet.

- | Green Eggs and Ham | Alice's Adventures in Wonderland | Kalevala | War and Peace
--- | --- | --- | --- | ---
Huffman | 1.71 | 1.70 | 1.69 | 1.71
Lempel-Ziv | 1.56 | 0.96 | 0.97 | 0.95

Suorituskyvyn osalta on mainittava myös suorituksen tuskastuttava hitaus.


## Laajojen kielimallien käyttö

Projektissa ei ole käytössä minkäänlaista nk. laajaa kielimallia.
