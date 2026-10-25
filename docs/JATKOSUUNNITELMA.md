# Kehä-Ketut – tehtäväjärjestys ja toteutussuunnitelma (päivitetty 25.10.2026)

## Nykyinen toimiva lähtötilanne

- Uusittu Yhdistysavaimen etusivu ja seuran värit, logo, kuvatausta, liittymispainike.
- GitHub Actions / Pages päivitys neljästi vuorokaudessa: rajatut BoxerBase-tulokset ja tilastot sekä kolme uusinta Yhdistysavaimen uutista.
- Instagram @kehaketut → Juicer-kuvavirta; Facebookin korttivirta → Kehä-Kettujen Metricool-brändi + erillinen ajastettu päivitys. Ei automaattista somessa julkaisemista.
- Oikea BoxerBase-seura `1Le8shnOwPIW`; historiassa on duplikaatteja, joita ei saa summata tai poistaa ennen yhdistämistä.

## P0 – ensimmäinen seuraava toteutus (automaattisesti päivittyvät uudet ottelut)

Katso tekninen määrittely: [AUTOMAATTISET_OTTELUT_2026-10-25.md](AUTOMAATTISET_OTTELUT_2026-10-25.md)

1. Julkisten BoxerBase-tapahtumien automaattinen haku ja sivutus, ei vain `tracked_events` ja kalenterin ensimmäiset tapahtumat.
2. Tapahtuman/ottelijan tunnistepohjainen yhdistäminen ja tuloksen virallisen julkaisustatuksen varmistaminen; ilmoittautuminen ≠ vahvistettu ottelu ≠ julkaistu tulos.
3. Tulosten `event_id + bout_id` -deduplikointi, korjaushistoria ja säilyminen lähdekatkoissa.
4. Kilpailupäivän tiheämpi tarkistus vain relevanteissa seuratuissa tapahtumissa, mikäli BoxerBasen ehdot sallivat. GitHub Pagesin automaattinen julkaisu. Tavoite noin 1 h lähteen julkaisemisesta, ei taattua reaaliaikaa.
5. Tulokset etusivulla ja urheilijan omalla sivulla ilman HTML-muokkausta. Kaksi historiallista tapahtumaa ja yksi uusi tapahtuma hyväksymistestiksi.

## P0 – lähdedatan puhdistus

- Tomi ja tarvittaessa BoxerBase-tuki yhdistävät duplikaattiseuran ja urheilijaprofiilit (säilytä historiat ennen poistoa), täydentävät puuttuvat ottelut.
- Kun oikean seuran Josias-tilastot ovat kattavat, poista tilapäinen rinnakkaisprofiilin poikkeus.
- BoxRec ei kuulu suunnitelmaan eikä sivuille.

## P1 – sivujen laatu ja luotettavuus

- Seuran viidellä nykyisellä ottelijasivulla vanhojen käsin kirjoitettujen ottelumäärien ristiriidat pois; historia ja päivämäärät säilyvät.
- Tarkista yhdistetyn Instagram/Facebook-osion mobiilitasaukset, kuvien lataus ja oikeiden tilien identiteetti; jatketaan vain yhtä someosiota.
- Poista vanhat piilotettujen HTML-uutislistojen päällekkäisyydet; `Uutiset → Lisää uutinen` → kolme uusinta korttia.
- Tuloslistan "tulevat" -osio tiiviinä, ei turhan suurta tyhjää korttia; selkeä lähteen tarkistusaika ja lähdekatkon varatieto.
- Terveyden seuranta (esim. viimeisin onnistunut kilpailuhaku, uutishaku, FB/IG-syötteen tila), merkittävät häiriöilmoitukset.
- Mobiili, saavutettavuus, oikeus alaikäisten kuviin, varakuvaukset ja toimivat linkit.

## P1 – sisällöntuotannon keskittäminen ja videoiden julkaisupilotti

