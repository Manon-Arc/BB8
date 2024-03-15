# ------------------------------
# This file is part of the BB-8 robot project.
# Created By : Killian Guillemot
# Created At : 2020-05-01
# Version : 1.0
# ------------------------------
import machine


class MoteurDC:
    def __init__(self, pin1, pin2):
        self.pin1 = machine.Pin(pin1, machine.Pin.OUT)
        self.pin2 = machine.Pin(pin2, machine.Pin.OUT)
        self.pin1.value(0)
        self.pin2.value(0)
        self.vitesse = 1000
        self.speed = machine.PWM(machine.Pin(pin1))
        self.speed.freq(self.vitesse)
        self.status = "stop"

    def avancer(self):
        self.pin1.value(0)
        self.pin2.value(1)
        self.speed.freq(self.vitesse)
        self.status = "avance"

    def reculer(self):
        self.pin1.value(1)
        self.pin2.value(0)
        self.speed.freq(self.vitesse)
        self.status = "recule"

    def arreter(self):
        self.pin1.value(1)
        self.pin2.value(1)
        self.status = "stop"