#!/usr/bin/python3
from brownie import *
from os import environ


GAS_LIMIT = 5000000


def __hex_bytes_string(string):
    bytes_string = bytes(string.encode('utf-8'))
    return f'0x{bytes_string.hex()}'


def main():
    if 'PK' in environ:
        accounts.add(environ['PK'])
    account = accounts[0]

    address = '0xc244DfAf7Af5587C3a203EDC01816f2F8661e3Df'
    owner_address = '0xE8786Aa041a586a8C32299F58e2342802d3eD6C1'
    charity_profile = CharityProfile.at(address)

    __profile_name = 'Jim Green'
    __profile_id = 'jim.green'
    __bytes_profile_name = __hex_bytes_string(__profile_name)
    __bytes_profile_id = __hex_bytes_string(__profile_id)
    
    charity_profile.create_profile(
        __bytes_profile_name,
        __bytes_profile_id,
        {'from': account, 'gas': GAS_LIMIT}
    )
