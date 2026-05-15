# ============================================================
#  ⚔  ANCIENT TRANSLATOR  ⚔
#  Kivy app – fully offline, no internet or API required
#  Modes: Medieval Dutch | Pirate | Old Egypt | Shakespeare
#
#  Install requirements:
#    pip install kivy
#  Run:
#    python ancient_translator.py
# ============================================================

import random
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.widget import Widget

# ─── Window setup ───────────────────────────────────────────
Window.clearcolor = (0.08, 0.06, 0.03, 1)
Window.size = (900, 650)

# ════════════════════════════════════════════════════════════
#  MEDIEVAL DUTCH DICTIONARY
# ════════════════════════════════════════════════════════════

MW_WORDS = {
    # Pronouns
    "ik": ["ick", "ick mijzelf", "ick, de onwaardige"],
    "jij": ["gij", "gij edele", "u"],
    "je": ["gij", "u"],
    "jou": ["u", "uw persoon"],
    "jouw": ["uwen", "uw"],
    "mij": ["mij", "mijne persoon"],
    "me": ["mij"],
    "hij": ["dese heer", "den edelman", "hij"],
    "zij": ["dese vrouwe", "de edelvrouwe"],
    "ze": ["dezen", "dezelve"],
    "het": ["het", "hetzelve"],
    "wij": ["wij allen", "wij gezamenlijk"],
    "we": ["wij", "wij tezamen"],
    "hun": ["hunne", "derzulken"],
    "hen": ["henlieden", "dezelven"],
    "wie": ["welke persoon", "wie aldaar"],
    "wat": ["hetgeen", "wat dan ook"],

    # Common verbs
    "ben": ["ben", "bevinde mijzelve"],
    "is": ["is", "bevindt zich", "wezende"],
    "zijn": ["wezen", "zijn"],
    "was": ["was", "was voorheen"],
    "waren": ["waren", "waren te dien tijde"],
    "heeft": ["bezit", "heeft in zijn bezit"],
    "hebben": ["bezitten", "in bezit houden"],
    "had": ["bezat", "had te zijner tijd"],
    "hadden": ["bezaten", "hadden alsdan"],
    "gaat": ["begeeft zich", "gaat voort"],
    "gaan": ["zich begeven", "voortgaan"],
    "ging": ["begaf zich", "trok voort"],
    "gingen": ["begaven zich", "trokken voort"],
    "komt": ["aankomt", "verschijnt"],
    "komen": ["aanschouwen", "verschijnen"],
    "ziet": ["aanschouwt", "bemerkt"],
    "zien": ["aanschouwen", "waarnemen"],
    "zegt": ["verkondigt", "spreekt"],
    "zeggen": ["verkundigen", "spreken"],
    "weet": ["kent en weet", "is bekend met"],
    "weten": ["kennen en weten", "bekend zijn met"],
    "denkt": ["overweegt", "peinst"],
    "denken": ["overwegen", "peinzen"],
    "wil": ["begeert", "verlangt"],
    "willen": ["begeren", "verlangen"],
    "kan": ["vermag", "is bij machte"],
    "kunnen": ["vermogen", "bij machte zijn"],
    "moet": ["dient te", "is gehouden te"],
    "moeten": ["dienen te", "gehouden zijn te"],
    "mag": ["het is vergund", "het is geoorloofd"],
    "mogen": ["vergund zijn", "geoorloofd zijn"],
    "geeft": ["overreikt", "schenkt"],
    "geven": ["overreiken", "schenken"],
    "neemt": ["aangrijpt", "grijpt"],
    "nemen": ["aangrijpen", "grijpen"],
    "loopt": ["gaat te voet", "trekt"],
    "lopen": ["te voet gaan", "trekken"],
    "werkt": ["arbeidt", "verricht zijn plicht"],
    "werken": ["arbeiden", "zijn plicht verrichten"],
    "woont": ["verblijft", "zetelt"],
    "wonen": ["verblijven", "zetelen"],
    "leeft": ["leeft ten leven", "heeft het leven"],
    "leven": ["ten leven zijn", "het leven hebben"],
    "schrijft": ["stelt op schrift", "noteert"],
    "schrijven": ["op schrift stellen", "noteren"],
    "leest": ["aanschouwt het schrift", "leest het manuscript"],
    "lezen": ["het schrift aanschouwen", "het manuscript lezen"],
    "spreekt": ["voert het woord", "verkundigt"],
    "spreken": ["het woord voeren", "verkundigen"],
    "hoort": ["verneemt", "hoort met de oren"],
    "horen": ["vernemen", "met de oren opvangen"],
    "helpt": ["staat bij", "verleent hulp aan"],
    "helpen": ["bijstaan", "hulp verlenen aan"],
    "vraagt": ["beraagt", "verzoekt"],
    "vragen": ["beragen", "verzoeken"],
    "antwoordt": ["geeft antwoord", "repliceert"],
    "antwoorden": ["antwoord geven", "repliceren"],
    "koopt": ["schaf aan", "verwerft"],
    "kopen": ["aanschaffen", "verwerven"],
    "verkoopt": ["doet van de hand", "verkoopt"],
    "verkopen": ["van de hand doen", "vervreemden"],
    "vindt": ["ontdekt", "treft aan"],
    "vinden": ["ontdekken", "aantreffen"],
    "verliest": ["raakt kwijt", "verliest"],
    "verliezen": ["kwijtraken", "verliezen"],
    "wacht": ["verbeidt", "wacht geduldig"],
    "wachten": ["verbeiden", "geduldig wachten"],
    "probeert": ["tracht", "poogt"],
    "proberen": ["trachten", "pogen"],
    "lacht": ["is vrolijk", "verheugt zich"],
    "lachen": ["vrolijk zijn", "zich verheugen"],
    "weent": ["schreit", "vergiet tranen"],
    "wenen": ["schreien", "tranen vergieten"],
    "slaapt": ["rust in slaap", "neemt zijn rust"],
    "slapen": ["in slaap rusten", "zijn rust nemen"],
    "eet": ["nuttig zijn maal", "spijzigt zich"],
    "eten": ["zijn maal nuttighen", "zich spijzigen"],
    "drinkt": ["lest zijn dorst", "neemt zijn drank"],
    "drinken": ["zijn dorst lessen", "drank tot zich nemen"],
    "zingt": ["heft een lied aan", "jubileert"],
    "zingen": ["een lied aanheffen", "jubileren"],
    "danst": ["huppelt van vreugde", "danst"],
    "dansen": ["van vreugde huppelen", "dansen"],
    "vecht": ["strijdt", "doet den strijd"],
    "vechten": ["strijden", "den strijd doen"],
    "wint": ["behaalt de overwinning", "zegeviert"],
    "winnen": ["de overwinning behalen", "zegevieren"],
    "verliest": ["lijdt de nederlaag", "wordt verslagen"],

    # Nouns – people
    "man": ["heer", "edelman", "heer van stand"],
    "vrouw": ["edelvrouwe", "vrouwe", "dame van stand"],
    "kind": ["jong wicht", "kleine edeling", "jeugdig wezen"],
    "kinderen": ["jonge wichten", "de jeugdige telgen"],
    "baby": ["de pasgeborene", "het jonge wicht"],
    "jongen": ["de jongeling", "de knaap"],
    "meisje": ["de jonkvrouwe", "de jonge dame"],
    "vader": ["de eerwaarde vader", "de patriarch"],
    "moeder": ["de eerwaarde moeder", "de matriarch"],
    "broer": ["de broeder", "de mannelijke telg"],
    "zus": ["de zuster", "de vrouwelijke telg"],
    "opa": ["de grijsaard", "de eerbiedwaardige oudste"],
    "oma": ["de eerwaarde grootmoeder", "de edelvrouwe van hoge leeftijd"],
    "vriend": ["edel vriend", "trouwe metgezel", "bondgenoot"],
    "vriendin": ["edele vriendin", "trouwe gezellin"],
    "vijand": ["vijand en belager", "de gehate tegenstander"],
    "buurman": ["de nabuurige heer", "de aangrenzende edelman"],
    "buurvrouw": ["de nabuurige vrouwe"],
    "dokter": ["de geneesheer", "de meester der geneeskunst"],
    "leraar": ["de meester", "de leermeester"],
    "soldaat": ["de krijgsman", "de wapendrager"],
    "ridder": ["de edel ridder", "de wapenrusting dragende heer"],
    "koning": ["de verheven vorst", "de doorluchtige koning"],
    "koningin": ["de doorluchtige koninginne", "de verheven vorstin"],
    "prins": ["de doorluchtige prins", "de koninklijke telg"],
    "prinses": ["de schone prinses", "de doorluchtige jonkvrouwe"],
    "keizer": ["de machtige keizer", "de opperheer"],
    "hertog": ["de hertog", "de edele hertog"],
    "graaf": ["de graaf", "de edele graaf"],
    "baron": ["de baron", "de edele baron"],
    "bisschop": ["de eerwaarde bisschop"],
    "priester": ["de eerwaarde priester", "de geestelijke"],
    "monnik": ["de vrome monnik", "de kloosterling"],

    # Nouns – places
    "huis": ["huys", "het onderkomen", "de woning"],
    "thuis": ["ten huyze", "in het eigen onderkomen"],
    "kamer": ["de vertrekke", "het gemak"],
    "slaapkamer": ["de slaapvertrekke", "het nachtverblijf"],
    "keuken": ["de keukene", "het kookhuis"],
    "tuin": ["de hof", "het besloten erf"],
    "kasteel": ["het burchtslot", "de vestinge"],
    "kerk": ["het heilige bedehuis", "de godstempel"],
    "school": ["de leerschole", "het onderwijs gesticht"],
    "winkel": ["de koopmansstede", "het handelshuis"],
    "markt": ["de weekmarkt", "de koopplaats"],
    "stad": ["de stede", "de ommuurde stad"],
    "dorp": ["het gehucht", "het landelijk gehucht"],
    "land": ["het koninkrijck", "het vaderland"],
    "bos": ["het donkere woud", "het uitgestrekte woud"],
    "rivier": ["de groote stroom", "de vlietende rivier"],
    "zee": ["de woeste zee", "de ontembare oceaan"],
    "berg": ["de hoge rots", "het gebergte"],
    "veld": ["het wijde veld", "de vlakte"],
    "weg": ["de kronkelende weg", "het pad"],
    "brug": ["de houten brug", "de stenen brug"],
    "poort": ["de stadspoort", "de eikenhouten poort"],
    "toren": ["de wachttoren", "de hoge toren"],
    "muur": ["de stenen muur", "de vestingwal"],
    "put": ["de waterput", "de fontein"],

    # Nouns – nature / time
    "dag": ["dezen dag", "dese dagh"],
    "nacht": ["den duisteren nacht", "de nachtelijke ure"],
    "ochtend": ["den ochtendt", "de vroege dageraad"],
    "middag": ["den middag", "het middaguur"],
    "avond": ["den avondstonde", "de schemering"],
    "week": ["de sevendag", "de lopende week"],
    "maand": ["de maand", "de maanstand"],
    "jaar": ["het jaer", "het verlopen jaer"],
    "lente": ["het voorjaer", "de lente des levens"],
    "zomer": ["de warme zomer", "de zomertijd"],
    "herfst": ["de herfst", "het vallend seizoen"],
    "winter": ["de ruwe winter", "de barre wintermaanden"],
    "zon": ["de heilige zon", "het hemelse licht"],
    "maan": ["de bleeke maan", "het nachtelijk licht"],
    "ster": ["het hemellicht", "de glinsterende ster"],
    "regen": ["de neerdalende regen", "de hemelse regen"],
    "sneeuw": ["de witte sneeuw", "het witte deken"],
    "wind": ["de gierend wind", "de adem des hemels"],
    "storm": ["de geweldige storm", "de onstuimige storm"],
    "vuur": ["het heilige vuur", "de vlam"],
    "water": ["het klare water", "het levende water"],
    "aarde": ["de vruchtbare aarde", "het aardrijk"],
    "lucht": ["de uitspansel", "het hemelblauw"],

    # Nouns – objects
    "boek": ["het perkamenten manuscript", "het leerboek"],
    "brief": ["de schriftelijke boodschap", "het epistel"],
    "pen": ["de ganzenveer", "het schrijfgerei"],
    "papier": ["het perkament", "het schrijfvel"],
    "geld": ["goud en zilver", "het geldstuk"],
    "brood": ["het dagelijksche brood", "het vers gebakken brood"],
    "vlees": ["het gebraden vleesch", "het vleesch"],
    "wijn": ["de edele wijn", "de druivenkorf"],
    "bier": ["het gerstenat", "de schuimende drank"],
    "water": ["het klare water", "het fonteinwater"],
    "kleding": ["het gewaad", "het kleed"],
    "mantel": ["de wollen mantel", "het omhangsel"],
    "hoed": ["de hoofdtooi", "het hoofddeksel"],
    "schoen": ["de leerschoen", "het voetenkleed"],
    "zwaard": ["het edel zwaard", "het stalen wapen"],
    "schild": ["het houten schild", "de defensieve wapenrusting"],
    "paard": ["het edel ros", "het rijdier"],
    "hond": ["de trouwe hond", "de waakhond"],
    "kat": ["het kattenbeest", "de huispoes"],
    "vogel": ["de gevleugelde", "het vliegende schepsel"],
    "vis": ["de watervis", "het waterbeest"],
    "tafel": ["de tafelplank", "het eettafel"],
    "stoel": ["de rustbank", "de zetel"],
    "bed": ["het rustbed", "de slaapplaats"],
    "deur": ["de eikenhouten poort", "de toegangsdeur"],
    "raam": ["het venster", "de glasopening"],
    "lamp": ["de kaars", "het lichtpunt"],
    "vuur": ["het heilige vuur", "de haard"],

    # Adjectives
    "goed": ["edel en goed", "voortreffelijk", "loffelijk"],
    "slecht": ["verdorven en snood", "jammerlijk", "verfoeilijk"],
    "groot": ["verheven en groot", "van aanzienlijke grootte"],
    "klein": ["gering van formaat", "van kleine omvang"],
    "oud": ["van oudsher", "bejaard van jaren"],
    "nieuw": ["nieuwelijcks", "vers van origine"],
    "mooi": ["schoon van aanschijn", "fraai van uiterlijk"],
    "lelijk": ["onbegaafd van uiterlijk", "misvormd van gelaat"],
    "snel": ["met grote spoed", "vlug als de wind"],
    "langzaam": ["met trage pas", "slepend van beweging"],
    "sterk": ["sterk van lichaam", "krachtig van gestel"],
    "zwak": ["zwak van gestel", "broos van lichaam"],
    "slim": ["wijs van geest", "scherpzinnig"],
    "dom": ["van eenvoudige geest", "ongeletterd"],
    "arm": ["van geringe stand", "berooid"],
    "rijk": ["van aanzienlijke rijkdom", "welgesteld"],
    "blij": ["verheugd van harte", "opgetogen"],
    "droevig": ["bedroefd van ziele", "troosteloos"],
    "boos": ["vertoornd van gemoed", "toornig"],
    "bang": ["vervuld van vrees", "angstvallig"],
    "moe": ["afgemat van lijve", "uitgeput"],
    "ziek": ["door ziekte geveld", "kwakkelend"],
    "gezond": ["gezond van lijf en leden", "florissant"],
    "lief": ["lieftallig", "beminnelijk"],
    "gemeen": ["laaghartig", "snood van karakter"],
    "eerlijk": ["rechtschapen", "deugdzaam"],
    "vals": ["bedrieglijk", "verraderlijk"],
    "dapper": ["moedig en dapper", "onverschrokken"],
    "laf": ["laf van aard", "bloode"],
    "gelukkig": ["gezegend", "in geluk badende"],
    "ongelukkig": ["ongelukkig van lot", "rampzalig"],
    "leuk": ["aangenaam", "vermakelijk"],
    "saai": ["vervelend van aard", "eentonig"],
    "interessant": ["van groot belang", "merkwaardig"],
    "vreemd": ["wonderbaarlijk", "vreemd van aard"],
    "normaal": ["gewoon van aard", "alledaags"],
    "bijzonder": ["uitzonderlijk", "buitengewoon"],
    "belangrijk": ["van groot gewicht", "van hoge importantie"],
    "gevaarlijk": ["gevaarlijk van aard", "levensbedreigend"],
    "veilig": ["in veiligheid", "geborgen"],
    "heet": ["gloeiend heet", "brandend heet"],
    "koud": ["ijzig koud", "guurkoud"],
    "warm": ["aangenaam warm", "weldadig warm"],
    "zwaar": ["zwaar van gewicht", "bezwarend"],
    "licht": ["licht van gewicht", "vederlicht"],
    "hard": ["hard als steen", "onverbiddelijk"],
    "zacht": ["zacht als fluweel", "teder"],
    "diep": ["diep als de put", "grondeloos diep"],
    "hoog": ["hoog als de toren", "verheven"],
    "lang": ["lang van stature", "uitgestrekt"],
    "kort": ["gering van lengte", "beknopt"],
    "breed": ["breed van omvang", "wijds"],
    "smal": ["smal van doorgang", "nauw"],
    "vol": ["vol tot de rand", "boordevol"],
    "leeg": ["leeg en verlaten", "ontvolkt"],
    "open": ["wijd open", "onbesloten"],
    "gesloten": ["gesloten en vergrendeld", "afgegrendeld"],

    # Adverbs / conjunctions
    "maar": ["doch", "evenwel"],
    "en": ["ende", "en tevens"],
    "of": ["ofte", "dan wel"],
    "want": ["want alsoo", "dewijl"],
    "omdat": ["alsoo", "overmits"],
    "dus": ["derhalve", "mitsdien"],
    "ook": ["mede", "insgelijks"],
    "nog": ["noch", "bovendien"],
    "al": ["reeds", "alreeds"],
    "toen": ["ten tijde dat", "in de tijde dat"],
    "als": ["wanneer", "te dien tijde dat"],
    "nu": ["te dezen tijde", "thans"],
    "dan": ["alsdan", "ten tijde van"],
    "hier": ["alhier", "op deze stede"],
    "daar": ["aldaar", "op gene stede"],
    "niet": ["geenszins", "op geen wijze"],
    "nooit": ["nimmermeer", "te geener tijde"],
    "altijd": ["te allen tijde", "onveranderlijk"],
    "soms": ["bij gelegenheid", "van tijd tot tijd"],
    "vaak": ["dikwijls", "geregeld"],
    "zelden": ["zelden", "spaarzaam"],
    "heel": ["ten zeerste", "in hoge mate"],
    "erg": ["ten zeerste", "bijzonder"],
    "zeer": ["in hoge mate", "ten zeerste"],
    "wel": ["zonder twijfel", "voorwaar"],
    "niet": ["geenszins", "op generlei wijze"],
    "misschien": ["wellicht", "het is niet ondenkbaar"],
    "zeker": ["zonder twijfel", "voorwaar"],
    "samen": ["gezamenlijk", "te zamen"],
    "alleen": ["alleen en verlaten", "eenzaam"],
    "snel": ["met grote spoed", "haastelijk"],
    "langzaam": ["met trage pas", "bedachtzaam"],
    "graag": ["gaarne", "met graagte"],
    "liever": ["liever", "met grotere begeerte"],
    "toch": ["nochtans", "evenwel"],
    "echt": ["waarlijk", "in waarheid"],
    "gewoon": ["zoals gebruikelijk", "op gewone wijze"],
    "bijna": ["nagenoeg", "ten naaste bij"],
    "net": ["juist", "precies"],
    "al": ["reeds", "alreeds"],
    "nog": ["nog immer", "nog altijd"],
    "weer": ["wederom", "andermaal"],
    "nog": ["noch immer", "nog steeds"],
    "ook": ["mede", "eveneens"],
    "zelfs": ["zelfs", "ja zelfs"],
    "anders": ["anderszins", "op andere wijze"],
    "zo": ["alzoo", "op dergelijke wijze"],
    "meer": ["meer", "in grotere mate"],
    "minder": ["minder", "in mindere mate"],
    "te": ["al te", "overdadig"],

    # Common phrases parts
    "vandaag": ["op dezen dagh", "heden ten dage"],
    "morgen": ["op den volgenden dageraad", "morgenstond"],
    "gisteren": ["op den vorigen dagh", "gisteren"],
    "vanavond": ["dezen avondstonde", "in de late avond"],
    "vannacht": ["dezen nacht", "in de nachtelijke ure"],
    "straks": ["weldra", "binnen korte tijd"],
    "later": ["later", "te zijner tijd"],
    "vroeger": ["in vroeger tijden", "van oudsher"],
    "nooit": ["nimmermeer", "te geener tijde"],
    "altijd": ["te allen tijde", "steeds en altijd"],
    "soms": ["bij gelegenheid", "bij wijlen"],
}