Täydellinen suunnitelma: [SISALTOTUOTANTO_VIDEO_JA_UUTISAUTOMAATIO_2026-10-25.md](SISALTOTUOTANTO_VIDEO_JA_UUTISAUTOMAATIO_2026-10-25.md)

- Hallitus voi toimittaa uutisaiheet, kuvat ja linkit seuran yhteiseen sisältöpostiin; pitkät videot yksityisen Dropboxin vastaanottolinkin kautta. Automaattiset julkaisutoimet edellyttävät erillistä vahvistusta ja hyväksyntää.
- Sähköposti -> AI-uutisluonnos -> Pepe/yhdistyksen ylläpitäjä tarkistaa -> julkaisu nykyisessä Yhdistysavaimen Uutiset-arkistossa. Suoraa natiivia sähköpostijulkaisurajapintaa ei ole vahvistettu.
- Yhdistysavaimen RSS -> Metricoolin Autolist, jossa uudet julkaisut tulevat aluksi disabled/hyväksyttävään tilaan. Suora somepostaus vasta hyväksytyistä tiedoista.
- Kaksi kilpailuvideota -> lyhyt kohokohtakooste 20–40 sek -> valmentajan hyväksyntä -> yksi Instagram Reel, Facebook-video ja YouTube Short. Täysi otteluvideo pysyy yksityisessä valmennusarkistossa.
- YouTube-kanava yhdistetään seuran oikeaan Metricool-brändiin; tällä hetkellä siellä vain Facebook ja @kehaketut Instagram.
- Harjoituskuvista automaattiset brändin mukaiset kuvat ja luonnolliset suomenkieliset tekstit, julkaisu ja kotisivun Juicer-kuvavirta ilman etusivun manuaalista editointia.

## P2 – julkaisuautomaation jatko

- Uusi julkaistu ottelutulos → luonnos kilpailun yhteisestä somekoosteesta; hyväksyntä ennen Metricoolin FB/IG-jakelua.
- Myöhemmin mahdollisuus tehdä ehdotettu Yhdistysavain-uutisluonnos, mutta **ei** esitetä automaattisesti kirjoittavana uutisintegraationa ennen toimivaa teknistä polkua.
- Uutisten ja harjoituskuvien luonteva laatu; Yhdistysavaimen uutiset tehdään edelleen toimituksellisesti yhdestä paikasta.

## P3 – ylläpito ja pitkän ajan kehitys

- Sivuston dokumentaatio, hallitukselle uutisohje, GitHub-koodin siistiminen ja vähäiset HTML-lohkot.
- Tietosyötteen historianäkymä, kilpailukohtaiset sivut ja parannettu urheilijaprofiili.
- BoxRec-integraatiota ei tehdä; lähdelukujen puutteet kerrotaan rehellisesti.
- Ei Yhdistysavaimesta poismuuttoa tässä vaiheessa.

## Toteutusperiaate

**Yhdistysavain = jäsenet + toimitukselliset uutiset.**
**GitHub Actions = julkiset kilpailu-/ottelutiedot ja uutisnostojen päivitys.**
**GitHub Pages = etusivun HTML/JSON-komponentit.**
**Juicer = Instagram-kuvavirta.**
**Metricool/FB-syöte = Facebook-sisällön verkkosivunosto; varsinaiset somejulkaisut vasta hyväksyttyinä.**

Ei jatkuvaa käsinkopiointia eikä uusia HTML-muutoksia jokaisen ottelun jälkeen.

## Seuraavan teknisen työskentelykerran aloitus

Avaa ensin [otteluautomaation määrittely](AUTOMAATTISET_OTTELUT_2026-10-25.md) ja `scripts/update.py`. Aloita _event discovery_ -kerroksesta sekä tuloksen `result_published`-tilan validoimisesta, älä uusista ulkoasuhionnista. Tee työ erillisellä haaralla, mutta testaa hyväksytty toteutus julkaisuun ennen kuin siivoat nykyistä tuotantopolun koodia.
