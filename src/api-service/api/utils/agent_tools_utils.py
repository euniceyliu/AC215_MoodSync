from vertexai.generative_models import FunctionDeclaration, Tool, Part

ARTISTS = [
    "Kendrick-lamar",
    "A-ap-rocky",
    "Rich-the-kid",
    "Pusha-t",
    "Sob-x-rbe",
    "Ab-soul",
    "Rick-ross",
    "50-cent",
    "Danny-brown",
    "Mike-will-made-it",
    "Yg",
    "Robin-thicke",
    "Jay-rock",
    "Sir",
    "Trae-tha-truth",
    "Rapsody",
    "Big-sean",
    "Bj-the-chicago-kid",
    "Casey-veggies",
    "9th-wonder",
    "Mann",
    "Punch",
    "Eminem",
    "Dr-dre",
    "Lil-wayne",
    "Rihanna",
    "Slaughterhouse",
    "D12",
    "Skylar-grey",
    "Obie-trice",
    "Outsidaz",
    "Drake",
    "Nicki-minaj",
    "2-chainz",
    "Meek-mill",
    "Blocboy-jb",
    "Ilovemakonnen",
    "Kanye-west",
    "Dave",
    "Majid-jordan",
    "Dj-drama",
    "Young-money",
    "Nickelus-f",
    "Jay-z-and-kanye-west",
    "Kanye-west-chief-keef-pusha-t-big-sean-and-jadakiss",
    "Kanye-west-pusha-t-and-ghostface-killah",
    "Travis-scott",
    "Kanye-west-pusha-t-common-2-chainz-cyhi-the-prynce-kid-cudi-and-dbanj",
    "Ynw-melly",
    "Francis-and-the-lights",
    "Talib-kweli",
    "Nas",
    "Teyana-taylor",
    "Cyhi-the-prynce",
    "Common",
    "Consequence",
    "The-world-famous-tony-williams",
    "A-ap-ferg",
    "G-eazy",
    "Selena-gomez",
    "A-ap-mob",
    "Theophilus-london",
    "The-black-eyed-peas",
    "Tinashe",
    "Dram",
    "Big-boi",
    "Clams-casino",
    "A-ap-twelvyy",
    "Vic-mensa",
    "J-cole",
    "Miguel",
    "Logic",
    "Diddy-dirty-money",
    "Bas-and-j-cole",
    "Dj-khaled",
    "Bas",
    "Cozz",
    "Moneybagg-yo",
    "Xxxtentacion",
    "Lil-peep-and-xxxtentacion",
    "Rich-brian-keith-ape-and-xxxtentacion",
    "Yaprak-asimov",
    "Chance-the-rapper",
    "Snakehips",
    "Childish-gambino",
    "Sza",
    "Taylor-bennett",
    "Kyle",
    "Mapei",
    "Supa-bwe",
    "Skrillex",
    "John-legend",
    "Probcause",
    "Nosaj-thing",
    "Odd-couple",
    "G-herbo",
    "Alex-wiley",
    "Sir-michael-rocks",
    "Rock-genius",
    "Tee-grizzley",
    "Billboard",
    "Kembe-x",
    "Trinidad-james",
    "Jeezy",
    "Jadakiss",
    "Nas-and-michael-kiwanuka",
    "Sway-in-the-morning",
    "Zedd",
    "Tyler-thomas",
    "Big-lenbo",
    "Jhene-aiko",
    "Yc",
    "Dj-mo-beatz",
    "Kash-doll",
    "French-montana",
    "The-weeknd",
    "Beyonce",
    "Ricky-hil",
    "Trouble",
    "Joey-bada",
    "Pro-era",
    "Dyme-a-duzin",
    "Capital-steez",
    "Statik-selektah",
    "Tyler-the-creator",
    "Odd-future",
    "Kali-uchis",
    "Mac-miller",
    "Domo-genesis",
    "Schoolboy-q",
    "Anderson-paak",
    "Freddie-gibbs-and-madlib",
    "Lil-wayne-and-charlie-puth",
    "Bebe-rexha",
    "Ti",
    "Ace-hood",
    "Ty-dolla-sign",
    "Playaz-circle",
    "Wifisfuneral",
    "Dae-dae",
    "Dame-dolla",
    "Fabolous",
    "Paris-hilton",
    "Erykah-badu",
    "Wiz-khalifa",
    "Chief-keef",
    "Sean-kingston",
    "Machine-gun-kelly",
    "Jojo",
    "24hrs",
    "Tove-lo",
    "Iggy-azalea",
    "Alex-da-kid",
    "Raven-felix",
    "They",
    "Ne-yo",
    "Caye",
    "Boaz",
    "Jay-z",
    "Kris-wu",
    "Major-lazer",
    "Steve-aoki",
    "Juicy-j",
    "Belly",
    "Migos",
    "Tory-lanez",
    "Jaye",
    "Smoke-dza",
    "Linkin-park",
    "Clipse",
    "Birdman",
    "Que",
    "Yogi",
    "Moxie-raia",
    "Hit-boy",
    "Desiigner",
    "Nore",
    "Benny-the-butcher",
    "Pusha-t-and-jeremih",
    "Re-up-gang",
    "Yo-gotti",
    "Jason-derulo",
    "Calvin-harris",
    "Curren-y",
    "B-smyth",
    "Jack-u",
    "Jay-park",
    "Don-q-and-a-boogie-wit-da-hoodie",
    "Robert-greene",
    "Snoop-lion",
    "Tha-dogg-pound",
    "21-savage-and-metro-boomin",
    "Rocko",
    "Future",
    "6lack",
    "Vince-staples",
    "Bad-meets-evil",
    "Shady-records",
    "Kehlani",
    "The-game",
    "Lil-durk",
    "Big-krit",
    "Ariana-grande-and-victoria-monet",
    "Ariana-grande-and-social-house",
    "Ariana-grande",
    "Bia-and-ariana-grande",
    "Who-is-fancy",
    "Billie-eilish",
    "Kid-cudi",
    "Nav",
    "Kid-ink",
    "Sadek",
    "Wale",
    "Waka-flocka-flame",
    "Eric-bellinger",
    "Black-cobain",
    "Chevralet-ss",
    "Anne-marie",
    "Ed-sheeran",
    "Post-malone",
    "Colonel-loud",
    "Hustle-gang",
    "E-40",
    "K-camp",
    "Omarion",
    "Jaden",
    "Carnage",
    "Madeintyo",
    "X-ambassadors",
    "Machine-gun-kelly-and-camila-cabello",
    "Lupe-fiasco",
    "Dee-1",
    "Playboi-carti",
    "Lil-uzi-vert",
    "Juice-wrld",
    "Moosh-and-twist",
    "Lil-peep-and-ilovemakonnen",
    "Watsky",
    "Eve",
    "Hittman",
    "2pac",
    "Funkmaster-flex",
    "Ra-the-rugged-man",
    "Rittz",
    "Tech-n9ne",
    "Ill-bill",
    "Panic-at-the-disco",
    "Kilo-kish",
    "Original-broadway-cast-of-hamilton",
    "Lin-manuel-miranda",
    "Marc-e-bassy",
    "Marty-grimes",
    "Genius",
    "Lil-yachty",
    "Yfn-lucci",
    "Luis-fonsi-and-daddy-yankee",
    "Justin-bieber",
    "Skrillex-justin-bieber-and-diplo",
    "Poo-bear",
    "Uicideboy",
    "Bexey",
    "Doja-cat",
    "Usher",
    "Bilal",
    "Dave-east",
    "Rita-ora",
    "Zoey-dollaz",
    "Trey-songz",
    "Lil-mosey-and-chris-brown",
    "Skeme",
    "Zendaya",
    "Chris-brown",
    "Jacquees",
    "Brns",
    "Pharaoh-and-boulevard-depo",
    "Pharaoh",
    "Sheek-louch",
    "Diddy",
    "Fast-food-music",
    "Joyner-lucas",
    "Jarren-benton",
    "Jedi-mind-tricks",
    "Demigodz",
    "Block-mccloud",
    "Hell-razah",
    "Czarface",
    "Trip-lee",
    "Lecrae",
    "Andy-mineo",
    "Kb",
    "Xvxx",
    "Kevin-gates",
    "Big-l",
    "Gang-starr",
    "La-coka-nostra",
    "Jon-connor",
    "Chris-webby",
    "Soko-i-marysia-starosta",
    "Dizzy-wright",
    "Kyle-and-mr-man",
    "The-chainsmokers",
    "Tory-lanez-and-rich-the-kid",
    "Dosseh",
    "Michael-jackson",
    "Far-east-movement",
    "Riff-raff",
    "Jazzy-bazz",
    "Wicca-phase-springs-eternal",
    "Lil-b",
    "Damso",
    "Krisy",
    "Amine",
    "Cj-fly",
    "Jessie-reyez-and-6lack",
    "Bea-miller-and-6lack",
    "Jid",
    "Alessia-cara",
    "Pouya",
    "Plies",
    "Jeremih",
    "Valee",
    "Drop-city-yacht-club",
    "Nick-cannon",
    "Dj-luke-nasty",
    "Goldlink",
    "Vald",
    "Alkpote",
    "Uncle-murda",
    "Machine-gun-kelly-yungblud-and-travis-barker",
    "Knaan",
    "Cee",
    "Funk-volume",
    "Prince-ea",
    "Lotus-eater-evans",
    "Mr-muthafuckin-exquire",
    "A-trak",
    "Vampire-weekend",
    "Heems",
    "Catch-lungs",
    "Hurricane-chris",
    "Hs87",
    "Fall-out-boy",
    "Chief-keef-and-riff-raff",
    "Raury",
    "Kenneth-whalum",
    "Tha-joker-us",
    "Ski-mask-the-slump-god",
    "Joji",
    "Lil-toe",
    "Berner",
    "Mustard",
    "The-dream",
    "Fabolous-and-jadakiss",
    "Bet",
    "Stefflon-don",
    "Gashi",
    "Keyshia-cole",
    "Prettymuch",
    "Gucci-mane",
    "Kaaris",
    "Cashmere-cat",
    "Benny-blanco-tainy-selena-gomez-and-j-balvin",
    "Various-artists",
    "Action-bronson",
    "Willie-the-kid",
    "The-1975",
    "Wu-tang-clan",
    "Gza",
    "Raekwon",
    "A-f-r-o",
    "Rza",
    "Prhyme",
    "Royce-da-59",
    "Joe-budden",
    "Pharoahe-monch",
    "D-k-king-doka",
    "Nico-and-vinz",
    "Jr-castro",
    "Reflection-eternal",
    "Evidence",
    "Rico-love",
    "Sahbabii",
    "Yelawolf",
    "Da-mafia-6ix",
    "Young-thug",
    "Ralo",
    "Yungblud-and-halsey",
    "Kold",
    "Lorde",
    "Broods",
    "Bryson-tiller",
    "Sy-ari-da-kid",
    "Brockhampton",
    "The-notorious-big",
    "Big-pun",
    "The-lox",
    "Troye-sivan",
    "Lauv-and-troye-sivan",
    "Charli-xcx-and-troye-sivan",
    "Flatbush-zombies",
    "Gramz",
    "Cash-cash",
    "Busta-rhymes",
    "Dreams-divided",
    "Denzel-curry",
    "Deniro-farrar",
    "Yung-simmie",
    "Sdotbraddy",
    "Tyga",
    "Nf",
    "Pardison-fontaine",
    "City-girls",
    "Cardi-b",
    "Trippie-redd",
    "Isaiah-rashad",
    "Imagine-dragons",
    "Kent-jones",
    "Bones",
    "Idk",
    "Mf-doom",
    "Nyck-caution",
    "Immortal-technique",
    "Kids-these-days",
    "Eripe-x-quebonafide",
    "Quebonafide",
    "Quebonafide-x-cywil-x-tomb",
    "Quebonafide-soko-pro8l3m",
    "Rose",
    "Rap-genius-polska",
    "Te-tris-and-pogz",
    "Khalid",
    "Bhad-bhabie",
    "Social-house",
    "Charli-xcx",
    "Nexxthursday",
    "Kodie-shane",
    "Cousin-stizz",
    "Rae-sremmurd",
    "Three-6-mafia",
    "Why-dont-we",
    "Partynextdoor",
    "Dj-scream",
    "Johnny-cash",
    "System-of-a-down",
    "Red-hot-chili-peppers",
    "Beastie-boys",
    "Slayer",
    "Tom-petty",
    "Ll-cool-j",
    "Dixie-chicks",
    "Damien-rice",
    "Metallica",
    "T-la-rock-and-jazzy-jay",
    "Angus-and-julia-stone",
    "Offset-and-metro-boomin",
    "Offset",
    "At-wendys",
    "Honors-english",
    "Booba",
    "Kalash",
    "Christine-and-the-queens",
    "Shay",
    "Benash",
    "Outkast",
    "Big-grams",
    "Trick-daddy",
    "Jet-life",
    "Eric-b-and-rakim",
    "Nice-peter",
    "Watsky-and-mody",
    "Maxo-kream",
    "Rich-brian",
    "5-seconds-of-summer",
    "Russ",
    "Pnb-rock",
    "Macklemore-and-ryan-lewis",
    "Miley-cyrus",
    "Rich-boy",
    "Ghostface-killah",
    "Lil-skies",
    "Yung-bans",
    "Gnar",
    "Nekfeu",
    "Lino",
    "Nakk-mendosa",
    "Deen-burbigo",
    "Fixpen-sill",
    "Kranium",
    "Roy-woods",
    "Buddy",
    "Ashanti",
    "Lil-duval",
    "Jr",
    "Boogie-down-productions",
    "Cheat-codes",
    "Demi-lovato",
    "Azealia-banks",
    "A-boogie-wit-da-hoodie",
    "Dreezy",
    "22gz",
    "Sia",
    "Blackbear",
    "Jeremy-zucker",
    "Mike-shinoda",
    "Young-dolph",
    "Nick-jonas",
    "Davido",
    "Sofiane",
    "Kery-james",
    "Biffty",
    "Yasiin-bey",
    "The-roots",
    "Rap-genius",
    "Lil-dicky",
    "Ayo-jay",
    "Fetty-wap",
    "Cl",
    "Mick-jenkins",
    "Hurt-everybody",
    "Dua-lipa",
    "Sean-paul",
    "A-tribe-called-quest",
    "Del-the-funky-homosapien-and-aesop-rock",
    "Murs",
    "Mayday-x-murs",
    "The-grouch",
    "Lil-xan",
    "Boulevard-depo",
    "Gera-pkhat",
    "Krestall-courier",
    "Laud",
    "I61",
    "Scarlxrd",
    "A-boogie-wit-da-hoodie-and-don-q",
    "Ally-brooke",
    "R-kelly",
    "The-isley-brothers",
    "Ellie-goulding",
    "Sean-price",
    "Rejjie-snow",
    "Hoodie-allen",
    "Chelsea-cutler",
    "Taco-hemingway",
    "Britney-spears",
    "Youngboy-never-broke-again",
    "Bring-me-the-horizon",
    "Danny-ocean",
    "Benny-benassi",
    "Cal-chuchesta",
    "Anthony-fantano",
    "The-cool-kids",
    "Luke-christopher",
    "Asher-roth",
    "Marshmello-and-anne-marie",
    "Hodgy",
    "Nipsey-hussle",
    "Kirk-knight",
    "Dessy-hinds",
    "Julia-michaels",
    "Madison-beer",
    "L-devine",
    "Earthgang",
    "B-horowitz",
    "Pnl",
    "Black-thought",
    "M",
    "Poppy",
    "Emeli-sande",
    "Aaliyah",
    "Empire-cast",
    "Rockie-fresh",
    "D-why",
    "Lloyd",
    "Token",
    "Big-daddy-kane",
    "Boots",
    "Daniel-caesar",
    "Niall-horan",
    "Tede",
    "Sitek",
    "William",
    "Noname",
    "Pouya-and-fat-nick",
    "Smokepurpp",
    "Smokepurpp-and-murda-beatz",
    "Rich-homie-quan",
    "Ella-mai",
    "Polo-g",
    "Jay-critch",
    "Rich-the-kid-and-ybn-almighty-jay",
    "Snow-tha-product",
    "Banks",
    "The-underachievers",
    "Avril-lavigne",
    "Kevin-abstract",
    "Sensei",
    "Andy-mineo-and-wordsplayed",
    "For-king-and-country",
    "Maroon-5",
    "Hozier",
    "Niro",
    "Hopsin",
    "Portugal-the-man",
    "The-purist",
    "Dwa-sawy",
    "Fen",
    "88rising-and-rich-brian",
    "Mz",
    "88glam",
]