# Dutch names → medieval versions (200+ names)
MW_NAMES = {
    "jan": ["Jan der Ridder", "Jan van den Ouden Stede", "Jan de Dappere"],
    "kees": ["Kees van den Ouden", "Kees der Velden", "Kees de Wijze"],
    "piet": ["Piet van het Veld", "Piet der Hoeven", "Piet de Sterke"],
    "henk": ["Henk van den Burcht", "Henk der Wouden"],
    "hans": ["Hans de Brouwer", "Hans van den Rijn"],
    "dirk": ["Dirk der Dapperen", "Dirk van den Toren"],
    "gerard": ["Gerard de Edele", "Gerard van het Kasteel"],
    "willem": ["Willem de Vermaarde", "Willem der Ridders", "Willem van Oranje"],
    "thomas": ["Thomas der Geleerden", "Thomas de Wijze"],
    "peter": ["Peter van de Toren", "Peter der Schilden"],
    "mark": ["Mark der Strijder", "Mark van het Zwaard"],
    "bas": ["Bas van de Vlakte", "Bas den Onverschrokkene"],
    "sven": ["Sven der Noorsman", "Sven van het Noorden"],
    "david": ["David der Dappere", "David van den Leeuw"],
    "tim": ["Tim der Schildknaap", "Tim van den Boog"],
    "joris": ["Joris de Drakenverslager", "Joris van den Burcht"],
    "ruud": ["Ruud van den Rijnstroom", "Ruud der Ridders"],
    "frank": ["Frank de Frankische", "Frank van den Velde"],
    "paul": ["Paul der Apostelen", "Paul van den Berg"],
    "martin": ["Martin de Strijder", "Martin van den Vrede"],
    "stefan": ["Stefan der Edelen", "Stefan van het Zuiden"],
    "michiel": ["Michiel de Aartsengel", "Michiel van den Woud"],
    "arjan": ["Arjan van den Stroom", "Arjan der Velden"],
    "wouter": ["Wouter van den Burg", "Wouter der Monniken"],
    "pieter": ["Pieter van Delft", "Pieter den Ouderling"],
    "nico": ["Nico van den Hoek", "Nico der Steden"],
    "rob": ["Rob van den Rots", "Rob der Schilden"],
    "erik": ["Erik der Noorsman", "Erik van het Noorden"],
    "bart": ["Bart van den Brugge", "Bart der Kooplieden"],
    "arno": ["Arno van den Aquila", "Arno de Adelaar"],
    "daan": ["Daan van den Rivier", "Daan der Vloten"],
    "tom": ["Tom van den Gronden", "Tom der Jagers"],
    "max": ["Max der Dapperen", "Max van den Berg"],
    "finn": ["Finn der Vikingen", "Finn van het Noorden"],
    "luca": ["Luca van den Zuiden", "Luca der Italianen"],
    "noah": ["Noah van den Arke", "Noah der Zalmen"],
    "sem": ["Sem van den Heuvel", "Sem der Koningen"],
    "luuk": ["Luuk van den Lichtenberg", "Luuk der Geneesheren"],
    "bram": ["Bram van den Venen", "Bram der Duinen"],
    "stijn": ["Stijn van den Steen", "Stijn der Bouwmeesters"],
    "milan": ["Milan van den Zuiden", "Milan der Edelen"],
    "thijs": ["Thijs van den Tijstroom", "Thijs der Geleerden"],
    "jasper": ["Jasper van den Jaspis", "Jasper der Koningen"],
    "emma": ["Emma van het Hof", "Emma der Edelvrouwen", "Emma de Schone"],
    "anna": ["Anna der Deugdzame", "Anna van den Bloementuin", "Anna de Heilige"],
    "maria": ["Maria der Genade", "Maria van den Hemel"],
    "lisa": ["Lisa van den Burcht", "Lisa der Schonen"],
    "lotte": ["Lotte van het Kasteel", "Lotte der Jonkvrouwen"],
    "nina": ["Nina der Edelvrouwe", "Nina van den Nacht"],
    "eva": ["Eva der Goedertierene", "Eva van den Paradijs"],
    "roos": ["Roos van den Gaarde", "Roos der Bloemen"],
    "laura": ["Laura van den Lauwerkrans", "Laura der Dichters"],
    "sofie": ["Sofie der Wijzen", "Sofie van den Licht"],
    "julia": ["Julia van den Zuiden", "Julia der Caesaren"],
    "mia": ["Mia van den Beemd", "Mia der Kleinen"],
    "nora": ["Nora van den Noord", "Nora der Edelvrouwen"],
    "sara": ["Sara van den Oudheid", "Sara der Koninginnen"],
    "hanna": ["Hanna van den Genade", "Hanna der Moederlijken"],
    "eline": ["Eline van den Elenboog", "Eline der Schonen"],
    "fleur": ["Fleur van den Bloemengaard", "Fleur der Bloemkransen"],
    "lies": ["Lies van den Liesbosch", "Lies der Deugdzamen"],
    "tessa": ["Tessa van den Tessalonike", "Tessa der Edelvrouwen"],
    "iris": ["Iris van den Regenboog", "Iris der Kleuren"],
    "lena": ["Lena van den Leen", "Lena der Rustigen"],
    "isa": ["Isa van den IJssel", "Isa der Kleinen"],
    "mila": ["Mila van den Zuiden", "Mila der Edelen"],
    "luna": ["Luna van den Maan", "Luna der Nacht"],
    "amber": ["Amber van den Barnsteen", "Amber der Goudkleuren"],
    "merel": ["Merel van den Merelbos", "Merel der Zangvogels"],
    "anouk": ["Anouk van den Ankou", "Anouk der Edelvrouwen"],
    "femke": ["Femke van den Fennen", "Femke der Friezen"],
    "marieke": ["Marieke van den Mariengaard", "Marieke der Deugdzamen"],
    "sanne": ["Sanne van den Zandvlakte", "Sanne der Schonen"],
    "esmee": ["Esmee van den Esdom", "Esmee der Jonkvrouwen"],
    "nathalie": ["Nathalie van den Natuur", "Nathalie der Geborenen"],
    "mieke": ["Mieke van den Miekelaard", "Mieke der Moederlijken"],
    "klara": ["Klara van den Licht", "Klara der Heldere"],
    "yara": ["Yara van den Oosten", "Yara der Dansenden"],
    "zoë": ["Zoë van den Leven", "Zoë der Grieken"],
    "fenna": ["Fenna van den Fen", "Fenna der Friezen"],
    "liesbeth": ["Liesbeth van den Liesbeek", "Liesbeth der Deugdzamen"],
    "hanneke": ["Hanneke van den Genade", "Hanneke der Kleinen"],
    "marianne": ["Marianne van den Marienhoven", "Marianne der Schonen"],
    "charlotte": ["Charlotte van den Charlemagne", "Charlotte der Edelen"],
    "olivia": ["Olivia van den Olijfberg", "Olivia der Schonen"],
}

