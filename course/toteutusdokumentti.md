# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelman lähdekoodi löytyy hakemistosta `src/tiratiivistys/`, jonka sisältö on pääpiirteittäin seuraavanlainen.

- `bit_io.py`: Tiedoston sisältöä mm. bitti kerrallaan lukeva/kirjoittava moduuli
    * `BitReader`: Luokka lukemiseen
    * `BitWriter`: Luokka kirjoittamiseen
- `classes.py`: Abstraktit luokat
- `compressor.py`
    * `Compressor`: Algoritmien toteutuksia tiedostojen pakkaamiseen/purkamiseen käyttävä luokka
- `constants.py`: Ohjelman käyttämät vakiot
- `user_interface.py`: Click-pakkauksen avulla toteutettu ohjelman käyttöliittymä
- `huffman/`: Huffman-koodauksen toteuttava moduuli
    * `decoder.py`
      - `HuffmanDecoder`: Luokka Huffman-koodauksella pakatun tiedoston purkamiseen
    * `encoder.py`
      - `HuffmanEncoder`: Luokka tiedoston pakkaamiseen Huffman-koodauksella
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
    * `token.py`
        - `LempelZivToken`: LZ77-algoritmin käyttämiä kolmikkoja käsittelevä luokka
    * `window.py`
        - `SlidingWindow`: LZ77-algoritmin _sliding window_ -tekniikan toteuttava luokka
        - `TokenWindow`: Kirjanpitoluokka LZ77-algoritmilla pakatun tiedoston palauttamiseen
