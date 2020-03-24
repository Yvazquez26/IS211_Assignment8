#!/usr/bin/env python
# coding: utf-8

# Assignment 8 - Design Patterns


import random
import sys
import argparse
import time


class player:
    """Players for the game Pig."""
    
    def __init__(self, name, total=0):
        self.name = name
        self.total = total

    def newTotal(self, newscore):
        self.total = self.total + newscore

    def rollHold(self, gametotal=0):
        roll = input('Roll or Hold? r = roll, h = hold')
        return roll


class ComputerPlayer(player):
    """Computer player for the game Pig."""
    
    def rollHold(self, gametotal):
        limit = 100 - self.total
        limit = 25 if limit > 25 else limit

        if ( gametotal < limit ):
            roll = 'r'
            rolling = 'rolling'
        else:
            roll = 'h'
            rolling = 'holding'

        return roll


class playerfactory:
    """A Factory class that will instantiate either a human or computer player,depending on 
    the class"""
    
    def getplayer(self, playertype, name):
        if playertype == 'h':
            return player(name)
        if playertype == 'c':
            return ComputerPlayer(name)


class Dice:
    """A constructor for the game when the players roll."""
    def __init__(self, roll=0):
        self.roll =  roll

    def newRoll(self, seed): 
        random.seed(seed)
        self.roll = random.randrange(1, 7)
        return self.roll


class gamecenter:
    """The player's score during the game as the player plays."""
    
    def __int__(self, players, total=0):
        self.player1 = players[1]
        self.player2 = players[2]
        self.ttotal = total

    def turnScore(self, newscore):
        self.ttotal = self.ttotal + newscore
        return self.ttotal

    def totalScoreCheck(self, player, winpoints):
        score = player.total + self.ttotal
        if score >= winpoints:
            player.total = score
            print('%s You win' % (player.name))
            print('Final score', player.total)
            self.gameOver()

    def tswitch(self, ComputerPlayer):
        self.ttotal = 0
        print('Switch players')
        return 2 if ComputerPlayer == 1 else 1

    def statcurrent(self, player, new_roll):
        print('%s rolled %s. Score for this turn is %s and player total score is %s' %         (player.name, new_roll, self.ttotal, player.total))

    def playerGreet(self, player):
        print('%s, your current score is %s.' %         (player.name, player.total))

    def gameOver(self):
        print('Game Over. Restart to play again.')    
        sys.exit()


class TimeGameProxy:
    """A Proxy to the Game class that follows all the same exact rules of Pig as before, 
    but with a timed aspect: the game will continue until either someone scores 100, 
    or one minute has elapsed since the start of the game."""
    
    def __init__(self, timestamp = 0):
        self.timestamp = timestamp
        self.dice = None
        self.dice = Dice()

    def timecheck(self, timestamp):
        if (self.timestamp == 0 or self.timestamp > time.time() ):
            seed = time.time()
            return self.dice.newRoll(seed)
        else:
            print('Game Over')
            print("Time's up")
            sys.exit() 


def main():
    """This function runs the game when the program is executed."""
    
    parser = argparse.ArgumentParser()
    player1 = parser.add_argument('--player1', help='enter player type: "c" - computer, "h" -human eg: --player1 c', type=str)
    player2 = parser.add_argument('--player2', help='enter player type: "c" - computer, "h" -human eg: --player1 c', type=str)
    timed = parser.add_argument('--timed', help='timed game enter y', type=str)
    args, unknown = parser.parse_known_args()

    factory = playerfactory()
    game = gamecenter()

    players = { 1: factory.getplayer(args.player1,'player1'),
                2: factory.getplayer(args.player2,'player2')}

    if args.timed=='y':
        timestamp = time.time() + 60
    else:
        timestamp = 0
    
    p = TimeGameProxy(timestamp)

    ComputerPlayer = 1
    game.ttotal = 0
    game.playerGreet(players[ComputerPlayer])

    while (players[ComputerPlayer].total < 100) :
        new_roll = p.timecheck(timestamp)

        roll = players[ComputerPlayer].rollHold(game.ttotal)

        if roll == 'r':

            print('DICE ROLL: ', new_roll)
            if new_roll == 1:
                game.ttotal = 0
                game.statscurrent(players(ComputerPlayer),new_roll)
                ComputerPlayer = game.tswitch(ComputerPlayer)
                game.playerGreet(players(ComputerPlayer)
                p.timecheck(timestamp)
            else:
                game.ttotal = game.turnScore(new_roll)
                game.statscurrent(players(ComputerPlayer),new_roll)
                game.totalScoreCheck(players(ComputerPlayer), 100)
                p.timecheck(timestamp)

        elif roll == 'h':
            p.timecheck(timestamp)
            print(players(ComputerPlayer).name, 'adds', game.ttotal, 'points to the previous total of', players[ComputerPlayer].total)
            players(ComputerPlayer).newTotal(game.ttotal)
            ComputerPlayer = game.tswitch(ComputerPlayer)
            game.playerGreet(players(ComputerPlayer))

        else:
            print("enter r - to roll or h - to hold")

        p.timecheck(timestamp)

    sys.exit()


if __name__ == '__main__':
    main()
