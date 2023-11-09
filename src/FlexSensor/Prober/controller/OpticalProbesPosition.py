import sys
import logging


class OpticalProbesPosition:

    def __init__(self, input: tuple, output: tuple):
        self.INPUT: ProbePosition = ProbePosition(input)
        self.OUT: ProbePosition = ProbePosition(output)
        self.logger = logging.getLogger('OpticalProbesPosition')


    def __str__(self):
        return f"INPUT: {self.INPUT} | OUT: {self.OUT}"


class ProbePosition:

    def __init__(self, position: tuple):
        self.x, self.y, self.z = position

    def __str__(self):
        return f"x:{self.x} - y:{self.y} - z:{self.z}"
    
    def __substract__(self, other):
        pass

