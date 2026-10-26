# Julkisen repositorion sisältöraja

Tähän repositorioon kuuluvat seuran julkinen verkkosivukoodi, julkaistava tietosyöte, synteettiset testiaineistot ja neutraalit käyttöohjeet.

## Ei julkiseen GitHubiin

- Alkuperäiset ottelu-, harjoitus- tai haastattelutallenteet ilman erillistä tarkoitusta ja julkaisupäätöstä.
- Kuvaus-/julkaisuluparekisterit, huoltajatiedot, lataajien henkilötiedot ja yksityiset lokit.
- API-avaimet, OAuth-tokenit, kirjautumistiedot, yksityiset tai allekirjoitetut medialinkit.
- Ryhmille rajattujen materiaalipyyntöjen osoitteet ja yksityiset järjestelmätunnisteet.
- Muiden organisaatioiden sisäinen aineisto, kaupalliset suunnitelmat ja julkaisemattomat tuotantosuunnitelmat.

Rajaus koskee myös issueita, PR-kuvauksia, kommentteja, GitHub Actions -lokeja ja julkaisuartifakteja. `docs/`-hakemisto julkaistaan Pagesiin; Markdown-tiedoston tekninen tiedostopääte ei tee siitä yksityistä.

## Käytä erillisiä ympäristöjä

Julkinen sivustorepositorio ja yksityinen median käsittely-ympäristö ovat eri säilytyspaikkoja. Yksityisessä ympäristössä pidetään media, suostumukset, latauskohtainen alkuperätieto, julkaisuloki ja palvelutunnukset. Julkiseen sivustoon tuodaan vain tarkoituksellisesti julkaistava lopputulos.

## Vanha sisältö

Tämä ohje ei poista aiemmin tallennettua aineistoa Git-historiasta. Vanhojen dokumenttien, issueiden ja PR-keskustelujen tarkistus on oma ylläpitotehtävänsä. Julkisen vastaanottolinkin poistaminen nykyisestä tiedostosta ei mitätöi linkkiä; sen sulkeminen tai vaihtaminen tehdään palvelussa erikseen ja koordinoidaan käyttäjien kanssa.

Historiaa ei kirjoiteta uudelleen eikä toimivia vastaanottolinkkejä suljeta automaattisesti. Salaisuuden paljastuessa tunnus perutaan tai vaihdetaan ensin, ja historiatoimet arvioidaan erikseen.

`.gitignore` vähentää tahattomia uusia lisäyksiä, mutta ei suojaa jo versionhallinnassa olevia tiedostoja eikä korvaa sisällöntarkistusta.
