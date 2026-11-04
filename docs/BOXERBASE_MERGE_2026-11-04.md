# BoxerBase-lähteen yhdistäminen 4.11.2026

## Yksi lähdeseura

Säilyvä lähde on **RIIHIMÄEN KEHÄ-KETUT**, `mZjkT0LW248X`:
https://boxerbase.com/o/mZjkT0LW248X/boxers

Vanha `1Le8shnOwPIW` on yhdistetty tähän. Sivuston nimeä tai typografiaa ei muuteta suuraakkosiksi. Historiallisissa ottelukorteissa voi yhä näkyä aiempi nimi Riihimäen Kehä-Ketut ry; tämä on saman seuran aiempi lähdemerkintä, ei toinen seurattava organisaatio.

## Varmennetut profiilit

Julkisen yhdistetyn seuralistan ja profiilien seuraviittausten tarkistus 4.11.2026:

| Ottelija | Vanha tunniste | Yhdistetty profiili |
|---|---|---|
| Daniela Taskila | KyEKnjm-NRp4 | Pi3gCaWD-7jD |
| Gleb Simanov | U2N_OOYxyFui | h9XYEbAs3Py4 |
| Ilo Grönroos | 0efaqUGeO1JP | W9dy-RM88aLL |
| Josias Joseph Ndikumana | rLyNGj8sCoF7 | vfT3Q-X7B3Tf |
| Kosmo Grönroos | RGUkxNVIo4px | jRMAAn1JtaN6 |
| Maarjo Ranne | 5A-7Dh4jmTdy | ir_z7p9BvsZM |
| Otso Västilä | CVjkkb7fii6a | RyBcZO1fI2Rb |
| Rami Vuori | 2zTFqL5gFsqg | nqzy3scM-NDs |
| Simo Pöyry | vK0bN2sPxnbo | PxXnRMHDTclP |

Profiiliosoitteen muoto on `https://boxerbase.com/boxer/<tunniste>`.

## Säilyttäminen ja yhteensopivuus

- `confirmed_club_merge` sallii vain tämän tarkistetun seuranvaihdon. Aiemmat tulokset ja havaintoajat säilytetään. Muun seuran tietoja ei siirretä automaattisesti.
- Profiilien tilastoja ei summata. Tilapäinen Josias-rinnakkaisprofiilin käyttö on poistettu asetuksista; lähteenä on yksi yhdistetty profiili.
- Ilmoittautumisten ottelijatunnisteet muutetaan ennen täydennystä ja samoihin tapahtumiin kuuluvat saman ottelijan havainnot yhdistetään. Vanhaa havaintoa ei merkitä uudeksi tarkistukseksi pelkän tunnistevaihdon vuoksi.
- Päivitys pysähtyy ensimmäisessä siirrossa, jos koko tunnettu yhdistetty ottelijajoukko ei löydy; aiempi syöte säilyy.
- Profiilien julkiset ottelulinkit otetaan mukaan tapahtumahakuun. Näin yhdistymisen myötä näkyvät historialliset ottelut eivät jää vain tulevien kilpailujen haun varaan.
- Vanhoja `widget.html?view=profile&id=...`-upotuksia tuetaan tunnistekartalla. Nykyinen `profile-embed.js` käyttää uusia tunnisteita.
- `boxerbase-links.js` vaihtaa sivulla vain tarkistetut vanhat BoxerBase-seura-/profiililinkit uusiin. Historialliset tapahtuma-/ottelulinkit ja muut sivut säilyvät. Lataus nykyisistä news-loader/profile-embed-kytkennöistä; Yhdistysavaimen tallennettua alkuperäis-HTML:ää ei tällä muutoksella kirjoiteta uudelleen.

## Lähteen koontiluvut: tarkistettava poikkeus

4.11.2026 julkisista profiiliotsikoista luettiin neljä ristiriitaista yhteenvetoa:

| Profiili | Otteluja | Voittoja | Tappioita |
|---|---:|---:|---:|
| Daniela Taskila | 6 | 4 | 4 |
| Gleb Simanov | 4 | 0 | 5 |
| Kosmo Grönroos | 13 | 5 | 9 |
| Maarjo Ranne | 7 | 1 | 7 |

Nämä ovat lähteestä havaittuja lukuja, eivät sivuston laskemia yhdistelmiä. Voittojen ja tappioiden summa ylittää ottelumäärän. Täsmällistä syytä ei päätellä; yhdistämisen ajallinen yhteys ei yksin todista virheen syytä. Julkinen JSON säilyttää lähdearvot ja merkitsee `stats_consistency=inconsistent`. Näyttö korvaa ristiriitaisen yhteenvedon tarkistusmerkinnällä; yksittäiset varmennetut tulokset ja lähdeprofiililinkki säilyvät. Kun lähde palauttaa taas sisäisesti eheät luvut, normaali näkymä palautuu seuraavalla onnistuneella päivityksellä.

## Tarkistukset ja rajat

Lähdeauditit `41921839137` ja `41922295972` lukivat yhdistetyn seuralistan ja yhdeksän profiilia GitHub Actionsissa. Raportteihin ei tallennettu syntymäaikoja, lisenssejä tai yksityisiä viestejä. Paikallinen Python-testiajo: 150 testiä, yksi aiempi valinnainen testi ohitettu. Node-testit varmistavat vanhojen tunnisteiden toiminnan, linkkien rajauksen, tuloshistorian ja ristiriitaisten lukujen näyttökäytännön. Nämä eivät yksin todista tuotantoon julkaisua; ajantasainen julkaisutulos kirjataan `CURRENT_STATUS.md`:hen.

Tämä muutos ei julkaise someen, muokkaa BoxerBase-lähdetietokantaa tai muuta media-vastaanotinta, kuvaajan lomaketta tai muiden projektien ajoja. Historialliset sivut ja raportit säilyvät historiallisina.