# Phrase replacements (applied before word replacements)
MW_PHRASES = [
    # Greetings
    (r"hoe gaat het met jou", [
        "hoe vaert gij in deze duistere tijden van het rijk",
        "hoe is het gesteld met uw persoon in deze beroerde tijden",
        "hoe vaert gij, edele ziele, in het huidige tijdperk",
        "hoe staat het met uw welzijn in deze onstuimige tijden",
    ]),
    (r"hoe gaat het", [
        "hoe vaert gij in deze tijden",
        "hoe is het gesteld met uw welzijn",
        "hoe vaert gij, edele heer",
        "hoe staat het met u",
    ]),
    (r"hoe is het", [
        "hoe is het gesteld",
        "hoe bevindt gij u",
        "hoe staat de zaak ervoor",
    ]),
    (r"hallo|hoi|hey|hi\b", [
        "heil u, edele reiziger",
        "weest gegroet, doorluchtige heer",
        "God zij met u, edele ziele",
        "gegroet zij u, waardige heer",
        "heil en zegen, edele bezoeker",
    ]),
    (r"goedemorgen", [
        "weest gegroet in dezen vroegen dageraad",
        "een gezegend morgenlicht zij u gewenst",
        "de ochtenddauw begroet u, edele heer",
    ]),
    (r"goedemiddag", [
        "een gezegend middaguur zij u gewenst",
        "de middagzon beschijnt u, edele heer",
    ]),
    (r"goedenavond", [
        "een gezegend avonduur zij u toegewenst",
        "de avondster begroet u, edele heer",
        "de schemering valt neder, edele heer",
    ]),
    (r"goedenacht", [
        "een rustige nacht zij u gewenst",
        "de maan wacht over uw rust, edele heer",
    ]),
    (r"tot ziens", [
        "vaart wel, tot wij elkander wederom ontmoeten",
        "moge de Heer u geleiden tot ons wederzien",
        "vertrek in vrede, tot de wegen ons weder kruisen",
        "vaarwel, edele heer, tot de volgende ontmoeting",
    ]),
    (r"dank je wel|dank u wel|heel erg bedankt|bedankt|dank je|dank u", [
        "ick betuige u mijn innigste dankbaerheid",
        "mijn dank zij u diep verschuldigd, edele heer",
        "ick ben u ten zeerste erkentelijk",
        "de Almachtige moge u belonen voor uw grootmoedigheid",
    ]),
    (r"sorry|het spijt me|excuses", [
        "ick smeeke om vergiffenis voor mijn tekortkominge",
        "ick buig mij in diepe deemoed voor u neder",
        "vergeef mij, edele heer, mijn onwaardige handeling",
    ]),
    (r"ja\b", [
        "dit is waarachtig zoo",
        "voorwaar, het is zo",
        "ick beaam dit ten volle",
        "zoo is het inderdaad",
    ]),
    (r"nee\b", [
        "geenszins, dit kan niet worden toegestaan",
        "nimmermeer, dit is niet denkbaar",
        "bij de Almachtige, dit is geenszins waar",
    ]),
    # Common phrases
    (r"ik hou van jou|ik hou van je|ik houd van jou|ik houd van je", [
        "mijn hart brandt van de heilige liefde voor u",
        "ick bemin u met geheel mijn ziele en lichaam",
        "gij zijt de zon van mijn bestaan, edele vrouwe",
    ]),
    (r"ik mis je|ik mis jou", [
        "uw afwezigheid vervult mijn ziele met droefheid",
        "ick verlang ten zeerste naar uw aanwezigheid",
        "het gemis van uw persoon doet mij pijn in het hart",
    ]),
    (r"ik weet het niet", [
        "dit is mij een ondoorgrondelijk raadsel",
        "de kennis hieromtrent ontgaat mij ten ene male",
        "ick ben niet in staat dit te doorgronden",
    ]),
    (r"dat weet ik niet", [
        "de kennis hieromtrent is mij vreemd",
        "dit overstijgt mijn verstand",
    ]),
    (r"geen idee", [
        "dit is mij ten ene male onbekend",
        "hier tasten ook ick in het duister",
    ]),
    (r"wat is dat", [
        "wat voor wonderbaarlijk ding is dit",
        "welk merkwaardig verschijnsel is dit",
    ]),
    (r"heel goed|erg goed|super goed", [
        "uitmuntend en loffelijk",
        "voortreffelijk van kwaliteit",
        "edel en voortreffelijk",
    ]),
    (r"niet goed", [
        "geenszins loffelijk",
        "verre van voortreffelijk",
        "jammerlijk van kwaliteit",
    ]),
    (r"ik ga naar huis", [
        "ick begeef mij naar mijn eigen onderkomen",
        "ick trek terug naar mijn huys",
        "ick keer terug naar mijn eigen haard",
    ]),
    (r"ik ben thuis", [
        "ick bevinde mij ten huyze",
        "ick russe in mijn eigen onderkomen",
    ]),
    (r"hoe laat is het", [
        "welk uur wijst de zonnewijzer",
        "hoe staat de zon aan het uitspansel",
    ]),
    (r"wat is de tijd", [
        "welke tijde heeft het",
        "hoe laat is het uur",
    ]),
    (r"ik ben moe", [
        "ick ben afgemat van lijve en ziele",
        "de vermoeidheid heeft mij in haar greep",
        "mijn lichaam verlangt naar rust en slaap",
    ]),
    (r"ik ben ziek", [
        "de ziekte heeft mij geveld",
        "ick ben door kwaal en ziekte neergeslagen",
        "een vreemde kwaal teistert mijn lichaam",
    ]),
    (r"ik ben blij", [
        "ick ben verheugd van harte",
        "mijn ziele jubileert van vreugde",
        "een grote blijdschap vervult mijn gemoed",
    ]),
    (r"ik ben boos", [
        "de gramschap heeft mij bevangen",
        "ick ben vertoornd van gemoed",
        "mijn toorn weet geen grenzen",
    ]),
    (r"ik ben bang", [
        "de vrees heeft mij bevangen",
        "ick ben door schrik en vrees bevangen",
        "een grote angst heeft mij in haar greep",
    ]),
    (r"ik ben verdrietig|ik ben droevig", [
        "de droefheid heeft mij bevangen",
        "mijn ziele is diep bedroefd",
        "een groot verdriet drukt op mijn hart",
    ]),
    (r"ik heb honger", [
        "mijn maag knort van honger en armoede",
        "de honger kwelt mij",
        "ick verlang hevig naar het dagelijksche brood",
    ]),
    (r"ik heb dorst", [
        "de dorst teistert mijn keel",
        "ick verlang naar het klare water",
    ]),
    (r"het is mooi weer", [
        "de heilige zon beschijnt ons met haar welwillende stralen",
        "het hemelse licht baadt het land in gouden gloed",
    ]),
    (r"het is slecht weer|het regent|het waait", [
        "de hemelse wateren neerdalende teisteren het land",
        "de onstuimige storm woedt over het koninkrijck",
    ]),
    (r"er was eens", [
        "in de oude kronieken staat opgetekend dat",
        "in tijden van weleer",
        "zoals geschreven in de vergeten manuscripten",
    ]),
    (r"lang geleden", [
        "in de grijze oudheid",
        "in vervlogen tijden",
        "sedert mensenheugenis",
    ]),
]

