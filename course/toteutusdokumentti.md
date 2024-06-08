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
- `lempel_ziv/`: Lempel-Ziv-Welch-algoritmin toteuttava moduuli
    * `decoder.py`
        - `LZWDecoder`: Luokka Lempel-Ziv-Welch-algoritmilla pakatun tiedoston purkamiseen
    * `encoder.py`
        - `LZWEncoder`: Luokka tiedoston pakkaamiseen Lempel-Ziv-Welch-algoritmilla
    * `io.py`: Moduulin _bit_io.py_ luokista perivät tiedoston luku-/kirjoitusluokat
      - `LZWReader` ja `LZWWriter`
    * `dictionary.py`
        - `LZWDictionary`: Lempel-Ziv-Welch-algoritmin käyttämä sanakirjaluokka


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
Huffman Coding | 1.71 | 1.70 | 1.69 | 1.71
Lempel-Ziv-Welch | 1.92 | 1.96 | 1.87 | 1.96

Suorituskyvyn osalta on mainittava myös suorituksen tuskastuttava hitaus.


## Laajojen kielimallien käyttö

Projektissa ei ole käytössä minkäänlaista nk. laajaa kielimallia.
