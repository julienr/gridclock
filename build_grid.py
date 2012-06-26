"""
This is a simple algorithm that will figure out all the words needed
to print all the hours/minutes. It will then create a crossword-like grid
with all those words
The goal is to build a clock similar to
http://thepagefoundry.com/TPFprojects/clock/
"""
from humantime.human_time import human_time
from datetime import datetime
import numpy as np
import numpy.ma as ma

def find_all_words():
    """Find all words used in human time"""
    words = set()
    for hour in xrange(0, 23):
        for minutes in xrange(0, 60):
            ht = human_time(datetime(2011, 1, 1, hour, minutes))
            for w in ht.split():
                words.add(w)
    return words

def check_placement(grid, word, pos, d):
    for i, w in enumerate(list(word)):
        if d == 'v':
            ci = pos[0] + i
            cj = pos[1]
        else:
            ci = pos[0]
            cj = pos[1] + i

        if ci >= grid.shape[0] or cj >= grid.shape[1]:
            return False

        cell = grid[ci, cj]
        if cell is not ma.masked and cell != w:
            return False
    return True

def find_best_pos(grid, word):
    for i in xrange(grid.shape[0]):
        for j in xrange(grid.shape[1]):
            for d in ['v', 'h']:
                if check_placement(grid, word, (i, j), d):
                    return (i, j, d)
    return None

def print_grid(grid):
    for i in xrange(grid.shape[0]):
        for j in xrange(grid.shape[1]):
            if grid[i, j] is ma.masked:
                print '* ',
            else:
                print '%s '%grid[i, j],
        print


def build_grid(words):
    sw = sorted(words, key=len, reverse=True)
    gs = len(sw[0])
    grid = ma.masked_all((gs, gs), dtype='a1')
    # 1. Place longest word on first row
    grid[0,:] = list(sw[0])
    sw.pop(0)

    # 2. Go through each word in the list by decreasing length, place
    #    at best position
    while len(sw) > 0:
        word = sw[0]
        wordlen = len(word)
        print "-- Best position for : ", word
        # Try to find a position. If we can't, increase grid size
        pos = find_best_pos(grid, word)
        while pos is None:
            newgrid = ma.masked_all((grid.shape[0]+1, grid.shape[1]+1),
                                    dtype='a1')
            newgrid[:-1,:-1] = grid
            grid = newgrid

            pos = find_best_pos(grid, word)
        print pos
        # Place word
        if pos[2] == 'v':
            grid[pos[0]:pos[0]+wordlen, pos[1]] = list(word)
        else: # 'h'
            grid[pos[0], pos[1]:pos[1]+wordlen] = list(word)
        print_grid(grid)
        sw.pop(0)


    print '==== Final grid ===='
    print "Shape : ", grid.shape
    print_grid(grid)


if __name__ == '__main__':
    words = find_all_words()
    build_grid(words)

