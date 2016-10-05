"""Manages variety of rates given a base rate"""
import logging
from math import trunc
INDI_SUB = 100


class Rate:
    def __init__(self, rate):
        self.base_rate = rate

    def indi_member(self, hours=1):
        return (self.base_rate-INDI_SUB) * hours

    def indi_vip(self, hours=1, disc=10):
        indi_base = (self.base_rate - INDI_SUB)
        vip_discount = indi_base*(disc/100)
        vip_discount_round = trunc((vip_discount+4)/5)*5

        # Indi foibles
        if indi_base == 180:
            vip_discount_round = 35
        elif indi_base == 130:
            vip_discount_round = 25
        elif indi_base == 110:
            vip_discount_round = 20

        new_rate = indi_base-vip_discount_round
        logging.debug("%d // (%d)%d // %d", indi_base, vip_discount, vip_discount_round, new_rate)
        return (new_rate)*hours

    def web_rate(self, hours=1):
        return self.base_rate * hours

    def __str__(self):
        return "{}/{}".format(self.indi_member(), self.indi_vip(disc=20))

