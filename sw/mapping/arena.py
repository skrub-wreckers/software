from collections import namedtuple
import csv
from vision import Colors

Wall = namedtuple('Wall', 'x1 y1 x2 y2')
Stack = namedtuple('Stack', 'x y cubes')

class Arena(object):
    def __init__(self, walls, stacks, platforms, start):
        self.walls = walls
        self.stacks = stacks
        self.platforms = platforms
        self.start = start

    @classmethod
    def load(cls, fname):
        walls = []
        stacks = []
        platforms = []
        start = None
        with open(fname) as f:
            reader = csv.reader(f)

            for line in reader:
                if line[0] == 'W':
                    walls.append(Wall._make(map(int, line[1:])))
                elif line[0] == 'P':
                    walls.append(Wall._make(map(int, line[1:])))
                elif line[0] == 'S':
                    stacks.append(Stack(
                        x=int(line[1]),
                        y=int(line[2]),
                        cubes=[
                            Colors.GREEN if i == 'G' else Colors.RED
                            for i in line[3:]
                        ]
                    ))
                elif line[0] == 'L':
                    start = map(int, line[1:])

        return cls(walls=walls, stacks=stacks, platforms=platforms, start=start)