# Random flavor injections for Medieval mode
MW_FLAVOR = [
    "in tijden van oude kronieken",
    "zoals geschreven in vergeten manuscripten",
    "onder het gezag van het koninklijk hof",
    "in naam van de doorluchtige vorst",
    "gelijk de oude oorkonden vermelden",
    "zoals overgeleverd door de eeuwen heen",
    "aldus staat geschreven in de grote annalen",
    "onder de bescherming van het rijk",
    "in het licht van de koninklijke gunst",
    "zoals de herauten van weleer verkondigden",
    "bij het licht van de waskaarsen",
    "in de schaduw van de kathedraal",
    "aan het hof van de doorluchtige vorst",
    "in het jaar des Heren",
    "zoals de monniken optekenden",
    "bij de gratie Gods",
    "onder het wapenschild van eer en trouwe",
    "in de tijden van ridderschap en eer",
    "zoals de kruisvaarders ons verkondigden",
    "bij de heilige relikwieën",
    "in het verborgene der kloostermuren",
    "op het slagveld der edelen",
    "in de kelders van het burchtslot",
    "aan de oever van de grote stroom",
    "bij het kraken van het ijs in de winter",
]

# Sentence expanders for Medieval mode
MW_EXPANDERS = [
    lambda s: f"Het zij allen bekend dat {s.lower()}, zo is het geschreven",
    lambda s: f"{s}, aldus staat geschreven in de koninklijke annalen",
    lambda s: f"Verneem en weet dat {s.lower()}, bij de gratie Gods",
    lambda s: f"{s}, naar het woord van de verheven vorst",
    lambda s: f"Weten zij die dit lezen: {s.lower()}, dit is de waarheid",
    lambda s: f"In naam van het koninkrijck: {s.lower()}",
    lambda s: f"{s}, zoals de oude kronieken vermelden",
    lambda s: f"De herauten verkondigen: {s.lower()}",
    lambda s: f"Zo spreekt de verheven vorst: {s.lower()}, en het zij zo",
    lambda s: f"{s}, hetgeen bij dezen officieel bekrachtigd wordt",
    lambda s: f"Hoor allen: {s.lower()}, in tijden van eer en ridderlijkheid",
    lambda s: f"{s}, want zo heeft de Almachtige het gewild",
]


