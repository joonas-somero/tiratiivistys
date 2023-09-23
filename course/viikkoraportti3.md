# Viikkoraportti 3, vko 38

## Työn kulku

LZ77-algoritmin totetus aloitettu _sliding window_ -tekniikan osalta. Testausta saatu hieman edistettyä. Lähdekoodin kommentointia/tyypitystä on parannettu. Refaktorointia. Testausdokumentti alustettu.

**Viikon aikana työhön käytetty aika:** n. 25 h


## **Ongelmat**

- LZ77:n tapaus, jossa "seuraavaa merkkiä" ei ole. Esim. syöte `abcabc` haluttaisiin koodata muodossa `abc[3,3,<seuraava merkki>]`. Tämä tosin ratkennee myöhemmin pakatun tiedoston palautusta toteuttaessa.
