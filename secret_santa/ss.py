#!/usr/bin/env python

'''
To Do:
------

- move child matches into couples dictionary as new key; results to include 
  couples dict so email addy and match are avail

'''

import secret_santa

ss = secret_santa.SecretSanta(santa_config='santas.yml', email=True, write=True, debug=True)
matches = ss.run()

print(matches)
