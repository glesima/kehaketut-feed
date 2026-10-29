# Nykytila ja tunnetut rajat

Päivitetty 30.10.2026. Tämä tiedosto on nykytilan aloituspiste. Päivätyt suunnitelmat kuvaavat myös aiempia työvaiheita, eivät automaattisesti tämänhetkistä käyttöönottoa.

## Harjoitukset jatkuvat 30.10.2026

Seuran vahvistuksen perusteella Kamppailukeskuksen harjoitukset jatkuvat perjantaina 30.10.2026 klo 17.00 alkaen normaalin harjoitusaikataulun mukaisesti. Peruutus 27.–29.10. on päättynyt. Korjausten valmistumisesta tai sisäilman mittaustuloksista ei esitetä erillisiä väitteitä.

- Facebook-tiedote julkaistu 30.10.2026 klo 01.40 Europe/Helsinki. Metricoolin jälkitarkistus palautti PUBLISHED-tilan, alustan postitunnisteen ja julkisen osoitteen: https://facebook.com/1570416605115618/posts/1575746574582621 . Ei uusintajulkaisua.
- Julkinen tiedotesivu: `docs/tiedotteet/harjoitukset-jatkuvat-2026-10-30.html`.
- Etusivun nykyinen `news-loader.js` lisää erillisen jatkumisilmoituksen uutisosion yläpuolelle 30.10.–5.11.2026; ilmoitus poistuu ajan perusteella 6.11. klo 00.00 Suomen aikaa. Uutisten suora Yhdistysavain-haku säilyy ennallaan. Paikallisen JavaScript-tarkistuksen yhdeksän skenaariota läpäisivät aikarajojen, duplikaattisuojan, puuttuvan kohde-elementin, DOM-valmiuden ja virhevaran testit.
- Aiempi GitHub Pagesin peruutustiedote säilyy kokonaisena ja sen alkuun lisättiin päivätty päivitys sekä linkki jatkotiedotteeseen. Vanha määräaikainen peruutusbanneri on jo vanhentunut 30.10. klo 00.00.
- Sisältöcommit `5ecf465e4a892f998ae9ae4282de5c2bd0c3b6e6`; Pages-ajon `40975026700` Deploy Pages -vaihe palautti success. Tämä ei ole riippumaton selaimen näyttötesti Yhdistysavaimen etusivusta.
- Yhdistysavaimen omaan `/uutiset/`-arkistoon ei tällä työvaiheella luotu tai muokattu artikkelia. Etusivun tiedotenosto ja erillinen julkinen tiedotesivu ovat eri julkaisupinta kuin uutisarkisto.

## Vahvistettu ja lähteen laatu

- Verkkosivun uutisnäkymän suora haku, päivämääräkorjaus, mukautuva otsikkokoko ja `news-loader.js` ovat päähaarassa. Ylläpitäjä vahvisti lataajaosoitteen vaihdon. Historiallinen onnistunut Pages-ajo: `40395207746`. Tämä merkintä ei väitä uutta selainmittausta jokaisella laitteella.
- Kolme kilpailuvideokokonaisuutta on julkaistu Facebookiin, Instagramiin ja YouTubeen: yksittäinen Hämeenlinnan ottelu, saman tapahtuman kahden ottelun yhteiskooste sekä 70 sekunnin Tampere-kooste. Viimeinen julkaistiin 28.10.2026. Julkaisuista palautuivat kanavakohtaiset tunnisteet ja julkiset osoitteet; tämä ei tarkoita jatkuvaa itsenäistä julkaisupalvelua.
- Tampere-koosteen V1:ssä raportoitiin toisto-ongelma. Ylläpitäjä vahvisti V2:n toimivan muuttamatta omia soitinasetuksiaan. Korjattua vientiprofiilia käytetään lähtökohtana; havainto ei yksin todista tietyn soittimen tai ajurin virhettä.
- Materiaalien vastaanottolinkki on testattu. Yksityinen vastaanotin v0.2.4 on nyt asennettu ylläpitäjän omalle koneelle. Ylläpitäjän toimittama tilaraportti vahvisti 27.10. aktiivisen ja automaattisesti käynnistyvän käyttäjäpalvelun, kymmenen vastaanottokierrosta, nolla peräkkäistä virhettä sekä onnistuneen Dropbox-lukukierroksen.
- Vastaanotin on tarkoituksella **receive-only**: se lataa ja tarkistaa aineiston, mutta ei renderöi tai julkaise. Koneen ja käyttäjäpalvelun käytettävyys on edellytys; ympärivuorokautista saatavuutta ei ole todistettu.
- Paikallinen v0.2.5-ottelutietolomake on toimitettu ylläpitäjälle. Sen käyttöönottoa tai ensimmäistä tallennusta käyttäjän koneella ei ole vielä vahvistettu. Paikallinen ylläpitolomake ei ole kuvaajille jaettava verkkopalvelu.

