## BoxerBase-lähdemuutos 8.11.2026
Virallisen yhdistetyn seuran tunniste on mZjkT0LW248X. Lähdemigraation koodi vaihtaa rosterin, säilyttää vanhat viralliset ottelut ja liittää aiemmat profiilit uuteen listaan vain täsmällisesti varmennetuilla nimillä. Se ei laske vanhojen duplikaattien ottelutilastoja yhteen. Lähdehaun ja Pages-käyttöönoton tulos tarkistetaan erikseen. Katso docs/BOXERBASE_MERGE_2026-11-08.md.

# Nykytila ja tunnetut rajat

Päivitetty 2.11.2026. Tämä tiedosto on nykytilan aloituspiste. Päivätyt suunnitelmat kuvaavat myös aiempia työvaiheita, eivät automaattisesti tämänhetkistä käyttöönottoa.

## Somepalstojen korkeudet korjattu — social v4, 2.11.2026

Ylläpitäjä vahvisti Juicerin korvaavan näkymän näkyvän, mutta kuvakaappauksessa Facebook-palsta jäi Instagramia pidemmäksi ja sen alaosassa oli ylimääräistä tyhjää. V4 korjaa rakenteen, ei vain venytä Instagramia saman tyhjän tilan mittaiseksi.

- Etusivun `docs/social-embed.js` lukee nyt myös Facebookin suoraan nykyisestä `facebook.json`-syötteestä. Erillinen Facebook-iframe, sen 530 px:n oletuskorkeus ja korkeuden viestikuuntelija poistettiin vain tästä someosiosta. Vanha `facebook.html` säilyy erillisenä yhteensopivuussivuna.
- Molemmissa sama otsikko–kolmen kortin lista–alalinkki/lähdetieto-rakenne. Desktopissa palstat ja vastaavat korttirivit asettuvat yhtä korkeiksi sisällön mukaan. Mobiilissa palstat ovat allekkain ilman pakotettua yhtäläistä korkeutta. Myös Facebookissa on Katso lisää -linkki.
- Nykyiset somejulkaisut, syötteiden tiedot, kuva-assetit ja ajastettujen ylläpitotehtävien asetukset säilyvät. Ei uusia somejulkaisuja, maksuja, Juicer-riippuvuutta tai muutoksia uutisiin/BoxerBase-upotuksiin/media-vastaanottimeen.
- `node --check` sekä 24 paikallista Chromium-skenaariota läpäisty. Leveydet 1600/1200/900/768/701/700/390/320 px. Mitatut tasakorkuiset desktop-palstat ja korttirivit, sama alalinkkien taso, normaali alareunapadding, ei kasvua toistuvissa leveysmuutoksissa. Testattu myös molempien kanavien erilliset virheet, turvattomat URL:t, duplikaatit, HTML-tekstin turvallinen näyttö, rikkoutunut kuva, eri julkaisumäärät ja suurempi teksti.
- Testit käyttävät synteettisiä tietoja ja pikkukuvia. Tämä ei ole riippumaton live-Yhdistysavain-selaintesti. Ajettava testi on `qa/check_social_layout.py`, erillinen vapaaehtoinen kehitystesti (Playwright/Chromium), ei uusi tuotantoriippuvuus.
- Koodicommit `057099de4d5ec95c5f4020d0e2cd01abca13b35e`. Testatun ja GitHubista takaisin luetun JS:n Git-blob SHA sama: `737d8dcfa514cb6eb0a3f34a1097991655d18bd3`. Pages-ajon tunniste `41531038511`; ajon lopullinen tila tarkistetaan GitHubista erikseen.
- Ajantasainen rakenne ja muuttumaton tietosopimus: `docs/INSTAGRAM_NOSTOT_2026-11-02.md`.

## Instagram: Juicer korvattu omalla tiiviillä nostolla 2.11.2026

Ensimmäisessä toteutuksessa `docs/social-embed.js` v3 korvasi Juicer-syötteen kolmella pienellä Instagram-kortilla. Kortissa on kuva, julkaisupäivä, lyhyt otsikko/ote ja linkki alkuperäiseen julkaisuun. Ei Juicer-scriptiä, mainosta, automaattisesti ladattavaa videosoitinta, loputonta syötettä tai sisäistä vieritystä. V3:n Facebook-kehys korvattiin yllä kuvatussa v4:ssä suorilla korteilla; Facebookin nykyinen päivitystehtävä säilyy. Mobiilissa palstat ovat allekkain.

