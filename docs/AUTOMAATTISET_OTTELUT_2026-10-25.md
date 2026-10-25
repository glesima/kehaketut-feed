# Kehä-Ketut – automaattisesti julkaistavat ottelutulokset
**Toteutussuunnitelma / 25.10.2026 · SUUNNITELTU, EI VIELÄ TOTEUTETTU**

## 1. Tavoite

Kun oikean Riihimäen Kehä-Ketut ry:n nyrkkeilijä ottelee ja **virallinen tulos on julkisesti julkaistu BoxerBasessa**, ottelu ilmestyy ilman käsityötä `kehaketut.fi`:n etusivun viimeisimpien tulosten listaan ja ottelijan omaan tilastonäkymään. Mahdolliset tuloskorjaukset päivittyvät alkuperäiseen otteluun – eivät tee duplikaattia.

Etusivun **tuloskortit** ovat automaattiset; siitä ei seuraa, että Yhdistysavaimen Uutiset-arkistoon kirjoitetaan automaattisesti erillinen uutisartikkeli tai että Facebookiin/Instagramiin julkaistaan sisältöä. Nämä ovat eri työnkulkuja.

### Nykyinen tekninen lähtötilanne

- Pääsivusto Yhdistysavaimessa, omat ulkoasut HTML/JavaScript-osioissa.
- GitHub-repo: https://github.com/glesima/kehaketut-feed
- `scripts/update.py`, `config.json`, `docs/data.json`, `docs/widget.html`, `docs/rss.xml`.
- Github Actions `.github/workflows/update.yml` hakee nykyisin 4 ×/vrk: UTC-kron `17 2,8,14,20 * * *`.
- Oikea BoxerBase-seura: https://boxerbase.com/o/1Le8shnOwPIW/boxers .
- Väärä rinnakkaismerkintä `RIIHIMÄEN KEHÄ-KETUT` on tunnisteella `mZjkT0LW248X`. Käytetään vain erikseen vahvistettuja historiapoikkeuksia, ei automaattiseen seurojen yhdistelyyn.
- Josias Joseph Ndikumanalla on tilapäinen profiilipoikkeus `rLyNGj8sCoF7` → `vfT3Q-X7B3Tf` kattavamman profiilitilaston käyttämiseksi. Tomi/BoxerBase korjaa lähteen myöhemmin.
- 25.10.2026 tarkistettu lähtöaineisto: 9 oikeaan seuraan liitettyä nyrkkeilijää ja 8 tapahtumakohtaista ottelutulosta. Historiatiedot eivät välttämättä ole täydelliset.
- Järjestelmä ei vielä löydä kaikkia tulevia tapahtumia: nykyisin tiettyjä `tracked_events`-kohteita sekä rajatun määrän etusivun tapahtumia.
- BoxRec ei kuulu integraatioon.
- Tietojen koneellisen haun sallittu rajapinta ja BoxerBasen käyttöehdot tulee varmistaa palveluntarjoajalta. `robots.txt` tarkistetaan jo nykykoodissa.

## 2. Milloin tulos on julkaistava?

BoxerBasessa on toisistaan riippumattomat tapahtuman julkaisu, osallistujien näkyvyys, ottelulistan julkaisu ja tulosten julkaisu. Ks. https://vlaamse.boxerbase.com/docs/event/visibility-and-publishing

**Tilakone, ehdotettu normalisoitu kenttä `status`:**

1. `registration` – ottelija ilmoitettu, ei ottelupäätelmää eikä julkista etusivun tulosmerkintää.
2. `scheduled` – ottelupari julkisesti vahvistettu ja ottelulista julkaistu; näytetään Vahvistetut tulevat ottelut -kortissa, jos ajankohta tiedossa.
3. `completed_unpublished` – tapahtuma/otteluaika mennyt, mutta vahvistettua virallista tulosta ei ole julkisesti saatavilla; **EI** julkaista voittona tai tappiona.
4. `result_published` – lähdesivulla on julkaistu riittävän yksiselitteisesti voittaja, ottelumuoto ja tulos; etusivun viimeisimmät tulokset sekä urheilijaprofiili päivittyvät.
5. `cancelled` / `no_contest` / `unknown` – erillinen merkintä; ei luokitella tappioksi eikä voitoksi ilman varmistettua päätöstä.

Ottelun **toteutuminen** ja sen **virallisen tuloksen julkaisu** ovat eri asioita. Sivusto ei arvaa voittajaa pelkästä päivämäärästä, eikä ilmoittautuminen tarkoita vahvistettua ottelua.