# ════════════════════════════════════════════════════════════
#  PIRATE DICTIONARY
# ════════════════════════════════════════════════════════════

PI_PHRASES = [
    (r"hallo|hoi|hey|hi\b|goedemorgen|goedemiddag|goedenavond", [
        "Ahoy, ye scallywag",
        "Ahoy there, ye landlubber",
        "Well blow me down, ahoy",
        "Shiver me timbers, greetings",
    ]),
    (r"hoe gaat het|hoe is het", [
        "how be ye faring on these treacherous seas",
        "what manner of life do ye lead on the high seas",
        "how sails yer ship, ye old sea dog",
    ]),
    (r"tot ziens|doei|dag\b", [
        "may the winds carry ye safely, farewell",
        "sail away safely, ye sea dog",
        "may Davy Jones not claim ye, farewell",
        "until we meet again on the seven seas",
    ]),
    (r"dank je|dank u|bedankt", [
        "I be grateful, ye fine soul, arrr",
        "ye have me thanks, by Davy Jones",
        "a chest of gold to ye for yer kindness",
    ]),
    (r"sorry|het spijt me", [
        "I beg yer pardon, by Davy Jones' locker",
        "shiver me timbers, I apologize",
        "I walk the plank in shame",
    ]),
    (r"ja\b", ["Aye", "Aye aye, captain", "By me honour, aye"]),
    (r"nee\b", ["Nay", "Nay, blast ye", "Nay, by Davy Jones"]),
    (r"ik ben|ik ben", [
        "I be",
        "This old sea dog be",
        "Arrr, I be",
    ]),
    (r"ik ga", ["I sail forth", "I set course", "I navigate towards"]),
    (r"ik heb", ["I possess in me hold", "I have plundered", "In me treasure chest I have"]),
    (r"ik wil", ["I desire with all me pirate heart", "I crave"]),
    (r"ik hou van|ik houd van", [
        "me heart sings like a sea shanty for",
        "I would sail seven seas for",
        "me black heart beats only for",
    ]),
    (r"goed", ["worthy as a chest o' gold", "fine as a pirate's treasure"]),
    (r"slecht", ["as rotten as bilge water", "as foul as a cursed ship"]),
    (r"heel|erg|zeer", ["by Davy Jones", "shiver me timbers"]),
    (r"vandaag", ["this very tide", "on this fine pirate day"]),
    (r"morgen\b", ["when the sun rises o'er the horizon", "on the morrow's tide"]),
    (r"gisteren", ["on the last tide", "when the moon last set"]),
]

