from flask import Flask ,flash, render_template ,request, jsonify,redirect,url_for
from flask.globals import g

from passlib.hash import sha256_crypt
import os
import pymysql


password = sha256_crypt.encrypt("12345")
print(password)  
print(sha256_crypt.verify("12345", '$5$rounds=535000$bgLSDP.bRQV1nwUD$pLoDM79keNU7y5rNZXLbzkheg4rttO01N6Tmm17ZEs.'))