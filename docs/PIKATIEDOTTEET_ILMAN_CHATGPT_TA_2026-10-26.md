# RKK – pikaviestintä ilman ChatGPT-keskustelua

**26.10.2026 | työnkulku seuran mediavastaavalle.**

## Yksi julkaisupaikka

**Yhdistysavain → Uutiset → Lisää uutinen → Julkaise** on ensisijainen, seuran ylläpitäjän itse tekemä sisällöllinen julkaisupäätös.

Kotisivujen etusivulle julkaistut uutiset päivittyvät välittömästi uudella sivulatauksella, kun Yhdistysavaimessa on käytössä ajantasainen ulkoinen `news-embed.js`. Se hakee saman domainin julkista `/uutiset/`-listaa suoraan, ei odota GitHubin 4 kertaa päivässä käynnistyvää RSS-hakua.

### Yksi kertaluonteinen Yhdistysavain-asetus – estä vanhan scriptin juuttuminen välimuistiin

**Älä lisää uutta uutisosiota tai toista `rkk-news-slot`-elementtiä.**

Etsi etusivun nykyisestä uutisupotuksen HTML-lohkosta aiempi script-rivi, jossa ladataan

    https://glesima.github.io/kehaketut-feed/news-embed.js

ja vaihda *vain ulkoisen scriptin lähde* muotoon

    https://glesima.github.io/kehaketut-feed/news-loader.js?v=1

Säilytä vanhan HTML-lohkon muu sisältö, erityisesti `<div id="rkk-news-slot"></div>`. Yksi esimerkkirivi, jos vanha script-rivi oli tässä muodossa:

    <script src="https://glesima.github.io/kehaketut-feed/news-loader.js?v=1" defer></script>

Loader lataa jatkossa varsinaisen `news-embed.js`-tiedoston minuutin välein vaihtuvalla versiotunnuksella. Uutisen **sisältö** haetaan joka sivulatauksella suoraan Yhdistysavaimen julkaistusta listasta välimuistin ohittavalla fetch-pyynnöllä. Jos suora haku epäonnistuu, haetaan viimeisin RSS-päivityksen yhteydessä muodostettu uutisdata GitHub Pagesin varasyötteestä myös välimuistivapaalla osoitteella. Tämä vähentää vanhan otsikon/päivämäärän riskiä, mutta oikea sivuston näkyvyys pitää testata selaimessa.

**Jos etusivulla on jo toinen news-data.js -script-rivi**, se ei ole välttämätön uuden loaderin rinnalla. Poista vain tuo ylimääräinen uutisdataviittaus, jos se osoittautuu päällekkäiseksi; älä muokkaa muita BoxerBase-/someupotuksia.

**Tärkeää:** yhteyden/palveluntarjoajan viive on mahdollinen, joten aivan reaaliaikaista jakelua sekunnissa ei voi taata. Loaderin sisältö tulee normaalisti näkyviin viimeistään uusimalla etusivu, ilman tavallista kovaa välimuistin tyhjennystä.

## Kiireellinen ilmoitus NYT – toimiva menettely jo tänään

1. Julkaise Yhdistysavain-uutinen. Otsikko kertoo mitä perutaan, missä ja milloin. Sisältö kertoo syyn vahvistetuin tiedoin, jatkon ja mistä seuraa päivitys.
2. Tarkista etusivu tavallisessa selainikkunassa uudella latauksella ja että otsikko ei katkea. Kerran vaihdettu `news-loader.js` poistaa tarpeen konsultoida ChatGPT:tä välimuistin vuoksi.
3. Kun haluat kiireellisen viestin varmasti Facebookiin **nyt**, mene Metricool → Planner → Luo julkaisu → Facebook POST → `Auto publish=ON` → julkaisu mahdollisimman pian. Älä odota nykyistä `RKK | Seurauutiset | Facebook` -autolistan ti/to klo 18 aikataulua; siinä `Add disabled posts` on päällä ja uusi artikkeli ei mene suoraan julkiseksi.
4. Korjaus tai jatkotiedote: päivitä alkuperäistä artikkelia ja tee uusi selkeä julkaisupäätös vasta, kun tilanne muuttuu. Väätä arvaamasta salin uudelleenavautumista.