PI_FLAVOR = [
    "by Davy Jones' locker",
    "shiver me timbers",
    "as the seas be me witness",
    "on the seven seas",
    "or I'll walk the plank",
    "blow me down",
    "as me father Blackbeard once said",
    "arrr",
    "by the code of the pirates",
    "on me honour as a buccaneer",
    "as any pirate worth his salt knows",
    "by the kraken's tentacles",
    "yo ho ho",
    "curse ye, Davy Jones",
    "by the Flying Dutchman",
]

PI_EXPANDERS = [
    lambda s: f"{s}, arrr",
    lambda s: f"Hear me, {s.lower()}, or walk the plank",
    lambda s: f"{s}, by the code of the pirates",
    lambda s: f"Blast yer eyes, {s.lower()}, arrr",
    lambda s: f"{s}, on me honour as a buccaneer",
    lambda s: f"Avast ye! {s}, ye scallywag",
    lambda s: f"{s}, shiver me timbers",
    lambda s: f"By Davy Jones, {s.lower()}, arrr",
]


# ════════════════════════════════════════════════════════════
#  OLD EGYPT DICTIONARY
# ════════════════════════════════════════════════════════════

EG_PHRASES = [
    (r"hallo|hoi|hey|hi\b|goedemorgen|goedemiddag|goedenavond", [
        "May Ra's light shine upon thee, traveller",
        "Greetings, humble servant of the Nile",
        "The gods smile upon thine arrival",
        "Blessed be thy presence before the great pharaoh",
    ]),
    (r"hoe gaat het|hoe is het", [
        "how doth the great Nile flow through thy life",
        "how art thou blessed by the eternal Ra",
        "doth Ra shine favourably upon thy days",
    ]),
    (r"tot ziens|doei|dag\b", [
        "may Osiris guide thy path until we meet again",
        "may Ra illuminate thy journey",
        "go in peace, guided by the gods",
        "may Anubis keep thee safe on thy journey",
    ]),
    (r"dank je|dank u|bedankt", [
        "the gods smile upon thy generosity",
        "may Ra reward thy kindness",
        "thou art as generous as the Nile in flood",
    ]),
    (r"sorry|het spijt me", [
        "I prostrate myself before thee in humble apology",
        "by the scales of Ma'at, I beg forgiveness",
        "I offer this humble apology upon the altar of Ma'at",
    ]),
    (r"ja\b", [
        "It is written, so it shall be",
        "By the will of Ra, it is so",
        "The gods decree it",
    ]),
    (r"nee\b", [
        "By the scales of Ma'at, this cannot be so",
        "The gods forbid it",
        "Nay, this is against the sacred order",
    ]),
    (r"ik ben", ["I, servant of the gods, am", "By Ra's grace, I am", "The pharaoh's humble servant is"]),
    (r"ik ga", ["I journey forth along the sacred Nile", "I walk the path of Ra"]),
    (r"ik heb", ["In my possession, blessed by the gods, lies", "By Ra's grace, I possess"]),
    (r"ik wil", ["It is the will of the gods that I", "My soul, guided by Ra, desires"]),
    (r"ik hou van|ik houd van", [
        "my heart, like the eternal Nile, flows to",
        "by the love of Isis and Osiris, I cherish",
    ]),
    (r"goed", ["blessed by Ra", "worthy of the pharaoh's favour"]),
    (r"slecht", ["cursed by Set", "against the sacred order of Ma'at"]),
    (r"groot", ["mighty as the pyramid of Giza", "as vast as the desert"]),
    (r"vandaag", ["on this sacred day", "under Ra's watchful eye today"]),
    (r"morgen\b", ["when Ra rises once more", "on the next sacred dawn"]),
]

