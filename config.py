import os


PWD = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(PWD, "data")

STEAM_API_KEY = "" # Apply then put your own steam api key here

JSON_PATH = os.path.join(DATA_DIR, "database.json")

DB_PATH = os.path.join(DATA_DIR, "database.db")

HEROES_CN_PATH = os.path.join(DATA_DIR, "heroes_cn.json")

NPY_PATH = os.path.join(DATA_DIR, "statistics.npy")

ACCOUNTS_ID = [105248644, 34505203, 82262664, 101356886, 72312627,  # Liquid
               82327674, 149486894, 139876032, 117281554, 87012746,  # Newbee
               114239371, 119576842, 90882159, 148215639, 111189717,  # LFY
               98878010, 107081378, 106863163, 177416702, 134276083,  # LGD
               134556694, 132851371, 106573901, 92423451, 106809101,  # VP
               140153524, 205813150, 129958758, 207829314, 90892734,  # IG
               43276219, 86799300, 86726887, 40547474, 6922000,  # NP
               87278757, 89117038, 116585378, 101450083, 169025618,  # Secret
               94155156, 311360822, 26771994, 41231571, 19672354, # OG
               111620041, 86745912, 87276347, 73562326, 25907144,  # EG
               113331514, 92847434, 159020918, 5150808, 86725175,  # Empire
               87196890, 155494381, 184950344, 132309493, 187619311]  # TNC
