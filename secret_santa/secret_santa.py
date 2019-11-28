#!/usr/bin/env python

"""
Description: Plays traditional Secret Santa game, printing results to stdout,
             to files or send via email.
Author: Carl Tewksbury
Last Update: 2019-11-27 - Py3-ize; remove unneeded passing of couples var;
                          email auth password now in file.
"""

# stdlib
import random
import yaml
import copy
from datetime import date

# local
import ssmail


class SecretSanta(object):

    def __init__(self, santa_config=None, debug=False, write=False,
                 email=False):

        self.santas_config = santa_config
        self.couples = self._load_config()
        self.debug = debug
        self.write = write
        self.email = email
        d = date.today()
        self.year = d.year

    def badmatch(self, santa, pick):
        """ Santa can't pick themselves or anyone in their immediate family

        Args:
           couples (list): list of tuples, each containing persons who should
           not be matched together

        Returns:
            True if is bad match, False otherwise
        """

        res = False
        if santa == pick or self.couples[santa]['family'] == self.couples[pick]['family']:
            res = True

        return res

    def deadend(self, hat, santa, pick):
        """ Detect dead ends - a badmatch() is the only available pick """

        res = False
        if (len(hat) <= 2) and (self.badmatch(santa, pick)):
            print("only {0} left: {1}".format(len(hat), hat))
            res = True

        return res

    def pick_from_the_hat(self, secretsantas, hat, santa):
        """ Randomly select from the hat and check if its a good pick """

        pick = random.choice(hat)
        print("santa picked {}".format(pick))

        if self.deadend(hat, santa, pick):
            res = ("deadend")
        elif self.badmatch(santa, pick):
            res = ("badmatch")
        else:
            hat.remove(pick)
            print("looks good, man! I removed {} from the hat!".format(pick))
            res = pick

        return res

    def play(self, secretsantas, hat):
        """ Wrapper for picking function to deal with the results; such as
           dead ends resulting in the need to start the game over again
        """

        for santa, pick in secretsantas.items():
            santaschoice = False
            while santaschoice == False:
                print('santa is {} ... '.format(santa), end='')
                mypick = self.pick_from_the_hat(secretsantas, hat, santa)
                if mypick == "deadend":
                    print("crap, deadend!")
                    return True
                elif mypick == "badmatch":
                    print("crap, bad match!")
                    continue
                elif mypick:
                    print("adding match...", santa, "->", mypick)
                    secretsantas[santa] = mypick
                    santaschoice = True

        return False

    def _makefiles(self, secretsantas):
        for santa, child in secretsantas.items():
          message = santa + ' is secret santa for: ' + child
          santaf = '/tmp/' + santa + '_secret_santa.txt'

          with open(santaf, 'w+') as f:
            f.write(message)

    def _sendmail(self, secretsantas):

        for santa, child in secretsantas.items():
            to_address = self.couples[santa]['email']

            print(to_address, santa, child)
            e = ssmail.Email(santa=santa, child=child, to_address=to_address,
                        debug=self.debug)
            r = e.send()

    def _load_config(self):
        with open(self.santas_config, 'r') as f:
            return yaml.safe_load(f)

    def makefiles(self, secretsantas):
        for santa, pick in secretsantas.iteritems():
            message = '{0} is secret santa for: {1} '.format(santa, pick)
            santaf = '/tmp/{0}_SecretSanta-{1}.txt'.format(santa, self.year)

            with open(santaf, 'w+') as f:
              f.write(message)

    def run(self):
        keepplaying = True

        while keepplaying:
            hat = []
            secretsantas = {}

            # Each time we play again, reinitialize the elves data
            self.couples = self._load_config()

            if self.debug:
              print(self.couples)

            # Create list of santas in the hat using couples data
            secretsantas = copy.deepcopy(self.couples)

            for santa in secretsantas:
                hat.append(santa)

            keepplaying = self.play(secretsantas, hat)

            if self.debug:
                print('secret santas: {}'.format(secretsantas))

        print('makefile:', self.write)
        print('sendmail:', self.email)

        if self.write:
            self._makefiles(secretsantas)
        if self.email:
            print('...sending emails!')
            self._sendmail(secretsantas)

        return secretsantas
