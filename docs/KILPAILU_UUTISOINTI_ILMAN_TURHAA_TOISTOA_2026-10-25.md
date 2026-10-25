# Kehä-Ketut – kilpailu-uutisoinnin automaation päätössäännöt (25.10.2026)

## Päätös: kilpailukortit ovat ensisijainen tiedotuskanava

Tärkein käytännön periaate on, että **jokaisesta BoxerBase-havainnosta ei synny uutista**. Verkkosivun oma kilpailukortti näyttää automaattisesti:

- julkiselta osallistujalistalta havaitut ilmoittautumiset (eivät takaa ottelua);
- vahvistetut otteluparit, silloin kun järjestäjä julkaisee ne;
- virallisesti vahvistetut ottelutulokset.

Päivitys näissä korteissa EI tee uutta Yhdistysavain-uutista, sähköpostia eikä Facebook-/Instagram-julkaisua. Sama tapahtuma voi muuttua monta kertaa ennen ottelupäivää ilman turhia viestejä.

## Milloin erillinen uutinen kannattaa tehdä?

| Tapahtuma | Etusivun kilpailukortti | Uutisluonnos | Julkaisu |
| --- | --- | --- | --- |
| Tavalliseen kilpailuun ilmoittautuminen | Kyllä, jos havainto julkinen | Ei oletusarvoisesti | Ei |
| Yksittäinen vahvistettu ottelupari | Kyllä | Ei oletusarvoisesti | Ei |
| Yksittäinen voitto tai tappio | Kyllä | Ei automaattista yksittäisuutista | Ei |
| Merkittävä kilpailu, esim. Nuorten SM | Kyllä | Yksi yhteinen ennakko mahdollinen | Vain valmennuksen tietojen vahvistus + hyväksyjä |
| Merkittävän kilpailun valmistuneet tulokset | Kyllä | Yksi kilpailun yhteinen tuloskooste mahdollinen | Vain tulosten kattavuuden tarkistus + hyväksyjä |
| Poikkeuksellinen seuran saavutus / mitali / debyytti | Kyllä, jos tulos julkinen | Toimituksellinen ehdotus, ei automaattinen hehkutus | Vain hyväksyntä |
| Ilmoittautuminen ei johtanut otteluun | Ilmoittautumisen historia saa näkyä | Ei normaalisti uutista | Ei |

**Katto merkittävälle kilpailulle:** korkeintaan yksi hyväksytty ennakko ja yksi hyväksytty jälkikooste. Useimmille tavallisille kilpailuille ei erillistä uutista lainkaan. Erillisiä poikkeuksia saa tehdä vain toimituksellisella päätöksellä.

## Ilon ja Kosmon ilmoittautumiset Nuorten SM -kilpailuihin

BoxerBase-tietosyöte sisältää kahden urheilijan, Ilo ja Kosmo Grönroosin, aiemmin julkisesti havaittua ilmoittautumista Nuorten SM -kilpailuihin 6.11.2026 alkavaan tapahtumaan, BoxerBase event ID `zdyYMbmXqIuV`.

- **Kilpailukortissa:** tieto riittää sellaisenaan, kun se on selitetty oikein; näyttö ei tarkoita vahvistettua otteluparia.
- **Erillinen ennakkouutinen:** mahdollinen, koska SM-tason kilpailu ja kaksi seuran ilmoittautunutta ovat seurauutiseksi kiinnostavia.
- **Ennen uutisen hyväksyntää:** valmentaja vahvistaa, että osallistuminen / lähtö on ajantasainen. Jos vain aiemmin havaittu ilmoittautuminen tunnetaan, ehdotus jää tarkistettavaksi.
- **Uutisen otsikko:** esimerkiksi "Kehä-Kettujen nyrkkeilijöitä ilmoittautunut Nuorten SM-kilpailuihin". Ei "kaksi ottelijaa kehässä" tai "varmat ottelut" ennen otteluparien vahvistamista.
- **Kilpailun jälkeen:** yksi jälkikooste vasta, kun tapahtuman ottelut ovat päättyneet, tulokset on tarkistettu kattaviksi ja toimituksellinen hyväksyjä antaa luvan.
- **Jos kukaan ei lopulta saa ottelua:** siitä ei normaalisti tarvita uutta uutista. Automaattinen kilpailukortti voi selittää tilanteen, jos se on luotettavasti vahvistettu.

