#!/usr/bin/env python

from secret_santa import SecretSanta


secretsantas = {'Jessica': 'Carl', 'Lee': 'Binski', 'Mimi': 'Jessica', 'Papa': 'Alfred', 'Binski':
                'Lee', 'Alfred': 'Mimi', 'Carl': 'Papa'}

s = SecretSanta(santa_config='santas.yml', email=True, write=False, debug=False)
s._sendmail(secretsantas)
