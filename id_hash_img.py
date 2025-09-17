
# .img hashes for all the games

import hashlib
from mod_color  import *
from debug_args import IN_PARAMS

game_releases_img_xg = {
    "5ee66db482493a75055e3b483ea22d64b2dcdce6ad1843c186ebc6f771660bd0": {'game': "XENOGEARS", 'version': "JP_TAIKEN", 'disc': 1, "rom": "Yoi Ko to Yoi Otona no. PlayStation Taikenban Vol. 1" },
}

game_releases_img_cc = {
    "2734b333f0f95279292aff54d1abd3f799709ecdf5e172be99de7daa14d5869b": {'game': "CHRONOCROSS", 'version': "JP_TAIKEN", 'disc': 1, "rom": "Square's Preview 5" },
}

game_releases_img_dp = {
    "383d5c23756a889b28968138093e6ee037278f1acee66053428b5a8656a81169": {'game': "DEWPRISM", 'version': "JP_TAIKEN",'disc': 1, "rom": "Square's Preview 5 / Dengeki PlayStation D23", },
    "77d880a53e2bd11cb41efa254c44e0ad2c8381345ed01b66ad67b89497dadfb4": {'game': "DEWPRISM", 'version': "USA_DEMO", 'disc': 1, "rom": "Squaresoft Collector's CD Vol. 3", },
}

game_releases_hedimg = {
    "xenogears":   game_releases_img_xg,
    "chronocross": game_releases_img_cc,
    "dewprism":    game_releases_img_dp,
}

def get_game_version_img(inFileName):
    gameData = None

    with open(inFileName, "rb") as inBin:
        inBytes = inBin.read()
        imgHash = hashlib.sha256(inBytes).hexdigest()
        print(f"{CYAN}[VERSION] Attemping to find matching file hash for {imgHash}{RESET}")
        for game in game_releases_hedimg:
            if imgHash in game_releases_hedimg[game]:
                gameData = game_releases_hedimg[game][imgHash]
                version = f"{gameData['game']}_{gameData['version']}_DS{gameData['disc']:02}"
                print(f"{GREEN}[VERSION] FOUND HASH MATCH! {version}{RESET}")
                continue

    if not gameData:
        print(f"{YELLOW}[VERSION] Unknown game version... no filetree can be used.{RESET}")

    return gameData

if __name__ == "__main__":
    with open(IN_PARAMS['XG_JP_TAIKEN']['img'], "rb") as inBin:
        inBytes = inBin.read()
        imgHash = hashlib.sha256(inBytes).hexdigest()
        print(imgHash)
        for game in game_releases_hedimg:
            if imgHash in game_releases_hedimg[game]:
                print(game_releases_hedimg[game][imgHash]["rom"])