#!/usr/bin/python3
from eth_utils.conversions import to_hex, to_bytes

def __hex_bytes_string(string):
    bytes_string = bytes(string.encode('utf-8'))
    return f'0x{bytes_string.hex()}'

def test_create_profile(charity_profile, accounts):
    # Encode with UTF-8 makes sure we are dealing with Bytes and not Str
    __profile_name = 'John Carmac'
    __profile_id = 'john.carmac'
    __bytes_profile_name = __hex_bytes_string(__profile_name)
    __bytes_profile_id = __hex_bytes_string(__profile_id)

    assert charity_profile.last_profile_no() == 0
    assert charity_profile.profile_ids(0) == '0x0'
    assert not charity_profile.profiles__exists(__bytes_profile_id)

    charity_profile.create_profile(__bytes_profile_name, __bytes_profile_id)

    assert charity_profile.last_profile_no() == 1
    assert charity_profile.profile_ids(0) == __bytes_profile_id

    assert charity_profile.profiles__exists(__bytes_profile_id)
    assert charity_profile.profiles__exists(__bytes_profile_id)
    assert charity_profile.profiles__last_review_no(__bytes_profile_id) == 0
    assert charity_profile.profiles__name(__bytes_profile_id) == __bytes_profile_name
    assert charity_profile.profiles__profile_id(__bytes_profile_id) == __bytes_profile_id