## 3. Automaattinen kilpailujen löytyminen – tärkein puuttuva palanen

Toteuta `discover_events` -vaihe, joka ei edellytä käsin lisättävää `tracked_events`-listausta:

- Ensisijaisesti kysy BoxerBaselta luvallinen API-, webhook- tai muu koneluettava tapahtuma-, osallistuja- ja tulosrajapinta.
- Muussa tapauksessa käytä vain palveluntarjoajan sallimia julkisia sivuja: Suomen julkista tapahtumakalenteria ja sen sivutusta, oikeaa seuran ID:tä sekä vahvistettuja yksittäisten ottelijoiden BoxerBase-profiileja.
- Aikahaarukka suunnitteluvaiheessa: tulevat 90 vrk, menneet 60 vrk ja erikseen pitkän historian korjaus. Toteutus saa säätää lukumääriä ja tehdä inkrementaalista hakua.
- Älä rajoitu etusivun ensimmäiseen kahdeksaan tapahtumaan. Käytä sivutusta, event-ID:tä ja paikallista tapahtumarekisteriä.
- Havaintokohteen löytäminen perustuu seuraprofiilin ja nyrkkeilijän **tunnisteisiin**, ei yksin etu- ja sukunimen tekstitäsmäytykseen.
- Mikäli osallistujat eivät vielä näy julkisesti, jätä tapahtuma tilaan `event_known` ja tarkista myöhemmin. Älä merkitse ketään osallistujaksi arvauksesta.
- Rajaa kierrosten sivupyynnöt, noudata palvelun ehtoja, robots.txt:tä, sallittua päivitystiheyttä sekä aikakatkaisuja. Vältä kaikkien tapahtumien ja urheilijoiden täyttä läpikäyntiä joka ajolla.
- Tallenna `events.json`-rekisteriin löydetyt tapahtumat, `event_id`, lähde, tapahtumapäivä, viimeinen onnistunut tarkistus ja julkisen näkyvyyden tila.

**Hyväksyntätesti:** uusi julkaistu kilpailu, jota ei ole käsin lisätty `config.json`:iin, löytyy ja siirtyy seurantaan.

## 4. Ottelun identiteetti, tuplien poisto ja lähdetarkistus

- Uuden tulostietueen ensisijainen avain `(event_id, bout_id)`. Jos BoxerBase käyttää lokalisoituja verkkotunnuksia, normalisoi ne samaan tunnisteeseen.
- Jos ottelun ID ei ole saatavilla, varmennettu varatunniste voi käyttää `event_date`, `event_id`, ottelijaprofiilien tunnisteita ja ottelun numeroa; epävarma yhdistelmä jää tarkistettavaksi, ei automaattiseen tuplien poistoon.
- Sama ottelu säilyy yhtenä tietueena myös silloin, kun tulos julkaistaan jälkikäteen tai pisteet korjataan.
- Säilytä lähde-URL, `last_checked`, `first_seen`, `result_published_at` kun saatavilla, alkuperäisen päätöksen ja viimeisimmän päätöksen muutoshistoria. Näytä julkisesti vain tarpeelliset tiedot.
- Urheilija yhdistetään ensisijaisesti oikeaan `boxer_id`:hen; historialliset duplikaatit vain erikseen vahvistetulla alias-listalla. Ei automaattista seurojen yhdistelyä nimen perusteella.
- Kielletyt tilanteet: sama ottelu kahteen kertaan, vanha tulos katoaa väliaikaisen lähdevirheen vuoksi, tuntematon voitto/tappio arvataan tai lähteen korjaus luo uuden ottelun.

## 5. Päivitysrytmi ja julkaisuviive

**Nykyinen**: BoxerBase, nyrkkeilijäprofiilit ja uutiset tarkistetaan neljä kertaa päivässä.

**Tavoitetoteutus**:

- Säilytä 4 ×/vrk perustarkistus nyrkkeilijöille, historiatiedoille, uutisille.
- Kun lähestyvästä kilpailusta on saatu luotettava tapahtumahavainto, käynnistä tapahtumakohtainen aktiiviseuranta kilpailupäivänä ja esimerkiksi 24–48 h sen jälkeen (tarkka ikkuna sovitaan toteutuksessa).
- Aktiiviseurannan suunniteltu tiheys 20–30 min **vain, jos sallittu BoxerBase-yhteys ja lähteen kuormitus sen mahdollistavat**; vaihtoehtona webhook/push on parempi.
- GitHub Actionsin ajastettu ajo ei ole sekunnintarkka: run voi jonoutua; sivulla näkyy uusi tulos vasta, kun BoxerBase on julkaissut sen, haku on onnistunut ja GitHub Pages on valmistunut.
- Hyväksymistavoite: monitoroidun tapahtuman uusi julkaistu virallinen tulos näkyy sivulla normaalitilanteessa noin 60 minuutin sisällä *lähteen julkaisemisesta*, ei ottelun fyysisestä loppumisesta. Tämä ei ole taattu SLA.
- Napsautettava `Tarkista nyt`-/manual `workflow_dispatch`-reitti ylläpitäjälle on varakeino.
- Koodissa ehkä erilliset `baseline_update` ja `event_watch`-ajot, mutta molemmat serialisoidaan samaan deployment-concurrency-ryhmään. Vältä aikaisempien git-push-kilpailutilanteiden uusiutumista.
- Github Actions cron -minimi on viisi minuuttia; tätä nopeampaa sykliä ei tarvita. Ks. https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

## 6. Etusivun ja ottelijasivujen toiminta

Yhdistysavain HTML-lohkoon **ei lisätä uusia manuaalisia otteluita**. Käytetään nykyistä GitHub Pages -näkymää (`docs/widget.html?view=updates`).

Etusivu:
- Otsikko **Kehä-Ketut kehässä**.
- Viimeisimmistä vahvistetuista tuloksista enintään neljä nostoa, aikajärjestys uusimmasta.
- Rivillä: ottelija, vastustaja, kilpailu, päivämäärä, tulos (voitto/tappio ja tuomariäänet tai lopetustapa) ja linkki lähteeseen.
- Tulevat kilpailut / vahvistetut otteluparit omassa kompaktissa osiossa, ei tyhjänä pitkänä korttina.
- Jos lähteessä ei ole uusia tuloksia, näytä viimeisimmät vahvistetut ja todellinen lähteen tarkistusaika; älä näytä tyhjää etusivua.
- Mahdollinen oma `Katso kaikki tulokset` -linkki erilliseen historia- tai kilpailusivuun, jolla voi selata pidempää listaa.

Ottelijoiden omat esittelysivut:
- Sama `boxer_id` ja sama päivittyvä lähde, mahdolliset viimeisimmät ottelut sekä ottelu-/voitto-/tappiotilastot.
- Erota `BoxerBaseen kirjattu` tilasto koko uran historiallisesta arviosta. Älä esitä puutteellista lukua koko uran varmana kokonaismääränä.
- Poista tai merkitse päivätyiksi nykyisissä esittelyteksteissä olevat käsin kirjoitetut vanhat ottelumäärät, jotta sivulla ei ole ristiriitaisia lukuja.
- Josias-rinnakkaisprofiilin tilapäinen sääntö poistaa itsensä käytöstä, kun virallinen profiili on ainakin yhtä kattava; poista sääntö kokonaan valmentajan korjauksen jälkeen.

## 7. Häiriönsieto ja valvonta

- Jos haun HTTP-vastaus, HTML-rakenne tai tulos jää epäselväksi, pidä viimeisin onnistunut aineisto näkyvissä; älä muuta tulosta virheellisen parsinnan perusteella.
- Talleta `last_successful_boxerbase_update`, `last_results_update`, `last_news_update` ja tarvittaessa `active_event_check` erilleen. Älä väitä kaikkien tietojen juuri päivittyneen, jos vain yksi osa onnistui.
- Toteuta pienet testit: uusi tapahtuma ilman käsin lisäystä; osallistuminen ilman vahvistettua ottelua; vahvistettu ottelu ilman tulosta; virallinen voitto/tappio; myöhempi tuloskorjaus; duplikaattiseura; nimen samankaltaisuus; lähtöpalvelun katko; RSS- ja sivukorttien julkaisu.
- Warn vain merkittävistä ongelmista: kolme peräkkäistä lähdevirhettä tai aktiivisen kilpailun julkaisu epäonnistuu; ei turhia ilmoituksia normaalista tyhjästä hakukierroksesta.
- Älä rakenna salaista tokenia julkiseen HTML:ään tai GitHub-repositorioon. Alaikäisten tietosuoja ja kuvaoikeudet huomioitava.

## 8. Toteutusjärjestys (tekninen työnkulku)

### Vaihe A – datan oikeellisuus
1. BoxerBase-lähteen luvallinen rajapinta/hakutapa ja virallisen tuloksen tunnistus.
2. Oikea seura, mahdolliset tunnetut duplikaatit ja ottelu-ID-pohjainen deduplikointi.
3. Varmennus historiallisella 2026-09-27, 2026-10-10 ja 2026-10-24 aineistolla: ei häviä eikä kahdennu.

