# Kehä-Ketut – jatkosuunnitelma 25.10.2026

## Ensisijaiset, käytännön toimet

1. **BoxerBase-tietojen yhdistäminen (Tomi / valmennuksen yhteyshenkilö):** pyydetään poistamaan duplikaattiseura vasta sitten, kun vanhan seuran ja ottelijaprofiilien historialliset ottelut on siirretty oikeaan seuraan/profiileihin. Oikea seuraprofiili on 1Le8shnOwPIW. Erityisesti Josias Joseph Ndikumanan 0 vs 1 -ottelun ristiriita sekä muiden ottelijoiden puuttuvat tiedot. Kun yhdistäminen valmis, tarkistetaan ja poistetaan integraation väliaikaiset alias-poikkeukset.
2. **Yhdistysavaimen loppusiivous:** varmistetaan, ettei vanhaa Uutislistaa, vanhaa staattista nyrkkeilijäluetteloa tai kahta erillistä someosiota näy uuden rinnalla. Yhtenäisen someosion asennus ja mobiilinäkymä varmistetaan. Etusivun muokkaus keskitetään ylläpitäjälle.
3. **Julkaisuprosessin käyttöönotto hallituksessa:** Pepe ja muut sisältöä tekevät hallituksen jäsenet käyttävät vain Uutiset → Lisää uutinen. Annetaan mahdollisimman lyhyt ohje ja tarvittaessa katsotaan yhdessä.
4. **Automaation toiminnan valvonta:** varmistetaan GitHub Actionsin neljä päivittäistä ajoa, uutissyötteen julkaisu, Facebookin erillisen päivittäisen ajastuksen toiminta sekä Juicerin Instagram-yhteyden pysyminen voimassa. Ei virheellisiä väitteitä täysin kattavasta kilpailuhistoriasta.

## Seuraavat kehitykset

5. **Uusien kilpailujen kattavampi löydettävyys:** tutki BoxerBasen sallittua rajapintaa/keruuta tapahtumien, ilmoittautumisten ja vahvistettujen ottelulistojen erottamiseen. Ilmoittautuminen ei saa näkyä vahvistettuna otteluparina.
6. **Nyrkkeilijäsivujen yhdenmukaistaminen:** viiden olemassa olevan henkilöesittelyn käsin kirjoitetut ottelumäärät voivat erota automaattisista luvuista. Poista tai selkeytä vanhojen lukujen päivämäärät, lisää mahdollisten uusien urheilijoiden seuran omat sivut sovitusti.
7. **Somejulkaisuluonnokset tuloksista:** uusista vahvistetuista tuloksista luonnos Facebookiin ja Instagramiin Metricoolin kautta. Ensimmäisessä vaiheessa julkaisuihin aina ihmisen hyväksyntä. Sävy asiallinen, hyväntuulinen ja luonnollinen, ei ylitsevuotava. Useita otteluita samasta kisasta mielellään yksi yhteinen kooste.
8. **Kuvallinen sisältö ja viestintä:** seuran omat kilpailu- ja harjoituskuvat, henkilötiedot ja alaikäisten kuvien käyttöoikeudet; harkitaan yhtenäisiä julkaisu-/uutiskuvapohjia. Instagram-kuvavirta päivittää sivua automaattisesti, mutta itse kuvia pitää edelleen julkaista lähdetiliin.
9. **Yhdistysavaimen rajoitukset:** tarvittaessa siirretään lisää HTML/CSS/JS-logiikkaa GitHub Pagesiin, jotta merkkirajat ja sisällönhallinta pysyvät hallinnassa. Oman sivuston alustan vaihtoa ei tarvita nyt.
10. **Ylläpito-ohje ja palautekierros:** hallitukselta kehitysideat; parannukset toteutetaan priorisoidusti. Myöhemmin voidaan rakentaa julkinen automaation tilasivu ja häiriöilmoitukset.

## Valmistumisen määritelmä

- Seuran uutisen voi kirjoittaa Yhdistysavaimeen ilman etusivun muokkausta ja se ilmestyy etusivun kolmeen uusimpaan uutiskorttiin.
- Tulokset ja ottelijatilastot päivittyvät ilman manuaalista kopiointia tunnetuista kilpailuista ja profiileista.
- Instagram- ja Facebook-sisällöt näkyvät siististi samalla rivillä eri laitteissa ja pysyvät kytkettyinä vain seuran tileihin.
- Hallitus tietää, mikä on automaattista ja mikä edelleen manuaalista.
- Korjattu BoxerBase-yhdistäminen tekee seuran tulostilastoista nykyistä kattavammat.
- Sosiaalisen median automaattinen varsinainen julkaiseminen tehdään vasta hyväksyntäprosessin kanssa.
