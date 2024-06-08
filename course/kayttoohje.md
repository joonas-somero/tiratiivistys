# Käyttöohje

> [!IMPORTANT]
> Dokumentaatiossa esitellyt komennot olettavat suorituksen tapahtuvan Poetryn luomassa virtuaaliympäristössä.


## Poetry

Projektin riippuvuuksia hallitaan _Poetry_-työkalun avulla. Projekti käyttää pakkauksia

- _click_
- _bitstring_
- _autopep8_
- _coverage_


## Click

Click luo automaattisesti ohjelman komennolla `python -m tiratiivistys --help` tulostaman käyttöohjeen:

```text
Usage: python -m tiratiivistys [OPTIONS] INPUT_FILE OUTPUT_FILE

  Compress or restore INPUT_FILE into OUTPUT_FILE, overwriting existing
  OUTPUT_FILE.

Options:
  -c, --compress / -r, --restore  operation  [required]
  -a, --algorithm [Huffman|LZW]   compression algorithm (case insensitive)
                                  [required]
  --help                          Show this message and exit.
```

Esimerkiksi tiedoston _big\_band.ensemble_ pakkaaminen tiedostoon _quartet.ensemble_ onnistuu _Lempel-Ziv-Welch_-algoritmia käyttäen komennolla

```bash
python -m tiratiivistys --compress -algorithm LZW big_band.ensemble quartet.ensemble
```

Tai hieman lyhyemmin

```bash
python -m tiratiivistys -ca lzw big_band.ensemble quartet.ensemble
```

Vastaavasti esim. Huffman-koodausta käyttäen pakatun tiedoston _skiff.boat_ palauttaminen tiedostoksi _yacht.boat_ tapahtuu komennolla

```bash
python -m tiratiivistys -ra huffman skiff.boat yacht.boat
```


## Lisätietoa

Mm. suorituskyky- ja yksikkötestaus on kuvailtu [testausdokumentissa](testausdokumentti.md). Ohjelman yleisrakenne sekä toteutusten suorituskykyvertailu löytyvät puolestaan [toteutusdokumentista](toteutusdokumentti.md).
