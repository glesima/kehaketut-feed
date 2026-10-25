# Riihimäen Kehä-Ketut – verkkosivun automaatio

**Tilanne 25.10.2026:** käytössä oleva GitHub Pages -integraatio, jossa GitHub Actions hakee julkisia BoxerBase-ottelu- ja urheilijatietoja sekä Yhdistysavaimen uutisia. Seuran Instagram-kuvavirta tulee Juicerista, ja Facebookin erillinen korttinäkymä perustuu yhdistetyn Metricool-brändin tietoihin. GitHub Pages ja Yhdistysavaimen HTML-lohkot muodostavat julkisen etusivun automaattiset osat.

## Lue nämä ensin

- [Tehdyt muutokset ja nykyinen tila](docs/TOTEUTUS_JA_TILANNE_2026-10-25.md)
- [Jatkosuunnitelma ja keskeneräiset työt](docs/JATKOSUUNNITELMA.md)
- [Uusien ottelutulosten automaattisen julkaisun toteutusmäärittely](docs/AUTOMAATTISET_OTTELUT_2026-10-25.md)
- [Lyhyt tekninen jatko-ohje seuraavaan keskusteluun](docs/TEKNINEN_JATKOSEURAAVAAN_KESKUSTELUUN.md)
- [Uutis-, video-, YouTube- ja someautomaation toteutussuunnitelma](docs/SISALTOTUOTANTO_VIDEO_JA_UUTISAUTOMAATIO_2026-10-25.md)
- [Hallituksen ohje sisällöntuotantoon](docs/HALLITUKSEN_SISALTOOHJE.md)


- [BoxerBase-tutkimus ja toimiva julkisten ilmoittautumisten haku](docs/BOXERBASE_TUTKIMUS_JA_AUTOMAATION_TULOS_2026-10-25.md)
- [Erillisen uutisosoitteen ja kolmen hyväksyjän tietoturvasuunnitelma](docs/TURVALLINEN_SISALTOVASTAANOTTO_2026-10-25.md)

## Olennaiset linkit

- Sivusto: https://www.kehaketut.fi/
- Oikea BoxerBase-seura: https://boxerbase.com/o/1Le8shnOwPIW/boxers
- GitHub Pages: https://glesima.github.io/kehaketut-feed/
- Tulosnäkymä: https://glesima.github.io/kehaketut-feed/widget.html?view=updates
- Ottelijakortit: https://glesima.github.io/kehaketut-feed/widget.html?view=boxers
- Facebook-korttivirta: https://glesima.github.io/kehaketut-feed/facebook.html

## Ajastukset ja tekninen rakenne

- GitHub Actions: .github/workflows/update.yml – neljä ajoa vuorokaudessa, työjonon ja ajastuspalvelun toteutumisesta riippuen.
- scripts/update.py: oikean BoxerBase-seuran profiilit, tunnetut kilpailut ja ottelut.
- scripts/update_news.py: kolme uusinta uutista Kehä-Kettujen Yhdistysavaimen Uutiset-sivulta.
- docs/: GitHub Pagesin julkinen rajattu JSON/RSS-data sekä näyttökomponentit.
- embed/: Yhdistysavaimen HTML-koodiosioihin liitettävät katkelmat.
- tests/: paikallisesti ajettavat testit komennolla python -m unittest discover -s tests -v.
- Facebook-syöte: ChatGPT:ssä erikseen ajastettu päivittäinen Metricool-tietojen tuonti tiedostoon docs/facebook.json; ajastuksen ensimmäisen ajon onnistuminen tulee varmistaa.

## Turva- ja toimintaperiaatteet

1. Julkiseen GitHub-repositorioon ei lisätä salasanoja, API-avaimia, maksutietoja tai muita salaisuuksia.
2. Käytetään vain yhdistyksen valtuuttamia somekanavia ja julkiseen näyttämiseen sopivaa tietoa.
3. BoxRec-lähde on poistettu pyynnöstä; ottelumääriä ei summata palvelujen välillä.
4. Tuloskortin BoxerBaseen kirjatut ottelumäärät eivät välttämättä kata koko otteluhistoriaa. Josiaksen duplikaattiprofiilille on dokumentoitu tilapäinen käsittely.
5. Ilmoittautumista kilpailuun ei näytetä vahvistettuna otteluna.
6. BoxerBase-tietojen koneellisen keruun käyttöehdot ja kestävän rajapinnan saatavuus on tarkistettava palveluntarjoajalta.
7. **Automaattista Facebook- tai Instagram-julkaisujen lähettämistä** ei ole vielä toteutettu: julkaisut valmistellaan tulevassa vaiheessa hyväksyttäviksi.

## Sisällöntuotannon ohje

Uutinen lisätään **Yhdistysavain → Uutiset → Lisää uutinen**. Etusivua ei muokata tavallista uutista varten. Etusivulla näkyy ajastuksen jälkeen kolme uusinta uutista; täydellinen arkisto säilyy Uutiset-sivulla.