## Ei vielä tuotantokäytössä kokonaisuutena

- Ulkoisille kuvaajille tarkoitettu tapahtuma-, ottelija- ja materiaalityyppivalinnan yhdistävä lähetyspalvelu. Paikallinen pilotti ja julkinen käyttöön otettu palvelu ovat eri asioita.
- Uploaderin tietojen automaattinen yhdistäminen luotettuun ottelutietoon ja erilliseen julkaisuoikeusrekisteriin.
- Jatkuva tapahtumakohtainen keräys, odotusikkuna, myöhäisen materiaalin toimituksellinen valinta ja tuotantorenderöinti.
- Uudelleenpakattujen ja leikattujen kopioiden luotettava tunnistus. SHA-256 tunnistaa täsmälleen samat tavut, ei saman tallenteen eri pakkauksia tai eri kameroita.
- Jatkuva renderöinti–somejulkaisu-palvelu ja osittain onnistuneen kolmen kanavan julkaisun palautuminen.
- Kiireellisten uutisten itsenäinen Facebook-jakeluyhteys.

## Julkaisun ja oikeuksien todentaminen

`Sent` tai `PUBLISHED` ilman alustan tunnistetta ei yksin todista julkista näkyvyyttä. Instagramin aiemmassa pilotissa Auto publish OFF tarkoitti mobiili-ilmoitusta. Jatkossa varmistetaan automaattijulkaisun asetus ja kanavakohtainen lopputulos. Epäonnistunut kanava käsitellään erikseen; onnistuneisiin ei tehdä sokkona kaksoisjulkaisua.

Lähettäjän ilmoitus kuvausluvasta on aineiston lähdetieto, ei oikeus myöntää seuran julkaisulupia. Normaali ennalta valtuutettu aineisto on tulevan automaation tavoite; epäselvät tiedot ja luvat ohjataan poikkeuskäsittelyyn. Kiireellisen uutisen toimituksellinen julkaisu on erillinen työnkulku.

## Jatkettavuus ja julkinen sisältöraja

Katso [CONTEXT_HANDOFF.md](CONTEXT_HANDOFF.md) ja [PUBLIC_SCOPE.md](PUBLIC_SCOPE.md). Tämän julkisen repositorion tulee kuvata seuran näkyvät palvelut ja neutraali käyttöönottotila. Yksityinen mediajärjestelmän koodi, ylläpitotiedot, kuvaajien tiedot, valtuutukset ja projektikeskustelun sisäiset päätökset säilytetään erikseen. Historiatiedostojen julkisuustarkastus on edelleen erillinen tehtävä; historiaa tai toimivia vastaanottolinkkejä ei poisteta automaattisesti.

Tämän tilannekirjauksen lisäksi tehdyt julkaisutoimet on eroteltu yllä. Vastaanotinta tai someasetuksia ei muutettu eikä uutta itsenäistä automaatiota otettu käyttöön. Vanhojen käsittelyraporttien mitätöinti, tilapäisten virheiden palautuminen ja uudet koko ketjun testit ovat yhä tuotantokäyttöönoton tarkistuskohtia.
