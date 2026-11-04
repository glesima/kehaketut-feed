"""One-off reviewed branch patch. Removed before the candidate commit."""
from pathlib import Path
import json

aliases={'KyEKnjm-NRp4':'Pi3gCaWD-7jD','U2N_OOYxyFui':'h9XYEbAs3Py4','0efaqUGeO1JP':'W9dy-RM88aLL','rLyNGj8sCoF7':'vfT3Q-X7B3Tf','RGUkxNVIo4px':'jRMAAn1JtaN6','5A-7Dh4jmTdy':'ir_z7p9BvsZM','CVjkkb7fii6a':'RyBcZO1fI2Rb','2zTFqL5gFsqg':'nqzy3scM-NDs','vK0bN2sPxnbo':'PxXnRMHDTclP'}
config=json.loads(Path('config.json').read_text())
assert config['club_id']=='1Le8shnOwPIW','Unexpected baseline: do not reapply or overwrite'
config.update(club_id='mZjkT0LW248X',club_url='https://boxerbase.com/o/mZjkT0LW248X/boxers',
 club_names=['RIIHIMÄEN KEHÄ-KETUT','Riihimäen Kehä-Ketut ry'],registration_club_aliases=[],verified_stat_aliases={},
 confirmed_club_merge={'from':'1Le8shnOwPIW','to':'mZjkT0LW248X','confirmed_on':'2026-11-04'},
 boxer_id_aliases=aliases,boxer_name_aliases={'Josias Ndikumana':'Josias Joseph Ndikumana'})
for e in config['tracked_events']:
 e.pop('allow_alias_club_on_bouts',None);e.pop('verified_as_duplicate_label',None)
Path('config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')

def edit(path,pairs):
 p=Path(path);s=p.read_text()
 for old,new in pairs:
  assert s.count(old)==1,(path,'unexpected anchor count',old[:90],s.count(old))
  s=s.replace(old,new,1)
 p.write_text(s)

edit('scripts/update.py',[
 ('from event_discovery import discover_event_links, event_id_from_url, parse_public_registrations','from event_discovery import discover_event_links, event_id_from_url, parse_public_registrations\nfrom club_identity import confirmed_merge, canonical_previous, validate_merged_roster, profile_bout_urls, mark_stats_quality'),
 ('    out = dict(previous)\n','    previous = canonical_previous(previous, CONFIG)\n    out = dict(previous)\n'),
 ('    errors = []\n','    errors = []\n    profile_links = []\n'),
 ('        previous_map = {v.get("id"):v for v in previous.get("boxers", [])}','        validate_merged_roster(boxers, previous, CONFIG)\n        previous_map = {v.get("id"):v for v in previous.get("boxers", [])}'),
 ('                profile = parse_profile(fetch(boxer["boxerbase_url"]))','                profile_html = fetch(boxer["boxerbase_url"])\n                profile = parse_profile(profile_html)\n                profile_links.extend(profile_bout_urls(profile_html, boxer["boxerbase_url"]))'),
 ('        out["boxers"] = boxers\n        if previous.get("club_id") != CONFIG.get("club_id"):','        for boxer in boxers:\n            mark_stats_quality(boxer)\n            if boxer["stats_consistency"] == "inconsistent":\n                LOG.warning("Canonical profile %s has inconsistent summary counts; preserving source values, UI marks pending review", boxer["id"])\n        out["boxers"] = boxers\n        out["boxer_id_aliases"] = CONFIG.get("boxer_id_aliases", {})\n        if (previous.get("club_id") != CONFIG.get("club_id")\n                and not confirmed_merge(previous, CONFIG)):'),
 ('        out["club_url"] = CONFIG["club_url"]','        out["club_url"] = CONFIG["club_url"]\n        out["club_name"] = CONFIG["club_names"][0]'),
 ('    except Exception as ex:\n        errors.append(f"Club roster: {ex}")','    except Exception as ex:\n        if confirmed_merge(previous, CONFIG):\n            raise RuntimeError("Canonical club migration could not be verified; previous feed unchanged") from ex\n        errors.append(f"Club roster: {ex}")'),
 ('        index = CONFIG["event_index"]','        # Restored public profile history can include untracked past events.\n        for bout_url in profile_links:\n            eid = event_id_from_url(bout_url)\n            if eid and eid not in known_ids:\n                known_ids.add(eid)\n                events.append({"url":bout_url.split("/m/")[0],\n                               "name":"BoxerBase-kilpailu", "date":None})\n        index = CONFIG["event_index"]'),
 ('                links = match_links(html, list_url, names)','                links = match_links(html, list_url, names)\n                for profile_url in profile_links:\n                    if (event_id_from_url(profile_url) == event_id_from_url(info["url"])\n                            and profile_url not in links):\n                        links.append(profile_url)'),
 ('            if name.casefold() in competitor.casefold():','            aliases = [name] + [a for a, n in CONFIG.get("boxer_name_aliases", {}).items() if n == name]\n            if competitor.casefold() in [a.casefold() for a in aliases]:'),
 ('and club.casefold() in label.casefold() for label in player_links)','and any(n.casefold() in label.casefold() for n in [club] + [a for a, v in CONFIG.get("boxer_name_aliases", {}).items() if v == club]) for label in player_links)'),
 ('    # Specific historic bouts were registered under BoxerBase\'s duplicate club.\n    # Accept that label only for a manually verified known competition, never generally.','    # club_names includes the reviewed former label on historical match cards.\n    # Roster and statistics use only the surviving organization/profile IDs.\n    # Per-event aliases remain available for other explicitly reviewed configurations.')
])
edit('docs/widget.html',[
 ('https://boxerbase.com/o/1Le8shnOwPIW/boxers','https://boxerbase.com/o/mZjkT0LW248X/boxers'),
 ('  c.appendChild(mk("p","",b.matches==null?','  if(b.stats_consistency==="inconsistent"){\n   c.appendChild(mk("p","dim","BoxerBasen yhteenvetotilastot tarkistettavana."));\n  }else{\n  c.appendChild(mk("p","",b.matches==null?'),
 ('  c.appendChild(link("Avaa ottelijaprofiili ↗",b.stats_source_url||b.boxerbase_url));','  }\n  c.appendChild(link("Avaa ottelijaprofiili ↗",b.stats_source_url||b.boxerbase_url));'),
 (' var b=(d.boxers||[]).find(function(a){return a.id===boxerId});',' var canonicalId=(d.boxer_id_aliases||{})[boxerId]||boxerId;\n var b=(d.boxers||[]).find(function(a){return a.id===canonicalId});'),
 (' add(stat,metric(b.matches,"Ottelua"),metric(b.wins,"Voittoa"),metric(b.losses,"Tappiota"));',' var consistent=b.stats_consistency!=="inconsistent";\n add(stat,metric(consistent?b.matches:null,"Ottelua"),metric(consistent?b.wins:null,"Voittoa"),metric(consistent?b.losses:null,"Tappiota"));\n if(!consistent)card.appendChild(mk("p","dim","BoxerBasen yhteenvetotilastot ovat ristiriitaiset ja tarkistettavana. Yksittäiset ottelutulokset näytetään lähteen mukaisesti."));'),
 ('Ottelutietoja voidaan täydentää, kun BoxerBasen seuramerkintöjä yhtenäistetään.','Tiedot haetaan seuran yhdistetyistä BoxerBase-profiileista. Julkinen ottelulista voi täydentyä.')
])
loader="""    if(!document.querySelector('script[data-rkk-boxerbase-links]')){
      var compat=document.createElement('script');compat.dataset.rkkBoxerbaseLinks='1';
      compat.src='https://glesima.github.io/kehaketut-feed/boxerbase-links.js?v=20261104';
      document.head.appendChild(compat);
    }
"""
edit('docs/news-loader.js',[('  function boot(){\n','  function boot(){\n'+loader)])
edit('docs/profile-embed.js',[( '"'+old+'"','"'+new+'"') for old,new in aliases.items()]+[
 ('  var slug=',loader+'  var slug='),
 ('if(e.origin!=="https://glesima.github.io"||!e.data','if(e.origin!=="https://glesima.github.io"||e.source!==f.contentWindow||!e.data')])
