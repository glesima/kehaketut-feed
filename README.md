# Riihimäen Kehä-Ketut – verkkosivun integraatiot

Tämä julkinen repositorio sisältää seuran verkkosivun näyttökomponentit, julkisista lähteistä muodostetut tietosyötteet sekä niiden testit. Se ei ole yksityisten videoiden, käyttöoikeustodisteiden tai tuotantotunnusten säilytyspaikka.

## Ajantasainen tilanne

Ensisijainen tilannekuva: [CURRENT_STATUS.md](CURRENT_STATUS.md). Päivätyt dokumentit `docs/`-hakemistossa kuvaavat myös aiempia työvaiheita ja suunnitelmia; niitä ei tule tulkita automaattisesti tämänhetkiseksi käyttöönottotilaksi.

- Verkkosivun julkiset BoxerBase-tiedot, uutisten varasyöte ja GitHub Pages päivittyvät GitHub Actions -ajoilla.
- Etusivun uutisnäkymä hakee ensisijaisesti julkaistut uutiset suoraan Yhdistysavaimen `/uutiset/`-sivulta. Varasyöte on erikseen ajastettu. Uutista ei tarvitse julkaista uudelleen etusivulle.
- Uutisupotuksen lataajan vaihto on ylläpitäjän mukaan tehty. Käyttöönoton selaintesti on erotettava koodin yksikkötesteistä.
- Kaksi kilpailuvideopilottia on julkaistu seuran Facebookissa, Instagramissa ja YouTubessa. Tämä ei tarkoita, että jatkuva Dropboxista somekanaviin toimiva automaatio olisi käytössä.
- `scripts/media/` sisältää paikallisia prototyyppejä. Vastaanotto-ohjelma ei yksin tunnista tapahtumia, käynnistä editointia tai julkaise videoita.
- Kiireellisten tiedotteiden automaattinen Facebook-jakelu on erillinen avoin integraatio. Nykyinen ajastettu RSS-autolista ei ole välittömän tiedottamisen kanava.

## Rakenne

- `docs/`: GitHub Pagesiin julkaistavat tiedostot. **Kaikki tämän hakemiston sisältö on julkista.**
- `embed/`: Yhdistysavaimen HTML-osioihin liitettävät katkelmat.
- `scripts/`: julkisten syötteiden muodostus ja paikalliset apuohjelmat.
- `tests/`: automaattiset tarkistukset.
- `deploy/`: asennusesimerkkejä; olemassa oleva esimerkkitiedosto ei todista palvelun olevan asennettuna.

## Keskeiset ohjeet

- [Nykytila ja tunnetut rajat](CURRENT_STATUS.md)
- [Julkisen sisällön rajaus](PUBLIC_SCOPE.md)
- [Uutisten lataus ja pikaviestinnän toimintamalli](docs/PIKATIEDOTTEET_ILMAN_CHATGPT_TA_2026-10-26.md)
- [Sivuston ulkoasun asennusohje](docs/PREMIUM_SIVUSTO_ASENNUS_2026-10-26.md)
- [Paikallisen videovastaanoton ohje](scripts/media/README_intake_service.md)
- [Sivuston tekninen inventaario](docs/SIVUSTON_AUTOMAATTINEN_AUDITTI.md)

## Testit

```sh
python -m unittest discover -s tests -v
python -m compileall -q scripts
node tests/test_widget_render.js
node tests/test_news_live.js
```

Testien onnistuminen ei yksin osoita jatkuvan palvelun asennusta, julkaisulupien olemassaoloa tai onnistunutta somejulkaisua.

## Julkiset palvelut

- Seuran kotisivut: https://www.kehaketut.fi/
- Tietosyöte: https://glesima.github.io/kehaketut-feed/
- Julkaistujen seurauutisten RSS: https://glesima.github.io/kehaketut-feed/news-rss.xml

## Säilyttäminen ja tietoturva

Alkuperäinen sivuhistoria, kilpailutulokset ja lähdelinkit säilytetään. Ilmoittautumista ei esitetä vahvistettuna otteluna. Julkisessa repositoriossa ei säilytetä raakavideoita, vastaanottajien henkilötietoja, suostumusrekistereitä, salasanoja tai API-avaimia. Älä sijoita näitä myöskään issueihin, PR-kuvauksiin, testilokeihin tai GitHub Pagesin tiedostoihin.