## Tärkeimmät päällekkäisyyden estot

1. Jokaisella kilpailulla pysyvä `event_id`.
2. Kullakin kilpailulla enintään yksi uutisehdotus avaimella `event_id:preview` ja yksi avaimella `event_id:recap`. Uudelleen havaittu ilmoittautuminen tai tulos ei käynnistä uutta ehdotusta.
3. Uutisten yhteinen tapahtumakohtainen tapahtumarekisteri säilyttää tilat `proposed`, `needs_coach_confirmation`, `awaiting_editorial_approval`, `approved`, `published`, `rejected`.
4. Yhdistysavaimeen jo julkaistut kilpailu-uutiset pitää kirjata rekisteriin. Esimerkiksi lokakuun 2026 yksi artikkeli "Kehä-Ketut kilpailivat lokakuussa Tampereella ja Hämeenlinnassa" kattaa kaksi eri tapahtuma-ID:tä; niitä EI ehdoteta uusiksi jälkikoosteiksi.
5. Jos osallistujat tai tulokset muuttuvat ennen hyväksyntää, päivitä olemassa oleva ehdotus; älä luo toista. Hyväksynnän jälkeen muuttunut sisältö vaatii uuden hyväksynnän.
6. Yksi hyväksytty seurauutinen voi synnyttää eri kanaville muotoillut Instagram/Facebook-julkaisuluonnokset. Sama ottelu ei samalla aiheuta toista riippumatonta somepostausta.
7. Ei ylimääräisiä viestejä valmentajille jokaisella neljästä päivittäisestä BoxerBase-haun kierroksesta. Tarvitaan vaiheeseen sidotut, kerran syntyvät ehdotukset.

## Mitä teknisesti on tehty?

Kehityshaarassa `feat/editorial-news-decision-policy-20261025`:
- `config/editorial_news_policy.json` sisältää vain erikseen uutisarvoiseksi nimetyt kilpailut sekä jo julkaistujen uutisten tapahtuma-ID-kattavuuden. Nykyisen Nuorten SM -tapahtuman kohdalta yksi ehdotus on sallittu, tavallisista kilpailuista ei.
- `scripts/editorial_news_triggers.py` on puhdas ehdotuksia muodostava moduuli. Se ei lähetä sähköpostia, ei tallenna julkaisua, ei kirjoita Yhdistysavaimeen eikä postaa someen.
- `tests/test_editorial_news_triggers.py` testaa duplikaatit, valmentajan vahvistuksen, yhden koosteuutisen, tavalliset kilpailut sekä puuttuvat tulokset.

Nykyinen `docs/data.json`-syöte ei ole muuttunut eikä käyttäjän näkyville tule uusia julkaisemattomia ehdotuksia.

## Mitä tarvitaan ennen varsinaista uutisautomaatiota?

1. Yksityinen hyväksyntäbackend ja tilojen pysyvä tallennus (edelleen suunnitteilla, ei käytössä).
2. Luonnoksen lähettämiseen soveltuva erillinen `kehaketut.aineisto@gmail.com`-postilaatikko on yhdistetty; sitä ei saa käyttää suoraan julkaisun laukaisijana.
3. Valmentajan varmennus ja Gleb/Pepe/Erika-henkilökohtainen hyväksyntä, yhden hyväksyntä riittää.
4. Uutisen julkaiseminen Yhdistysavain → Uutiset → Lisää uutinen säilyy nykyvaiheessa manuaalisena lopullisena vaiheena. Natiivia sähköposti→Yhdistysavain-kirjoitusrajapintaa ei ole varmistettu.
5. Kun automaatio on valmis, luonnosten ehdottamista ohjaa uutisarvo ja olemassa oleva tapahtumarekisteri, ei jokaisen raakamuutoksen erillinen lähettäminen.

**Tämä on tarkoituksella konservatiivinen ratkaisu:** sivut saavat elämää automaattisista kilpailutiedoista ja kuvavirroista; uutisarkisto pysyy toimitettuna ja luettavana.