edit('tests/test_update.py',[
 ('self.assertEqual(CONFIG["club_id"], "1Le8shnOwPIW")','self.assertEqual(CONFIG["club_id"], "mZjkT0LW248X")'),
 ('self.assertEqual(CONFIG["club_names"], ["Riihimäen Kehä-Ketut ry"])','self.assertEqual(CONFIG["club_names"][0], "RIIHIMÄEN KEHÄ-KETUT")\n        self.assertEqual(CONFIG["verified_stat_aliases"], {})'),
 ('def test_wrong_duplicate_club_is_rejected','def test_unrelated_club_is_rejected')])
p=Path('tests/test_update.py');s=p.read_text();a=s.index('    def test_unrelated_club_is_rejected');b=s.index('    def test_parse_result_win',a)
s=s[:a]+s[a:b].replace('RIIHIMÄEN KEHÄ-KETUT','UNRELATED BOXING CLUB')+s[b:];p.write_text(s)
edit('.github/workflows/pr-validation.yml',[('      - name: Inline website JavaScript syntax','      - name: Verify merged club identity compatibility\n        run: node tests/test_club_identity.js\n      - name: Inline website JavaScript syntax')])
edit('CONTEXT_HANDOFF.md',[('## Säilyvät toimintaperiaatteet','## BoxerBase-lähde 4.11.2026 alkaen\n\nLue `docs/BOXERBASE_MERGE_2026-11-04.md`. Ainoa seurattava organisaatio on `mZjkT0LW248X`. Aiemmat kirjoitusasu-/rinnakkaisprofiiliohjeet ovat historiaa; älä palauta `1Le8shnOwPIW`-lähdettä. Tunnetun yhdistämisen vuoksi tuloshistoriaa ei tyhjennetä, eikä kahden profiilin tilastoja summata.\n\n## Säilyvät toimintaperiaatteet')])
edit('CURRENT_STATUS.md',[
 ('Päivitetty 2.11.2026.','Päivitetty 4.11.2026.'),
 ('## Somepalstojen korkeudet korjattu','## BoxerBase: yhdistetyn seuran lähdemigraatio 4.11.2026\n\nLähdeseura on RIIHIMÄEN KEHÄ-KETUT (`mZjkT0LW248X`), johon vanha `1Le8shnOwPIW` yhdistettiin. Yhdeksän säilynyttä ottelijaprofiilia varmennettiin. Tunnistekartta, historiatietojen säilytys, ilmoittautumisten kohdistus ja linkkien yhteensopivuus on kuvattu `docs/BOXERBASE_MERGE_2026-11-04.md`:ssä.\n\nNeljässä lähdeprofiilissa voittojen ja tappioiden summa ylittää ottelumäärän. Sivusto ei summaa profiileja tai arvaa lukuja, vaan merkitsee ristiriitaisen yhteenvedon tarkistettavaksi. Yksittäiset tulokset säilyvät.\n\nToteutus on korjaushaarassa; käyttöönotto ja tuoreen syötteen varmennus kirjataan julkaisun jälkeen. Someosiot, uutiset, media-vastaanotto ja aiemmat julkaisut säilyvät ennallaan.\n\n## Somepalstojen korkeudet korjattu')])
print('Reviewed migration anchors applied; no production branch changed.')