EG_FLAVOR = [
    "as it is written in the Book of the Dead",
    "blessed by the eternal Ra",
    "by the will of the pharaoh",
    "as the Nile flows eternal",
    "in the name of Osiris and Isis",
    "since the time of the first pharaohs",
    "as the hieroglyphs foretold",
    "under the watching eye of Horus",
    "by the sacred scarab",
    "as inscribed on the walls of Karnak",
    "by the grace of Amun-Ra",
    "as the desert sands remember",
    "in the shadow of the great pyramid",
    "by the power of the ankh",
]

EG_EXPANDERS = [
    lambda s: f"By the will of the pharaoh, {s.lower()}",
    lambda s: f"{s}, as it has been written in stone for eternity",
    lambda s: f"The gods decree: {s.lower()}",
    lambda s: f"{s}, thus spoke the high priest of Amun",
    lambda s: f"Know ye all that {s.lower()}, by Ra's sacred light",
    lambda s: f"The eternal Nile witnesses: {s.lower()}",
    lambda s: f"{s}, as the hieroglyphs foretold",
    lambda s: f"Horus watches as {s.lower()}, glory to Ra",
]


# ════════════════════════════════════════════════════════════
#  SHAKESPEARE DICTIONARY
# ════════════════════════════════════════════════════════════

SH_PHRASES = [
    (r"hallo|hoi|hey|hi\b|goedemorgen|goedemiddag|goedenavond", [
        "Hark, good fellow, well met indeed",
        "What ho, good sir, well met",
        "God give ye good morrow, gentle sir",
        "Hark! Who goes there? Well met, good fellow",
    ]),
    (r"hoe gaat het|hoe is het", [
        "how dost thou fare in these troubled times",
        "what manner of day hath Fortune bestowed upon thee",
        "how fares thy noble spirit",
    ]),
    (r"tot ziens|doei|dag\b", [
        "fare thee well, till we meet again",
        "parting is such sweet sorrow, fare thee well",
        "till we meet again, fare thee well, good sir",
        "God speed thee on thy way, gentle sir",
    ]),
    (r"dank je|dank u|bedankt", [
        "I am most heartily in thy debt, good sir",
        "thou hast my deepest and most humble gratitude",
        "I doth thank thee from the bottom of mine heart",
    ]),
    (r"sorry|het spijt me", [
        "I doth most humbly beseech thy forgiveness",
        "forgive me, gentle soul, this grievous error",
        "I prostrate myself before thee in shame",
    ]),
    (r"ja\b", ["Aye, verily", "Indeed, forsooth", "By my troth, aye"]),
    (r"nee\b", ["Nay, forsooth", "Nay, by my honour", "Nay, I doth protest"]),
    (r"ik ben", ["I doth be", "Methinks I am", "I, poor wretch, am"]),
    (r"ik ga", ["I doth make haste", "I take my leave", "I doth depart"]),
    (r"ik heb", ["I doth possess", "Mine own hands hold", "I have in my keeping"]),
    (r"ik wil", ["It is mine earnest desire", "My heart doth yearn", "I doth wish with all mine heart"]),
    (r"ik hou van|ik houd van", [
        "mine heart doth overflow with love for",
        "what light is this? It is mine love for",
        "shall I compare thee to a summer's day? For I love",
    ]),
    (r"goed", ["most virtuous and fine", "of noble quality", "worthy of the highest praise"]),
    (r"slecht", ["most vile and wretched", "as foul as a villain's heart", "of the basest quality"]),
    (r"groot", ["of most magnificent proportion", "as great as Caesar himself"]),
    (r"vandaag", ["on this very day", "this very day that Fortune hath given us"]),
    (r"morgen\b", ["when the morning sun doth rise", "on the morrow"]),
    (r"gisteren", ["on the day that hath passed", "yesterday, that sorry day"]),
    (r"maar", ["yet", "howbeit", "withal"]),
    (r"niet\b", ["doth not", "doth ne'er"]),
    (r"heel|erg|zeer", ["most", "exceeding", "passing"]),
]

SH_FLAVOR = [
    "methinks",
    "forsooth",
    "by my troth",
    "hark what I say",
    "as the Bard himself would say",
    "by the grace of heaven",
    "as all the world's a stage",
    "to be or not to be, that is the question",
    "by mine honour",
    "as Fortune would have it",
    "as the stars decree",
    "by sweet heaven",
    "as Romeo once said",
    "in the name of all that is noble",
]

SH_EXPANDERS = [
    lambda s: f"Hark! {s}, methinks",
    lambda s: f"{s}, methinks 'tis true",
    lambda s: f"What light is this? {s.lower()}, by my troth",
    lambda s: f"{s}, by mine honour and my sword",
    lambda s: f"Hear ye, hear ye: {s.lower()}, forsooth",
    lambda s: f"{s}, thus spake the wise man of Avon",
    lambda s: f"All the world's a stage, and {s.lower()}",
    lambda s: f"{s}, as Fortune herself would have it",
]


# ════════════════════════════════════════════════════════════
#  TRANSLATION ENGINE
# ════════════════════════════════════════════════════════════

def apply_phrases(text, phrases):
    """Apply phrase replacements with random variation."""
    for pattern, replacements in phrases:
        def replace_match(m):
            return random.choice(replacements)
        text = re.sub(pattern, replace_match, text, flags=re.IGNORECASE)
    return text


def apply_word_dict(text, word_dict):
    """Apply word-by-word replacements with random variation."""
    words = text.split()
    result = []
    for word in words:
        clean = re.sub(r"[^a-zA-ZÀ-ÿ]", "", word.lower())
        suffix = re.sub(r"[a-zA-ZÀ-ÿ]", "", word)
        if clean in word_dict:
            choices = word_dict[clean]
            replacement = random.choice(choices) if isinstance(choices, list) else choices
            # Preserve capitalisation
            if word[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            result.append(replacement + suffix)
        else:
            result.append(word)
    return " ".join(result)


def apply_names(text, name_dict):
    """Replace known first names with medieval versions."""
    for name, variants in name_dict.items():
        pattern = r"\b" + re.escape(name) + r"\b"
        def replacer(m):
            return random.choice(variants)
        text = re.sub(pattern, replacer, text, flags=re.IGNORECASE)
    return text


def expand_sentences(text, expanders, flavor_list, expand_chance=0.9, flavor_chance=0.6):
    """Expand each sentence using random expanders and flavor injections."""
    sentences = re.findall(r"[^.!?]+[.!?]*", text)
    if not sentences:
        sentences = [text]
    result_parts = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        # Strip trailing punctuation
        punct_match = re.search(r"[.!?]+$", sentence)
        punct = punct_match.group() if punct_match else "."
        base = re.sub(r"[.!?]+$", "", sentence).strip()
        if not base:
            continue
        # Apply expander
        if random.random() < expand_chance and expanders:
            expanded = random.choice(expanders)(base)
        else:
            expanded = base
        # Inject flavor
        if random.random() < flavor_chance and flavor_list:
            flavor = random.choice(flavor_list)
            expanded += f". {flavor[0].upper()}{flavor[1:]}"
        # Clean up
        expanded = expanded[0].upper() + expanded[1:] if expanded else expanded
        if not re.search(r"[.!?]$", expanded):
            expanded += "."
        result_parts.append(expanded)
    return " ".join(result_parts)


def translate(text, mode):
    """Main translation function."""
    if not text.strip():
        return "Schrijf eerst tekst..."

    if mode == "Medieval":
        text = apply_phrases(text, MW_PHRASES)
        text = apply_names(text, MW_NAMES)
        text = apply_word_dict(text, MW_WORDS)
        text = expand_sentences(text, MW_EXPANDERS, MW_FLAVOR)

    elif mode == "Pirate":
        text = apply_phrases(text, PI_PHRASES)
        text = expand_sentences(text, PI_EXPANDERS, PI_FLAVOR)

    elif mode == "Old Egypt":
        text = apply_phrases(text, EG_PHRASES)
        text = expand_sentences(text, EG_EXPANDERS, EG_FLAVOR)

    elif mode == "Shakespeare":
        text = apply_phrases(text, SH_PHRASES)
        text = expand_sentences(text, SH_EXPANDERS, SH_FLAVOR)

    return text


# ════════════════════════════════════════════════════════════
#  KIVY UI
# ════════════════════════════════════════════════════════════

GOLD = (0.78, 0.59, 0.12, 1)
GOLD_DIM = (0.47, 0.36, 0.08, 1)
DARK_BG = (0.08, 0.06, 0.03, 1)
PANEL_BG = (0.13, 0.09, 0.04, 1)
BORDER = (0.35, 0.24, 0.06, 1)
TEXT_GOLD = (0.85, 0.70, 0.30, 1)
TEXT_DIM = (0.55, 0.42, 0.18, 1)


class DarkPanel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*PANEL_BG)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6])
            Color(*BORDER)
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6])
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border_rect.pos = (self.pos[0] - 1, self.pos[1] - 1)
        self.border_rect.size = (self.size[0] + 2, self.size[1] + 2)


class ModeButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0.14, 0.10, 0.04, 1)
        self.color = TEXT_DIM
        self.font_size = "14sp"
        self.bold = False
        self.size_hint_y = None
        self.height = 38

    def set_active(self, active):
        if active:
            self.background_color = (0.30, 0.20, 0.05, 1)
            self.color = GOLD
            self.bold = True
        else:
            self.background_color = (0.14, 0.10, 0.04, 1)
            self.color = TEXT_DIM
            self.bold = False


class AncientTranslatorApp(App):
    def build(self):
        self.title = "⚔  Ancient Translator  ⚔"
        self.mode = "Medieval"
        self.mode_buttons = {}

        root = BoxLayout(orientation="vertical", padding=16, spacing=10)
        root.canvas.before.add(Color(*DARK_BG))
        self._bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.canvas.before.add(self._bg_rect)
        root.bind(pos=self._upd_bg, size=self._upd_bg)

        # ── Header ──
        header = Label(
            text="⚔   Ancient Translator   ⚔",
            font_size="22sp",
            color=GOLD,
            bold=True,
            size_hint_y=None,
            height=40,
        )
        root.add_widget(header)

        sub = Label(
            text="Volledig offline · geen internet vereist",
            font_size="12sp",
            color=TEXT_DIM,
            size_hint_y=None,
            height=20,
        )
        root.add_widget(sub)

        # ── Mode buttons ──
        mode_row = GridLayout(
            cols=4, spacing=6, size_hint_y=None, height=42
        )
        modes = [
            ("⚔  Medieval", "Medieval"),
            ("☠  Pirate", "Pirate"),
            ("𓂀  Old Egypt", "Old Egypt"),
            ("✒  Shakespeare", "Shakespeare"),
        ]
        for label, key in modes:
            btn = ModeButton(text=label)
            btn.bind(on_press=lambda b, k=key: self.set_mode(k))
            self.mode_buttons[key] = btn
            mode_row.add_widget(btn)
        self.mode_buttons["Medieval"].set_active(True)
        root.add_widget(mode_row)

        # ── Text areas ──
        text_row = BoxLayout(orientation="horizontal", spacing=10)

        # Input
        in_box = BoxLayout(orientation="vertical", spacing=6)
        in_label = Label(
            text="Invoer", font_size="13sp", color=GOLD,
            size_hint_y=None, height=22, bold=True
        )
        in_box.add_widget(in_label)
        self.input_box = TextInput(
            hint_text="Type hier je tekst...",
            multiline=True,
            background_color=PANEL_BG,
            foreground_color=TEXT_GOLD,
            cursor_color=GOLD,
            font_size="15sp",
        )
        in_box.add_widget(self.input_box)
        text_row.add_widget(in_box)

        # Output
        out_box = BoxLayout(orientation="vertical", spacing=6)
        out_label = Label(
            text="Vertaling", font_size="13sp", color=GOLD,
            size_hint_y=None, height=22, bold=True
        )
        out_box.add_widget(out_label)
        self.output_box = TextInput(
            hint_text="De vertaling verschijnt hier...",
            multiline=True,
            readonly=True,
            background_color=PANEL_BG,
            foreground_color=(0.92, 0.78, 0.40, 1),
            font_size="15sp",
        )
        out_box.add_widget(self.output_box)
        text_row.add_widget(out_box)
        root.add_widget(text_row)

        # ── Buttons row ──
        btn_row = BoxLayout(
            orientation="horizontal", spacing=10,
            size_hint_y=None, height=46
        )

        translate_btn = Button(
            text="⚔   Vertaal   ⚔",
            font_size="16sp",
            bold=True,
            background_normal="",
            background_color=(0.30, 0.20, 0.05, 1),
            color=GOLD,
        )
        translate_btn.bind(on_press=self.do_translate)
        btn_row.add_widget(translate_btn)

        clear_btn = Button(
            text="Wissen",
            font_size="14sp",
            size_hint_x=0.25,
            background_normal="",
            background_color=(0.18, 0.12, 0.04, 1),
            color=TEXT_DIM,
        )
        clear_btn.bind(on_press=self.do_clear)
        btn_row.add_widget(clear_btn)

        root.add_widget(btn_row)

        # ── Stats ──
        self.stats_label = Label(
            text="Woorden in: 0  |  Woorden uit: 0  |  Uitbreiding: —",
            font_size="11sp",
            color=TEXT_DIM,
            size_hint_y=None,
            height=22,
        )
        root.add_widget(self.stats_label)

        return root

    def _upd_bg(self, instance, value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size

    def set_mode(self, mode):
        self.mode = mode
        for key, btn in self.mode_buttons.items():
            btn.set_active(key == mode)

    def do_translate(self, instance):
        text = self.input_box.text.strip()
        if not text:
            self.output_box.text = "Schrijf eerst tekst in het invoerveld..."
            return
        result = translate(text, self.mode)
        self.output_box.text = result
        iw = len(text.split())
        ow = len(result.split())
        ratio = f"{ow/iw:.1f}x" if iw > 0 else "—"
        self.stats_label.text = (
            f"Woorden in: {iw}  |  Woorden uit: {ow}  |  Uitbreiding: {ratio}"
        )

    def do_clear(self, instance):
        self.input_box.text = ""
        self.output_box.text = ""
        self.stats_label.text = "Woorden in: 0  |  Woorden uit: 0  |  Uitbreiding: —"


if __name__ == "__main__":
    AncientTranslatorApp().run()
