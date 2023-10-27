# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelman lähdekoodi löytyy hakemistosta `src/tiratiivistys/`, jonka sisältö on pääpiirteittäin seuraavanlainen.

- `classes.py`: Abstraktit luokat
- `constants.py`: Ohjelman käyttämät vakiot
- `user_interface.py`: Click-pakkauksen avulla toteutettu ohjelman käyttöliittymä
- `huffman/`: Huffman-koodauksen toteuttava moduuli
    * `decoder.py`
      - `TreeIterator`: Huffman-koodauksella pakattua dataa Huffman-puun avulla lukeva luokka
      - `HuffmanDecoder`: Luokka Huffman-koodauksella pakatun tiedoston purkamiseen
    * `encoder.py`
      - `HuffmanEncoder`: Luokka tiedoston pakkaamiseen Huffman-koodauksella
    * `huffman.py`
      - `Huffman`: Rajapinta tiedostojen pakkaamiseen/purkamiseen Huffman-koodausta käyttäen
    * `node.py`
      - `HuffmanNode`: Huffman-puun solmuja esittävä luokka
    * `node_queue.py`
      - `NodeQueue`: Huffman-puun lehtisolmuista rakentava luokka
    * `tree.py`
      - `HuffmanTree`: Huffman-puun toteuttava luokka
- `lempel_ziv/`: Lempel-Ziv LZ77-algoritmin toteuttava moduuli
    * `decoder.py`
        - `LempelZivDecoder`: Luokka LZ77-algoritmilla pakatun tiedoston purkamiseen
    * `encoded_range.py`
        - `EncodedRange`: LZ77-algoritmin käyttämiä kolmikkoja käsittelevä luokka
    * `encoder.py`
        - `LempelZivEncoder`: Luokka tiedoston pakkaamiseen LZ77-algoritmilla
    * `lempel_ziv.py`
      - `LempelZiv`: Rajapinta tiedostojen pakkaamiseen/purkamiseen LZ77-algoritmiä käyttäen
    * `window.py`
        - `SlidingWindow`: LZ77-algoritmin _sliding window_ -tekniikan toteuttava luokka
        - `CodeWordWindow`: Kirjanpitoluokka LZ77-algoritmilla pakatun tiedoston palauttamiseen
