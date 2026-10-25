# Kehä-Ketut: premium-ulkoasu, kohderyhmät ja somekanavat
Toteutussuunnitelma 25.10.2026. Tämä dokumentti erottaa tehdyn kehityshaaran ja vielä toteuttamatta olevat kanavat tai hyväksynnät.

## 1. Premium-ulkoasu ja ottelutulokset
- Kehä-Kettujen puna-valkoinen identiteetti (#B91C2B, #FFFFFF), grafiitinmusta (#171A1F) ja sininen vain ottelun sinisen kulman tiedoksi.
- Responsiivinen, helppolukuinen ottelutuloskortti: punainen/sininen kulma, ottelija, vastustaja, kilpailu, päivä, julkisen tuloksen tapa, erä ja lähdelinkki.
- KO = tyrmäys, TKO = tekninen tyrmäys, RSC/RSC-I/RSC-H = keskeytys, ABD/RET = keskeytys/luovutus, WO = luovutusvoitto, DQ/DSQ = hylkäys, pistein = 5-0, 3-2 jne.
- Punainen ja sininen kulma näytetään vain lähteen varmennetussa järjestyksessä. Vanhasta datasta ei arvata; julkisesti vahvistamaton tulos jää odottamaan. Arvioitu kellonaika ei ole luotettava.
- Toteutus kehityshaarassa: scripts/update.py, docs/widget.html ja tests/test_update.py. Ensin testit ja arviointi, sitten julkaisu tuotantoon.

## 2. Seuran ryhmät
Yksi seuran tiedotusjärjestelmä. Uutinen voi kuulua usealle ryhmälle:
- Koko seura: tiedotteet ja jäsenasiat.
- Kilpanyrkkeily: kilpailut, ottelut ja kilparyhmä.
- Juniorit: nuorten ryhmät, leirit ja kilpailut.
- Kuntonyrkkeily: kurssit ja harrastajaryhmät.
- Naisten nyrkkeily: naisten treeniryhmän kuulumiset.

Luokittelu valitaan toimituksellisesti. Henkilöiden sukupuolta, kilpailuryhmää tai ikää ei päätellä kuvasta tai nimestä. Erillisten some-tilien sijaan sama seuran kanava näyttää ryhmän kohderyhmän tunnisteella. Hyväksyttyjä ryhmiä hallitaan tiedostossa config/content_groups.json.

Nykyiset Yhdistysavaimen uutiset voivat saada toimituksellisesti hyväksytyn URL-kohtaisen kohderyhmän config/news_audiences.json -tiedostosta. Tuntemattomalle uutiselle ei keksitä ryhmää. Uutiskortin näkymä päivitetään docs/news-embed.js -tiedostossa.

## 3. Sisällöntuotannon oikeudet
Sisällön toimittaja (Pepe, Erika, muut valmentajat, kuntoryhmän vetäjä, naisten ryhmän vetäjä, ulkopuolinen) saa lähettää tekstejä ja liitteitä osoitteeseen kehaketut.aineisto@gmail.com. Kukaan ei saa julkaisuvaltuutta pelkästä lähettämisestä.

Gleb, Pepe ja Erika ovat nimetyt hyväksyjät. Yksi hyväksyntä riittää. Hyväksyjä kirjautuu omalla yksilöllisellä identiteetillään ja passkeyllä; Pepe ja Erika voivat silti lukea ilmoitukset yhteisestä virallisesta seurapostista riihimaenkehaketut@gmail.com. Virallista postia ei käytetä materiaalin vastaanottoon. Sähköpostin From-kenttä ei todista hyväksyjän identiteettiä.

Julkaisun turvallisuusehto: luonnos ja versio/tiiviste, vahva tunnistautuminen, oikea tarkastajan rooli, kohderyhmä sekä kohdekanavat. Muuttunut luonnos menettää hyväksynnän. Roskaposti eristetään. Alaikäisten kuvat tarkistetaan ennen ulkoista jakelua.

scripts/editorial_workflow.py on julkisen repo-version turvallinen, ei-julkaiseva mallikerros ja testit; se estää julkaisemisen kunnes yksityinen, kirjautumisen ja oikeudet tarkistava hyväksyntäpalvelin toteutetaan. Backend ei ole vielä käytössä.

## 4. Kanavien realistinen käyttöönotto
- Jo käytössä: Kehä-Kettujen Facebook ja @kehaketut Instagram, yhtenäinen Metricool-brändi.
- Prioriteetti: olemassa olevan YouTube-kanavan omistajuus ja yhdistäminen; TikTok-tilin perustaminen tai olemassaolon selvittäminen, yhdistäminen samaan Metricool-brändiin.
- Seuraavat mahdollisuudet: Threads tai Bluesky, jos yleisöä muodostuu.
- X-vaihtoehto myöhemmin: Metricool vaatii Starterin tai korkeamman tilauksen sekä erillisen X-lisäosan, hinta lokakuussa 2026 noin 10 euroa kuukaudessa tiliä kohden. Älä osta sitä ennen päätöstä.
- Sama lyhyt 20–40 sekunnin hyväksytty videosisältö voidaan mukauttaa Reelsiin, Shortsiin ja TikTokiin. Kokonaisia otteluvideoita ei julkaista automaattisesti, valmennuksen lupa vaaditaan.

Omaa TikTok-, X- tai YouTube-tunnusta ei ole tässä toteutuksessa luotu tai yhdistetty. Hallituksen valtuuttama henkilö perustaa/valtuuttaa ne, ottaa käyttöön vahvan kirjautumisen ja säilyttää palautusoikeudet.

## 5. Prioriteetit
1. BoxerBase-tulosten ja punaisen/sinisen kulman sekä keskeytystapojen testaus ja turvallinen julkaisu.
2. Uutisten kohderyhmämerkinnät sekä viiden vanhan ottelijasivun sisältöjen korjaus.
3. Yksityinen sähköposti -> luonnos -> yksi kirjautunut hyväksyjä -> julkaisu -palvelin. Älä ohita hyväksyntää.
4. YouTube-kanavan yhdistäminen ja TikTok-kanavan perustaminen, ensimmäinen videopilotti.
5. Sivuston suorituskyvyn, mobiilin saavutettavuuden ja automaatioiden valvonta.

Lähteet:
- https://help.metricool.com/how-to-connect-tiktok-to-metricool-0ea7e
- https://help.metricool.com/x-twitter-access-in-metricool-2bt66
- https://help.metricool.com/whats-a-brand-in-metricool-and-how-does-it-work-5l78b
- https://ohjeet.yhdistysavain.fi/kotisivut/osiot/uutislista/
