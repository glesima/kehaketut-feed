# Riihimäen Kehä-Ketut – verkkosivuston uudistus ja tilanne 25.10.2026

Tämä on projektin nykytilan ja toteutuneen työn pysyvä kuvaus. Yhdistyksen käytössä oleva julkinen sivusto on https://www.kehaketut.fi/ ja integraation lähdekoodi tässä repositoriossa.

## Lähtötilanne ja perusratkaisu

Etusivulla oli paljon vanhoja uutisia ja kursseja, suuri irrallinen yläbanneri sekä kömpelösti toimiva Facebook-upotus. Sivuston uudistuksessa ei vaihdettu Yhdistysavainta pois. Sen olemassa olevat jäsenrekisteri, sivurakenne ja uutisarkisto säilyvät. Uusi ulkoasu ja erilliset automaattiset tietonäkymät tuotiin Yhdistysavaimen HTML/JavaScript-sisältöosioiden kautta.

Yhdistysavain asettaa rajoitteita erityisesti koko sivupohjan muokkaukseen, HTML-osion merkkimäärään, JavaScriptin sijoitteluun ja ulkoisten upotusten toimintaan. Siksi uusi toteutus on jaettu moduuleihin ja automaatio on ulkoistettu GitHub Pages -palveluun; sivuston sisältöohje on erillinen.

## Tehdyt ulkoasumuutokset

- Seuran logo, sivuston pieni ikoni (favicon) ja yläosan taustakuva uusittu. Värit sovitettu seuran puna-valkoiseen perinteeseen; musta/hiilenharmaa tukivärinä.
- Yhdistysavaimen tarpeettoman korkeaa yläosaa madallettu ja navigaation luettavuutta parannettu.
- Etusivulle uusi tumma Kehässä tapahtuu -aloitusosio, toimiva Liity jäseneksi -painike, mobiiliin mukautuvat tulos- ja sisältöosiot sekä hillityt osioerottimet.
- Uutiset esitetään etusivulla kolmen uusimman artikkelin kortteina, ei pitkänä käsin ylläpidettävänä luettelona.
- Ottelijakortit ja nykyisten erillisten viiden ottelijaesittelysivun tilastonäkymät kytketty/valmisteltu yhteiseen tietosyötteeseen. Varsinaisia olemassa olevia esittelyjä ja videoita ei poistettu.
- Instagramin Juicer-kuvavirta ja Facebookin oma korttivirta toteutettu. Näille on myös yhteinen tasattava someosio tiedostossa embed/YHDISTYSAVAIN_some_yhtena.html; Yhdistysavaimen lopullinen yhden lohkon asennus varmistetaan sivustolla.
- Yhdistyksen Facebook-sivun logo ja kansikuva on myös uudistettu ylläpitäjän toimesta.

## Automaatiot ja lähteet

### BoxerBase

Oikea seura on **Riihimäen Kehä-Ketut ry**, tunniste **1Le8shnOwPIW**. Väärä duplikaattiseura on **RIIHIMÄEN KEHÄ-KETUT**, tunniste **mZjkT0LW248X**. Samannimisille urheilijoille saattaa olla duplikaattiprofiileja.

- GitHub Actionsissa työnkulku .github/workflows/update.yml. Ajastus neljä kertaa vuorokaudessa, cron 17 2,8,14,20 * * * UTC; GitHubin ajot voivat myöhästyä.
- Python-ohjelma scripts/update.py hakee oikean seuran julkisen urheilijaluettelon ja profiilit, enintään rajatun määrän tapahtumia sekä tunnettujen kilpailujen tuloksia.
- Järjestelmä tallentaa docs/data.json- ja docs/rss.xml-tiedostot, ja GitHub Pages näyttää tiedot docs/widget.html-näkymissä. Viimeinen erikseen tarkistettu onnistunut julkaisu: 25.10.2026; yhdeksän urheilijaa ja kahdeksan tunnistettua ottelutulosta.
- Kaikkien mahdollisten uusien kilpailujen löytymistä ei ole vielä taattu. Ilmoittautuminen on eri asia kuin vahvistettu ottelu. Pääsääntöisesti mahdollisissa virhetilanteissa käytetään viimeisintä toimivaa tietoa.
- Historiallisia lokakuun Hämeenlinnan otteluita on kirjattu väärän seuratunnisteen kautta. Skripti huomioi tämän tunnetun tapahtuman erikseen.
- Josias Joseph Ndikumanan oikea seuran profiili on rLyNGj8sCoF7. Vanhan seuran vastaavan profiilin tunniste on vfT3Q-X7B3Tf. Jos vanhasta profiilista löytyy kattavampi tilasto, sitä käytetään väliaikaisesti, mutta tietoja ei summata. Valmentajan korjauksen jälkeen vanha poikkeus voidaan poistaa.
- Muiden ottelijoiden ensisijaiset profiilit perustuvat oikean seuran tunnisteisiin, eivät samannimiseen duplikaattiseuraan.
- BoxRec-integraatio ja sen linkit poistettu pyynnöstä kokonaan. Sivustolla näkyvät tilastot kertovat BoxerBaseen kirjatuista otteluista, eivät välttämättä koko urasta.