- Alkuperäinen koodicommit `577727772aeb01f09dd8f5a24cf0f5e587c5e4f6`. Pages-ajo `41527594857` valmistui success-tilaan; testit, kuvavälimuisti ja Deploy Pages onnistuivat.
- Ensimmäinen syöte haettiin live-Metricool-yhteydestä oikean brändin 7632678 / @kehaketut tarkistuksen jälkeen. Reels-haku palautti kolme julkaistua videota; saman aikavälin tavallisten postausten haku oli tyhjä. Ei luonnoksia tai uusia somejulkaisuja.
- `docs/instagram.json` on erillinen some-nostojen tietolähde. Vanhat `docs/data.json`-Instagram-kentät tai Juicer eivät ohjaa tätä näkymää.
- GitHub Actions tallensi kaikki kolme oikeaa JPEG-esikatselua polkuun `docs/assets/instagram/`: DfCDNnGgVUU.jpg (2721 tavua), De9SHpJCSff.jpg (40466 tavua), De9QLdAkr_o.jpg (52979 tavua). Repon jälkiluku vahvisti tiedostot. Selaimet eivät ole riippuvaisia Instagramin väliaikaisten kuvalinkkien voimassaolosta.
- Ajastettu Instagram-ylläpito on luotu ja käytössä: neljä tarkistusta päivässä, vain tämän brändin jo julkiset Reels- ja Feed-julkaisut, kirjoituskohde vain `docs/instagram.json`. Tämä on ChatGPT:n ajastettua Metricool/GitHub-ylläpitoa, ei käyttäjän Kubuntun itsenäinen somepalvelu. Ensimmäinen listan täyttö tehtiin tässä työvaiheessa; tulevan ajastetun kierroksen suorittamista ei vielä väitetä testatuksi. Uuden julkaisun näkyminen riippuu Metricoolin tiedon saatavuudesta, tarkistuskierroksesta ja Pages-julkaisusta, ei reaaliaikaisesta push-ilmoituksesta.
- Erillinen `cache_instagram_thumbnails.py` kopioi sallituilta Meta-CDN-isänniltä enintään 3 MiB JPEG-kuvat atomisesti. Vanhat onnistuneet kuvat säilyvät virheessä; selain näyttää neutraalin linkkikortin puuttuvalle kuvalle. Korttilinkit/tekstit toimivat ilman kuvaa.
- V3:ssa paikallisesti 12 uutta yksikkötestiä ja 10 Chromium-skenaariota läpäisty: 1200/768/390/320 px, ei vaakaylivuotoa, duplikaattisuoja, rikkoutuva kuva/syöte, väärä brändi, turvattoman URL:n hylkäys ja tekstin turvallinen näyttö. Testatun JS:n Git-blob SHA täsmäsi julkaistuun lähteeseen.
- V3-layout-testi käytti synteettisiä pikkukuvia ja Facebookin staattista testisisältöä. Se ei ollut riippumaton lopullisen kehaketut.fi/Yhdistysavain-näkymän live-selaintarkistus. Julkisen sivun tuore renderöity näkymä ei ollut työympäristössä saatavilla. V4 poistaa tämän palstan iframe-riippuvuuden kokonaan.
- Ohje ja ylläpitosopimus: `docs/INSTAGRAM_NOSTOT_2026-11-02.md`. Juicer-tilausta ei ostettu tai peruttu. Historiallisia tiedotteita, somejulkaisuja, Facebook-syötettä, vastaanotinta tai media-automaatiota ei muutettu.

## Etusivun ylimääräinen tiedotenosto poistettu 2.11.2026

Ylläpitäjän pyynnöstä `docs/news-loader.js`:stä poistettiin harjoitusten jatkumista koskevan erillisen etusivuilmoituksen luontifunktio ja sen kutsu. Uutisten lataus, virhetilanteen uutisarkistolinkki ja duplikaattisuoja säilyvät. Tiedotesivuja, uutisarkistoa ja Facebook-julkaisua ei poistettu tai muokattu.

- Koodimuutos: `e245788abf10ee812a58fbef62b8d45337799ce2`.
- JavaScriptin syntaksitarkistus ja kahdeksan paikallista simuloidun DOM:n testiä läpäisty. Testit eivät ole oikean selaimen näyttötesti.
- Muutos käynnisti Pages-ajon `41520292153`; myöhempi työkalutarkistus vahvisti sen success-tilan. Tämä ei yksin ole selaimen näyttötesti.
- Alun perin 6.11. päättyväksi tarkoitettu lisänosto on poistettu koodista ennen määräaikaa. Alla oleva 30.10. julkaisutieto säilyy historiatietona.

## Harjoitukset jatkuvat 30.10.2026

Seuran vahvistuksen perusteella Kamppailukeskuksen harjoitukset jatkuvat perjantaina 30.10.2026 klo 17.00 alkaen normaalin harjoitusaikataulun mukaisesti. Peruutus 27.–29.10. on päättynyt. Korjausten valmistumisesta tai sisäilman mittaustuloksista ei esitetä erillisiä väitteitä.

- Facebook-tiedote julkaistu 30.10.2026 klo 01.40 Europe/Helsinki. Metricoolin jälkitarkistus palautti PUBLISHED-tilan, alustan postitunnisteen ja julkisen osoitteen: https://facebook.com/1570416605115618/posts/1575746574582621 . Ei uusintajulkaisua.
- Julkinen tiedotesivu: `docs/tiedotteet/harjoitukset-jatkuvat-2026-10-30.html`.
- Etusivun `news-loader.js` lisäsi alun perin erillisen jatkumisilmoituksen uutisosion yläpuolelle 30.10.–5.11.2026. Nosto poistettiin yllä kuvatusti 2.11.2026. Uutisten suora Yhdistysavain-haku säilyy ennallaan. Alkuperäisen julkaisun paikallisen JavaScript-tarkistuksen yhdeksän skenaariota läpäisivät aikarajojen, duplikaattisuojan, puuttuvan kohde-elementin, DOM-valmiuden ja virhevaran testit.
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

Sivuston some-nostojen ylläpito on erotettu yllä videoiden tuotanto- ja julkaisuketjusta. Vastaanotinta tai somekanavien asetuksia ei muutettu. Vanhojen käsittelyraporttien mitätöinti, tilapäisten virheiden palautuminen ja uudet koko mediaketjun testit ovat yhä tuotantokäyttöönoton tarkistuskohtia.