# Specify a function declaration and parameters for an API request
get_chunk_by_filters_func = FunctionDeclaration(
    name="get_chunk_by_filters",
    description="Get the chunks filtered by artist name and/or music genre",
    # Function parameters are specified in OpenAPI JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "artist": {
                "type": "string",
                "description": """The artist name. If no
                        artist specified, use None.""",
                "enum": [
                    "Kehlani",
                    "Rihanna",
                    "Beyonce",
                    "None",
                    "Anderson-paak",
                    "Jhene-aiko",
                    "Zedd",
                    "Selena-gomez",
                    "Khalid",
                    "Bruno-mars",
                ],
            },  # need to incorporate full list of artists
            "tag": {
                "type": "string",
                "description": """The genre of music requested.
                    If no genre specified, use None.""",
                "enum": ["R&B", "Pop", "Rock", "Rap", "Ballad", "None", "EDM"],
            },  # replace with full list of genres
            "search_content": {
                "type": "string",
                "description": """Term describing the user's mood,
                state of mind, or type of playlist requested. Ensure
                that the search content is at least one word.""",
            },
        },
        "required": ["artist", "tag", "search_content"],
    },
)


def get_chunk_by_filters(artist, tag, search_content, collection, embed_func):
    query_embedding = embed_func(search_content)
    if artist != "None" and tag != "None":
        where_dict = {"$or": [{"primary_artist": artist}, {"tags": tag}]}
    elif artist == "None":
        where_dict = {"tags": tag}
    elif tag == "None":
        where_dict = {"primary_artist": artist}
    # Query based on embedding value
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,  # can change this
        where=where_dict,
    )
    results_string = ""
    for i in range(len(results["ids"][0])):
        results_string += str(results["metadatas"][0][i])
        results_string += results["documents"][0][i]
        results_string += "\n"

    return results_string


# Define all functions available to the cheese expert
music_expert_tool = Tool(function_declarations=[get_chunk_by_filters_func])


def execute_function_calls(function_calls, collection, embed_func):
    parts = []
    for function_call in function_calls:
        print("Function:", function_call.name)
        if function_call.name == "get_chunk_by_filters":
            print(
                "Calling function with args:",
                function_call.args["artist"],
                function_call.args["tag"],
                function_call.args["search_content"],
            )
            response = get_chunk_by_filters(
                function_call.args["artist"],
                function_call.args["tag"],
                function_call.args["search_content"],
                collection,
                embed_func,
            )
            print("Response:", response)
            parts.append(
                Part.from_function_response(
                    name=function_call.name,
                    response={
                        "content": response,
                    },
                ),
            )

    return parts