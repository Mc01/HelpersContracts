#!/usr/bin/python3
import binascii

def __hex_bytes_string(string):
    bytes_string = bytes(string.encode('utf-8'))
    return f'0x{bytes_string.hex()}'

def test_create_profile(charity_profile, accounts):
    __profile_name = 'Jim Green'
    __profile_id = 'jim.green'
    __bytes_profile_name = __hex_bytes_string(__profile_name)
    __bytes_profile_id = __hex_bytes_string(__profile_id)
    charity_profile.create_profile(__bytes_profile_name, __bytes_profile_id)

    assert charity_profile.last_profile_no() == 1
    assert charity_profile.profile_ids(0) == __bytes_profile_id

    assert charity_profile.get_review_no(__bytes_profile_id) == 0

    charity_profile.add_review(
        __bytes_profile_id,
        __bytes_profile_name,
        (1,2,2,2,2,2),
        __hex_bytes_string("description"),
        __hex_bytes_string("http://trolololo.com"),
        __hex_bytes_string("@50.8046478,16.2890355,18z"),
    )

    assert charity_profile.get_review_no(__bytes_profile_id) == 1
