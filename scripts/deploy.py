#!/usr/bin/python3
from brownie import *
from os import environ


def main():
    if 'PK' in environ:
        accounts.add(environ['PK'])
    account = accounts[0]

    CharityProfile.deploy({'from': account})
