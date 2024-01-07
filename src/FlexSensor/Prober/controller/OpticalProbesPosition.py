import sys
import logging

from FlexSensor.FSBase import FSBase


class OpticalProbesPosition(FSBase):

    def __init__(self, input: tuple, output: tuple):
        super().__init__()
        self.INPUT: ProbePosition = ProbePosition(input)
        self.OUT: ProbePosition = ProbePosition(output)
        self.logger = self.create_new_logger(self.name)


    def __str__(self):
        return f"INPUT: {self.INPUT} | OUT: {self.OUT}"


class ProbePosition:

    def __init__(self, position: tuple):
        self.x, self.y, self.z = position

    def __str__(self):
        return f"x:{self.x} - y:{self.y} - z:{self.z}"
    
    def __substract__(self, other):
        pass

