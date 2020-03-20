#!/usr/bin/python3

def test_owner(charity_profile, accounts):
    assert charity_profile.owner() == accounts[0]