### Uutiset

- Seuran uutiset tehdään Yhdistysavaimessa; alkuperäinen Uutiset-sivu ja arkisto säilyvät.
- scripts/update_news.py lukee julkiselta https://www.kehaketut.fi/uutiset/ -sivulta kolme uusinta julkaisua.
- GitHub Pagesin docs/news.json ja docs/news-data.js syöttävät kolme uusinta uutista omaan etusivun korttinäkymään docs/news-embed.js.
- Uutisen kirjoittaja käyttää Yhdistysavaimen uutisenlisäystä, ei etusivun HTML-osioita. Päivitys ei ole välitön vaan seuraavan ajo-/julkaisukierroksen mukainen.
- BoxerBase ei vielä automaattisesti kirjoita sanallisia uutisartikkeleita eikä julkaise niitä Yhdistysavaimeen.

### Instagram ja Facebook

- Instagram: @kehaketut on yhdistetty Juiceriin, jonka kautta verkkosivun kuvavirta päivittyy palvelun päivitysvälin mukaisesti. Julkaisua ei tarvitse kopioida manuaalisesti verkkosivuille. Instagramin kuvat eivät tule GitHubin BoxerBase-ajon kautta.
- Facebook: Metricoolin yhdistetty brändi on Riihimäen Kehä-Ketut, brändi-ID 7632678 ja Facebook-sivu-ID 160875127258478. Henkilökohtaisia tai yritystilejä ei saa käyttää.
- Facebookin oma Page Plugin -iframe ei latautunut luotettavasti. Korvaava oma korttinäkymä on docs/facebook.html, tietosyöte docs/facebook.json ja Yhdistysavaimen upotus embed/YHDISTYSAVAIN_facebook_page.html.
- Facebook-syötteelle on luotu erillinen päivittäinen ChatGPT-ajastettu päivitystehtävä; sen toistuvien ajojen onnistuminen tulee vielä varmistaa. GitHub Actions ei käytä Metricoolin suoraa maksullista HTTP-rajapintaa.
- Yhtenäistetty someosio: docs/social-embed.js ja embed/YHDISTYSAVAIN_some_yhtena.html; tällä Instagram- ja Facebook-kortit saadaan samalle korkeudelle.
- **Automaattinen julkaisujen lähettäminen** Facebookiin tai Instagramiin BoxerBase-tulosten perusteella **ei ole vielä käytössä**. Tällä hetkellä automatisoituu vain sisältöjen näyttäminen.

## ylläpito ja tietoturva

- Uutisia kirjoittava henkilö saa ohjeen kirjoittaa uutisarkistoon (Yhdistysavain → Uutiset → Lisää uutinen), mieluiten otsikon, lyhyen tekstin, ajankohdan ja kuvan kanssa.
- Älä muuta etusivun HTML-moduuleita, värejä tai automaatiokoodia ilman sovittua teknistä ylläpitoa. Muutospyynnöt sivuston ylläpitäjälle.
- Julkisessa repositoriossa ei saa säilyttää salasanoja, some-API-avaimia tai muita tunnuksia. Sivulle tuodaan vain julkiseen julkaisemiseen soveltuvaa aineistoa, ja alaikäisten kuvien käyttöoikeudet varmistetaan erikseen.
- GitHubin onnistunut työnkulku ei automaattisesti takaa täydellistä BoxerBase-datan kattavuutta. Tarkista oikea seura, profiilien yhdistäminen ja lähdetietojen ristiriidat tarvittaessa.

## Linkit

- Julkinen sivusto: https://www.kehaketut.fi/
- Seuran uutiset: https://www.kehaketut.fi/uutiset/
- Oikea BoxerBase-seura: https://boxerbase.com/o/1Le8shnOwPIW/boxers
- GitHub-projekti: https://github.com/glesima/kehaketut-feed
- GitHub Pages: https://glesima.github.io/kehaketut-feed/
- Toimintasuunnitelma: JATKOSUUNNITELMA.md
- Sisällöntuotannon ohje: HALLITUKSEN_SISALTOOHJE.md