Näin toimii **kahden käyttöliittymän varma malli** jo nyt, ilman ChatGPT-käsityötä. Facebook-kirjoitusta ei voi taata automaattiseksi ennen erillisen integraation rakentamista.

## Tavoite: yksi julkaisu Yhdistysavaimessa -> etusivu + Facebook

Rakenna erillinen, hallittu **PIKATIEDOTE**-työnkulku, joka ei julkaise seuran jokaista normaalia uutista Facebookissa.

- Ainoastaan toimituksessa julkaistun uutisen **otsikko, joka alkaa `TIEDOTE:`**, toimii näkyvänä julkaisumerkintänä. Pelkkä sana 'harjoitukset' muualla ei laukaise automaattista somepostausta.
- Ensisijainen nopea syöte: Yhdistysavaimen **oma uutislistan RSS**, jos seuran julkaistu Uutislista tarjoaa RSS:n ja se on hallinnasta aktivoitu. Käytä järjestelmästä saatua tarkkaa URL:ia; älä keksi RSS-osoitetta. Aikataulutettu GitHubin `news-rss.xml` ei toimi kiireellisen ilmoituksen nopeana lähteenä, koska se noudetaan vain 4 kertaa päivässä.
- Make.com-skenaario: RSS Watch items -> tarkista domain, uutisen julkaistuus, `TIEDOTE:`-prefiksi, GUID/URL-deduplikointi -> Metricoolin virallinen MCP OAuth (`https://ai.metricool.com/mcp`) -> Facebook `POST`, `autoPublish=true`. Käytä yhden kanavan ja yhden julkaisun tapahtumalokia, ettei samaa uutista lähetetä kahdesti.
- Tarvitaan myös lyhyt siirtoviive tai koeaikataulu, koska kaikki Make-tilaukset eivät seuraa joka minuutti. Lisäksi tarkista varsinainen Facebookin publicUrl eikä pelkkä 'SENT'.
- Tavalliset seurauutiset jäävät nykyiseen tarkistettavaan RSS-autolistaan. Yksityiset henkilötiedot, alaikäisten valokuvat tai arkaluontoiset asiat eivät lähde pikajulkaisun kautta ilman asiaankuuluvaa julkaisupäätöstä.
- **Make+RSS+Metricool-MCP -siltaa EI ole vielä asennettu tai testattu.** Sen ohjelmointi ja RKK-tiliin yhdistäminen on seuraava selkeä työvaihe. Täyden automaation laatu ja kustannukset tarkistettava oikealla testitiedotteella.

## Käytännön esimerkki

Otsikko: `TIEDOTE: Kamppailukeskuksen harjoitukset peruttu 27.–29.10.`

Sisältö: `Kaupungin päätöksellä Kamppailukeskuksen harjoitusvuorot on peruttu korjaustöihin liittyvän sisäilmaongelman vuoksi. Tilanne arvioidaan uudelleen 29.10. Ilmoitamme jatkosta vahvistettujen tietojen perusteella.`

Mediavastaava julkaisee tämän yhden kerran Yhdistysavaimessa. Kotisivun ajankohtaisnäkymä päivittää sen. Kun tuleva `TIEDOTE:`-autopostaus on kytketty ja testattu, Make hoitaa myös Facebook-tiedotteen automaattisesti. Ennen sitä Facebook vaatii yhden lisätoimen Metricoolissa.

## Lähteet

- https://ohjeet.yhdistysavain.fi/kotisivut/osiot/uutislista/
- https://help.metricool.com/how-to-link-an-rss-feed-to-an-autolist-ank6m
- https://help.metricool.com/how-to-connect-metricools-mcp-eqp9h
- https://github.com/glesima/kehaketut-feed/blob/main/docs/UUTISTEN_RSS_METRICOOL_HYVAKSYNTA.md
