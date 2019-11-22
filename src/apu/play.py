import pygame
import numpy
import scipy.signal
from array import array
from time import sleep
from random import randint
import numpy as np
from pygame.mixer import Sound, get_init, pre_init, set_num_channels
from .pulse import PulseChannel
from .triangle import TriangleChannel
from .noise import NoiseChannel

CPU_CLOCK = 1789773
pre_init(44100, -16, 1, 1024)

class PulseNote(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


class TriangleNote(Sound):
    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_sample())
        self.set_volume(volume)

    def build_sample(self):
        wave = scipy.signal.triang(500 * 440 // self.frequency)
        amplitude = 2 ** (15) - 1
        sample = wave * amplitude
        sample = numpy.resize(sample, 44100)
        return sample.astype(numpy.int16)


class NoiseNote(Sound):
    def __init__(self, frequency, period, volume=.1):
        self.frequency = frequency
        self.period = period
        Sound.__init__(self, self.build_sample())
        self.set_volume(volume)

    def build_sample(self):
        amplitude = 2 ** (15) - 1
        samples = np.linspace(0, self.period, int(self.frequency * self.period), endpoint=False)
        sample = samples * amplitude
        sample = numpy.resize(sample, self.frequency)
        return sample.astype(numpy.int16)


class APUPlayState:

    @staticmethod
    def play_pulse(regs, start_index):
        pulse = PulseChannel(regs[start_index], regs[start_index + 1], regs[start_index + 2], regs[start_index + 3])
        timer = (pulse.get_timer_high() << 8) + pulse.get_timer_low()
        if timer > 7:
            volume = pulse.get_volume() / 15
            frequency = CPU_CLOCK / (16 * (timer + 1))
            pygame.mixer.Channel(start_index).play(PulseNote(frequency, volume), timer)
            regs[start_index] = 0
            regs[start_index + 2] = 0
            regs[start_index + 3] = 0

    @staticmethod
    def play_tri(regs, start_index):
        channel = TriangleChannel(regs[start_index], regs[start_index + 2], regs[start_index + 3])  ## skips $4009
        timer = (channel.get_timer_high() << 8) + channel.get_timer_low()
        frequency = CPU_CLOCK / (32 * (timer + 1))
        if timer > 0:
            pygame.mixer.Channel(start_index).play(TriangleNote(frequency), timer)
            regs[start_index + 2] = 0
            regs[start_index + 3] = 0
            regs[start_index] = 0

    @staticmethod
    def play_noise(regs, start_index):
        channel = NoiseChannel(regs[start_index], regs[start_index + 2], regs[start_index + 3])
        timer = (channel.get_lcl() << 8) + channel.get_loop_noise()
        period = channel.get_noise_period()
        frequency = randint(1, 15) * 440 ** 2
        pygame.mixer.Channel(start_index).play(NoiseNote(frequency, period), timer)
        regs[start_index + 2] = 0
        regs[start_index + 3] = 0
        regs[start_index] = 0

    @staticmethod
    def play(regs):
        set_num_channels(0x10)
        APUPlayState.play_pulse(regs, 0)
        APUPlayState.play_pulse(regs, 4)
        APUPlayState.play_tri(regs, 8)
        # APUPlayState.play_noise(regs, 12)
