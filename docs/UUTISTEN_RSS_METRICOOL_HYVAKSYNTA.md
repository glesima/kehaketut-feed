# Kehä-Ketut: uutisten RSS ja Metricoolin hyväksyttävät somepostaukset

## Tarkoitus

Yhdistysavain → Uutiset → Lisää uutinen pysyy seuran toimituksellisena julkaisutapana. GitHub Actions tarkistaa uutiset neljästi vuorokaudessa ja tuottaa erillisen RSS:n:

https://glesima.github.io/kehaketut-feed/news-rss.xml

Tämä on eri syöte kuin kilpailutulosten RSS, https://glesima.github.io/kehaketut-feed/rss.xml . Tulosten RSS:ää EI yhdistetä suoraan someautopostaukseen, koska jokaisesta kilpailu- ja ottelupäivityksestä ei tarvita erillistä uutista.

## Mikä on rakennettu

- scripts/news_rss.py muodostaa RSS 2.0 -tiedoston vain julkisesti julkaistuista kehaketut.fi/uutiset/ -artikkeleista.
- Pysyvä GUID on alkuperäinen uutisen URL, ei päivityskerran aika. Sama artikkeli ei ole uusi julkaisu neljä kertaa vuorokaudessa.
- XML sisältää otsikon, alkuperäisen linkin, julkaisuajankohdan, lyhyen tekstin sekä toimituksellisesti asetetut kohderyhmät.
- scripts/update_news.py tekee myös docs/news-rss.xml:n. Nykyinen docs/news.json pysyy kolmen uusimman uutisen etusivusyötteenä.
- Virheellinen lähde tai tyhjä tulos ei saa ylikirjoittaa viimeistä kelvollista uutis-RSS:ää. Toteutuksen pitää olla testattu ennen julkaisemista.
- Tämä ohjelma EI julkaise mitään Metricoolissa eikä luo ajastettua postausta.

## Metricoolin käyttöliittymässä tehtävä viimeinen yhdistys

Varmista oikea brändi: Riihimäen Kehä-Ketut (ID 7632678), Facebook 160875127258478, Instagram kehaketut.

1. Metricool → Planning → Autolists → New Autolist. Anna nimi RKK / seurauutiset / hyväksyntä.
2. Valitse alkuun vain Facebook. Instagramiin tarvitaan erillinen oikea, luvallinen kuva tai Reel.
3. Lisää RSS-linkiksi https://glesima.github.io/kehaketut-feed/news-rss.xml .
4. Include previous posts = POIS, ettei vuosikokousuutinen nouse uutena someen.
5. Add disabled posts = PÄÄLLE, jolloin uusi RSS-postaus odottaa hyväksyntää.
6. Repeat = POIS, ettei samaa postausta kierrätetä uudelleen.
7. Älä ota julkaisuautomaatiota käyttöön ennen kuin postausten sisältö, kohderyhmät ja kuvat on tarkistettu.

Käyttöliittymätoimintoja ei voi muuttaa tämänhetkisellä Metricoolin ChatGPT-liitännällä; yhdistäminen vaatii ylläpitäjän käyttöliittymätoiminnon. Jos oma tilaus ei tue Autolistiä, käytä erillisiä tarkistettavia Gmail- tai Metricool-luonnoksia.

Virallinen ohje: https://help.metricool.com/how-to-link-an-rss-feed-to-an-autolist-ank6m

## Milloin uutinen jaetaan someen?

Tavallista ilmoittautumista, vahvistettua otteluparia tai tulosta ei kopioida omaksi uutiseksi: kilpailukortti riittää. Poikkeuksellisen merkittävistä tapahtumista voi syntyä yksi yhteinen ennakko ja yksi jälkikooste valmennuksen ja toimituksen hyväksymänä. Erillinen uutisten duplikaatinestopolitiikka on dokumentoitu.

Uutisaiheita voi lähettää kehaketut.aineisto@gmail.com -osoitteeseen; tämä vastaanottaa aineistoa mutta EI yksin anna julkaisuvaltuutta. Sisältöposti on erillinen seuran virallisesta sähköpostista. Varsinainen vahva hyväksyntäpalvelin on vielä toteuttamatta.

## Jäljellä olevat työt

- Metricoolin Autolist-linkitys ja yhden disabled-postauksen tarkistaminen.
- Ensimmäinen kuvallinen harjoitus- tai kilpailukuuluminen Instagramissa ja Facebookissa.
- Olemassa olevan seurayoutube-kanavan osoitteen/omistuksen varmistus ja yhdistäminen; TikTok-tilin perustaminen tai vanhan tilin selvittäminen.
- Yksityinen aineisto → AI-luonnos → yksi Gleb/Pepe/Erika henkilökohtainen hyväksyntä → julkaisujonoon -backend sekä tarkastettu kuva/video.