### Vaihe B – uusien tapahtumien automaattinen löytyminen
4. Lisää tapahtumarekisteri ja rajattu inkrementaalinen julkisten tapahtumien haku.
5. Yhdistä tapahtumat nyrkkeilijöiden tunnisteisiin ja niiden julkisiin ottelulistoihin; erottele `registration`, `scheduled` ja `result_published`.
6. Kytke vain virallinen tulos automaattisiin tuloskortteihin.

### Vaihe C – kilpailupäivien seuranta
7. Lisää aktiiviseuranta vain löydetyille ja relevanteille kilpailuille.
8. Turvallinen GitHub Actions deployment ja kahden päällekkäisen ajon lukitus / päivitysristiriitojen hallinta.
9. Viiveen, lähteen ja viimeisimmän onnistuneen tarkistuksen seuranta.

### Vaihe D – etusivun viimeistely
10. Kevyt tuloslista, tuloskorjausten käsittely, kilpailuarkisto sekä lähdeajat.
11. Ottelijoiden profiilikorttien ja nykyisten manuaalisten esittelytekstien yhdenmukaistaminen.
12. Mobiili, saavutettavuus, no-JS-/kolmannen osapuolen estojen varanäkymät ja HTML-lohkojen marginaalit.

### Vaihe E – hyväksyttävät somejulkaisuluonnokset
13. Kun **uusi vahvistettu virallinen tulos** on ilmestynyt, muodosta yksi ottelutapahtumakohtainen luonnos (useita seuran ottelijoita yhdessä).
14. Luonteva, asiallinen viestintä ilman liiallista hehkutusta; myös tappiot asianmukaisesti.
15. Luonnos etenee oikeaan Metricoolin **Kehä-Ketut-brändiin** vasta käyttäjän/hallituksen hyväksyttäväksi. Älä julkaise automaattisesti ennen erillistä päätöstä.
16. Yhdistysavaimen omia uutisartikkeleita kirjoitetaan edelleen Uutiset → Lisää uutinen; tuleva erillinen työnkulku voi tarjota hyväksyttävän uutisluonnoksen, mutta ei väitetä suoraa Yhdistysavain-rajapintaa.

## 9. Hyväksymisehdot ennen käyttöönottoa

- Uusi julkinen kilpailu löytyy ilman, että `config.json` sisältää sen URL:n.
- Vahvistettu ottelu EI näy tuloksena ennen kuin tulos on julkinen ja varmistettu.
- Julkaistusta tuloksesta syntyy etusivun kortti ja urheilijan omaan profiiliin ottelumerkintä ilman Yhdistysavaimen muokkausta.
- Sama ottelu näkyy vain kerran ja myöhemmin korjattu tuomaripäätös päivittää samaa ottelua.
- Oikea seuraprofiili on edelleen `1Le8shnOwPIW`, Josias-rinnakkaiskäsittely on rajattu eikä BoxReciä käytetä.
- Vanha data säilyy lähdekatkon yli ja käyttöliittymän päivityspäivä vastaa oikeasti tietolähteen onnistunutta hakua.
- Ei vahingossa julkaista mitään henkilökohtaiselle tai yrityksen Facebook-/Instagram-tilille.
- Ei tarvetta kirjoittaa etusivun HTML-koodia uudelleen jokaisen kilpailun jälkeen.

## 10. Vastuut, riippuvuudet ja rajat

- **Tomi / valmennus / tarvittaessa BoxerBase-tuki:** duplikaattiseuran ja ottelijoiden yhdistäminen ja puuttuvien ottelujen palauttaminen. Älä poista vanhoja tietueita ennen tiedonsiirron varmistamista.
- **Pepe ja hallitus:** uutiset Yhdistysavaimen `Uutiset → Lisää uutinen` -toiminnosta. Etusivun HTML-järjestelmä jätetään teknisen ylläpidon vastuulle.
- **Tekninen ylläpito:** ajastukset, lähdemuotojen seuranta, tietoturva, virhetilanteet ja tuleva hyväksyttävien somejulkaisuluonnosten työnkulku.
- **Ylläpitäjän erillinen päätös:** julkaistaanko automaattisia sanallisia somejulkaisuja koskaan ilman ihmisen tarkistusta. Oletuksena ei.

**Tämä tiedosto on toteutusmäärittely, ei väite siitä, että kaikki luetellut vaiheet on toteutettu.**
