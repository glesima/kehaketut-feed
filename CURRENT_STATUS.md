# Nykytila ja tunnetut rajat

Tarkistus 27.10.2026. Tarkistuksen lähtökohta: `182fb1239f4a22c62e0f01c7ebf634663f77d49e`.

## Vahvistettu

- Viimeisin tarkistettu Pages-ajo `40395207746` onnistui. Siinä yksikkötestit, uutishaku ja julkaisu päättyivät onnistuneesti.
- Muutosesitys #23:n tarkistusajo `40395128567` onnistui.
- Uutispäivämäärien korjaukset, suora uutislistahaku, mukautuva otsikkokoko ja `news-loader.js` ovat päähaarassa. Ylläpitäjä ilmoitti vaihtaneensa etusivun lataajaosoitteen. Tämä on ylläpitäjän vahvistus, ei tässä tarkistuksessa toistettu selainmittaus.
- Aiemmat kilpailuvideopilotit ovat julkaistuina kolmessa somekanavassa. Vanhat 'ei julkaistu' -pilottiluonnokset kuvaavat niiden aikaisempaa vaihetta.
- Materiaalien vastaanottolinkki on ylläpitäjän testaama. Varsinaiset vastaanotto- ja käyttöoikeustiedot pidetään rajatussa ylläpidossa.

## Ei vielä tuotantokäytössä kokonaisuutena

- Yksityinen jatkuva Dropbox-vastaanotto ja sen asennus käyttäjän laitteelle.
- Eri lataajien tiedostojen luotettu tapahtumakytkentä, tapahtumakohtainen odotusikkuna ja myöhästyvän materiaalin käsittely.
- Uudelleenpakattujen tai leikattujen saman tallenteen versioiden tunnistus. Nykyinen SHA-256-tarkistus löytää vain täsmälleen saman sisällön.
- Monikameramateriaalin synkronointi ja automaattinen toimituksellinen valinta.
- Jatkuva renderöinnin ja kolmen kanavan julkaisun yhdistävä palvelu, julkaisukohtainen lukitus sekä osittaisen onnistumisen palautuminen.
- Kiireellisten uutisten itsenäinen Facebook-jakeluyhteys.

## Tarkistuksessa havaitut ylläpitokohteet

1. Päivätyissä suunnitelmissa on keskenään eri työvaiheita. README ja tämä tiedosto ovat ajantasaisen tilannekuvan aloituspiste; historiallista aineistoa ei poisteta automaattisesti.
2. Nykyinen paikallinen vastaanotto-ohjelma ei poista tai mitätöi kaikkia aikaisempia handoff-tiedostoja lähteen vaihtuessa. Jatkossa renderöijän pitää aina tarkistaa lähteen nykyinen versio/hash, ei luottaa irralliseen vanhaan JSON-tiedostoon.
3. Vastaanoton virhetiloille tarvitaan rajattu uudelleentarkistus. Muuttumaton tiedosto voi jäädä virhetilaan tilapäisen lukemisvirheen jälkeen.
4. SHA-256 ei yksin erota saman ottelun eri kameroita tai saman videon uudelleenpakattua kopiota. Nämä ovat eri käsittelytapauksia.
5. Julkiset käyttöönotto-ohjeet tulee erottaa yksityisistä käyttöoikeus-, vastaanotto- ja tuotantotiedoista. Julkisuustarkastus kattaa myös historiatiedot ja issue-/PR-keskustelut.
6. Testien kattavuutta pitää laajentaa edellä mainittuihin tilanteisiin ennen jatkuvan julkaisun käyttöönottoa.

## Julkaisun todentaminen

Ilmoituksen lähettäminen ei tarkoita onnistunutta somejulkaisua. Instagramin aiemmassa pilotissa `Auto publish=OFF` johti mobiili-ilmoitukseen, ei näkyvään Reeliin. Lopullinen tila varmennetaan kanavakohtaisella julkaisutunnisteella ja julkisella osoitteella tai vastaavalla alustakohtaisella lukutarkistuksella.

## Muutosten rajaus

Tämä tilapäivitys ei asenna palvelua, muuta somekanavien asetuksia, ajasta julkaisuja, muuta julkaisulupia tai siirrä yksityistä materiaalia julkiseen repositorioon. Repositorion täydellistä virheettömyyttä tai kaikkien historiaversioiden sisältöä ei ole sertifioitu.
