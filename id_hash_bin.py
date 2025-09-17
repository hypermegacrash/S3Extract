
# .bin hashes for all the games

import hashlib
from mod_color  import *
from debug_args import IN_PARAMS

game_releases_bin_xg = {
    "4d8733fe3aa1e397b64852c21cf6067ef9811cff7ea3f81a8818d7ef02ad168f": {'game': "XENOGEARS", 'version': "JP_TAIKEN", 'disc': 1, "rom": "Yoi Ko to Yoi Otona no. PlayStation Taikenban Vol. 1" },
    "e4ab5bbca64db33b47242c64589fa6a0398e93b3b576659a1df6132d27fac401": {'game': "XENOGEARS", 'version': "JP",        'disc': 1, "rom": "Xenogears Japan Disc 1"                               },
    "1bb150dc8ae1eed90f0d4b6fc8e0b83f18f278a30770af8c29eec1a7feec18eb": {'game': "XENOGEARS", 'version': "JP",        'disc': 2, "rom": "Xenogears Japan Disc 2"                               },
    "4d5fdc3b039b57175b07e1bd0a992c720935cbdd63790b2d59e8bcadcc25e89e": {'game': "XENOGEARS", 'version': "USA_DEMO",  'disc': 1, "rom": "Squaresoft Collector's CD Vol. 1"                     },
    "39c547a9afc6da15d847ef81a2c6cea1a6516bdfa562cf13b0999b04e8598bda": {'game': "XENOGEARS", 'version': "USA",       'disc': 1, "rom": "Xenogears USA Disc 1"                                 },
    "5eab85c683d4d7087d345b587472db9c44df29b35ce66553c2626d26018b947e": {'game': "XENOGEARS", 'version': "USA",       'disc': 2, "rom": "Xenogears USA Disc 2"                                 },
}

game_releases_bin_cc = {
    "0c0b7d630e8350e5d2ed2e238cc3df93df65847f82d22597729662d9b3f06bf3": {'game': "CHRONOCROSS", 'version': "JP_TAIKEN",  'disc': 1, "rom": "Square's Preview 5"                               },
    "a54fc8b085d7dbe768265e226afbdf536e52d72edaff8a21a34d3c771a8a313f": {'game': "CHRONOCROSS", 'version': "JP",         'disc': 1, "rom": "Chrono Cross Japan Disc 1"                        },
    "177ba2b120101107cca3c87e2d5d601ba9fde0975eaab23efab8c9099759b591": {'game': "CHRONOCROSS", 'version': "JP",         'disc': 2, "rom": "Chrono Cross Japan Disc 2"                        },
    "f34e062247a31a43cf2b85fc5d55784b40c9a4fb4ff9ab1c15ca04dacbbbc355": {'game': "CHRONOCROSS", 'version': "USA_BETA",   'disc': 1, "rom": "Chrono Cross USA Mar 8, 2000 80% Beta Disc 1"     },
    "f5b60a9a4c8785c9ca9b3ad79828f8f9f33f8ce62621f8fb96ff1a399226928f": {'game': "CHRONOCROSS", 'version': "USA_REVIEW", 'disc': 1, "rom": "Chrono Cross USA Apr 11, 2000 Beta Review Disc 1" },
    # USA_REVIEW Disc2 is the same as retail, not sure how best to handle this, just gonna ignore it
    #"e01c2367204f4d60a92011d4314ddad8db166f9211bdabb16cbf22d33e577899": {'game': "CHRONOCROSS", 'version': "USA_REVIEW", 'disc': 2, "rom": "Chrono Cross USA Apr 11, 2000 Beta Review Disc 2" },
    "01a0716ed46b6bce7717be1f9220f9bf323cee52404c9cd7fd4ef747d41a98da": {'game': "CHRONOCROSS", 'version': "USA", 'disc': 1, "rom": "Chrono Cross USA Disc 1"                                 },
    "e01c2367204f4d60a92011d4314ddad8db166f9211bdabb16cbf22d33e577899": {'game': "CHRONOCROSS", 'version': "USA", 'disc': 2, "rom": "Chrono Cross USA Disc 2"                                 },
}

game_releases_bin_dp = {
    "0c0b7d630e8350e5d2ed2e238cc3df93df65847f82d22597729662d9b3f06bf3": {'game': "DEWPRISM", 'version': "JP_TAIKEN", 'disc': 1, "rom": "Square's Preview 5",               },
    "fd0935b5b025af4890727ad77c56ee9590f7761701fd64dfb8d2849276d030f5": {'game': "DEWPRISM", 'version': "JP_TAIKEN", 'disc': 1, "rom": "Dengeki PlayStation D23",          },
    "ebeeb5cb8db7c3c2dcc7d239373275dcb42c6e635a7a4c2d22503003bbda9145": {'game': "DEWPRISM", 'version': "JP",        'disc': 1, "rom": "Dewprism Japan",                   },
    "c7bdc5534bc4bb3abb4681bf9608d8042f8474a460e4b86b9fd1e2060cdcdaa9": {'game': "DEWPRISM", 'version': "USA_BETA",  'disc': 1, "rom": "Dewprism USA 80% Beta",            },
    "91f7da9e18ea61125a95795048fc2f20460ddc68e1134a1525f295f9f610adbd": {'game': "DEWPRISM", 'version': "USA_DEMO",  'disc': 1, "rom": "Squaresoft Collector's CD Vol. 3", },
    "10ec26ea0c15b4605058543e61077824c37c7fd485a070604b8ea8805b0ee8f8": {'game': "DEWPRISM", 'version': "USA",       'disc': 1, "rom": "Dewprism USA",                     },
}

game_releases_bin = {
    "xenogears":   game_releases_bin_xg,
    "chronocross": game_releases_bin_cc,
    "dewprism":    game_releases_bin_dp,
}

def get_game_version_bin(inFileName):
    gameData = None

    with open(inFileName, "rb") as inBin:
        inBytes = inBin.read()
        imgHash = hashlib.sha256(inBytes).hexdigest()
        print(f"{CYAN}[VERSION] Attemping to find matching file hash for {imgHash}{RESET}")
        for game in game_releases_bin:
            if imgHash in game_releases_bin[game]:
                gameData = game_releases_bin[game][imgHash]
                version = f"{gameData['game']}_{gameData['version']}_DS{gameData['disc']:02}"
                print(f"{GREEN}[VERSION] FOUND HASH MATCH! {version}{RESET}")
                continue

    if not gameData:
        print(f"{YELLOW}[VERSION] Unknown game version...{RESET}")

    return gameData

if __name__ == "__main__":
    with open(IN_PARAMS['DP_USA_DEMO']['disc1'], "rb") as inBin:
        inBytes = inBin.read()
        imgHash = hashlib.sha256(inBytes).hexdigest()
        print(imgHash)
        for game in game_releases_bin:
            if imgHash in game_releases_bin[game]:
                print(game_releases_bin[game][imgHash]["rom"])