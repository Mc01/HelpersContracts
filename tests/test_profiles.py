#!/usr/bin/python3
from eth_utils.conversions import to_hex, to_bytes

def test_create_profile(charity_profile, accounts):
    # Encode with UTF-8 makes sure we are dealing with Bytes and not Str
    __profile_name = 'John Carmac'
    __profile_id = 'john.carmac'
    __bytes_profile_name = __profile_name.encode('utf-8')
    __bytes_profile_id = __profile_id.encode('utf-8')
    __hex_bytes_profile_name = f'0x{bytes(__bytes_profile_id).hex()}'
    __hex_bytes_profile_id = f'0x{bytes(__bytes_profile_id).hex()}'

    assert charity_profile.last_profile_no() == 0
    assert charity_profile.profile_ids(0) == '0x0'
    assert not charity_profile.profiles__exists(__hex_bytes_profile_id)

    charity_profile.create_profile(__bytes_profile_name, __hex_bytes_profile_id)

    assert charity_profile.last_profile_no() == 1
    assert charity_profile.profile_ids(0) == __hex_bytes_profile_id

    # TODO: Make sure mapping (bytes32 => Profile) works or might revert to (uint256 => Profile)
    # print(f'To Bytes: {to_bytes(__bytes_profile_id)}')
    # print(f'To Hex: {to_hex(__bytes_profile_id)}')
    # print(f'Bytes: {charity_profile.profile_ids(0)} and bytes: {__hex_bytes_profile_id}')
    # print(f'This should return value: {charity_profile.profiles__name(__hex_bytes_profile_id)}')
    # assert charity_profile.profiles__exists(__hex_bytes_profile_id)
    # assert charity_profile.profiles__exists(__hex_bytes_profile_id)
    # assert charity_profile.profiles__last_review_no(__hex_bytes_profile_id) == 0
    # assert charity_profile.profiles__name(__hex_bytes_profile_id) == __profile_name
    # assert charity_profile.profiles__profile_id(__hex_bytes_profile_id) == __profile_id
