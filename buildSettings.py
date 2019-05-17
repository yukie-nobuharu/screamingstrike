# -*- coding: utf-8 -*-
# Screaming Strike build settings
# Copyright (C) 2019 Yukio Nozawa <personal@nyanchangames.com>
# License: GPL V2.0 (See copying.txt for details)
import scorePostingAdapter

#	sys.stderr = open('data/errorLog.txt', 'w') # uncomment this line when releasing

GAME_NAME="Screaming Strike 2"
GAME_VERSION=2.00
UPDATE_SERVER_ADDRESS=""
UPDATE_PACKAGE_URL={
	"Windows": "",
	"Darwin": ""
}
UPDATE_PACKAGE_LOCAL_NAME={
	"Windows": "",
	"Darwin": ""
}

def getScorePostingAdapter(): return scorePostingAdapter.AdapterBase()