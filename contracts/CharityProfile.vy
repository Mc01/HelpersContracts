# Enums for Scoring Values
NEEDS_IMPROVEMENT: constant(uint256) = 0
MEETS_EXPECTATIONS: constant(uint256) = 1
OUTSTANDING: constant(uint256) = 2

# Scoring based on 10C Values
struct Score:
    effectivness: uint256
    humanism: uint256
    responsibility: uint256
    autonomy: uint256
    progress: uint256
    creativty: uint256

# Review of Profile
struct Review:
    reviewer_name: bytes32
    score: Score
    description: bytes32
    url: bytes32
    exists: bool

# Verified Profile
struct Profile:
    name: bytes32
    profile_id: bytes32
    last_review_no: uint256
    exists: bool

# Contract owner
owner: public(address)

# Key: profile_no -> Value: profile_id
# Behaves like an array
# Maps numbers like 0 to profile_id
profile_ids: public(map(uint256, bytes32))
last_profile_no: public(uint256)

# Key: profile_id -> Value: Profile
profiles: public(map(bytes32, Profile))

# Key: profile_id -> SecondKey: review_no -> Value: Review
reviews: public(map(bytes32, map(uint256, Review)))


@public
def __init__():
    self.owner = msg.sender

@private
def __assert_owner(msg_sender: address):
    assert msg_sender == self.owner

@private
def __get_new_profile(profile_id: bytes32) -> Profile:
    profile: Profile = self.profiles[profile_id]
    assert not profile.exists
    return profile

@private
def __get_existing_profile(profile_id: bytes32) -> Profile:
    profile: Profile = self.profiles[profile_id]
    assert profile.exists
    return profile

@private
def __get_new_review(profile_id: bytes32, review_no: uint256) -> Review:
    review: Review = self.reviews[profile_id][review_no]
    assert not review.exists
    return review

@public
def create_profile(
    name: bytes32,
    profile_id: bytes32,
):
    # Validate sender
    self.__assert_owner(msg.sender)
    # Assert profile does not exist
    profile: Profile = self.__get_new_profile(profile_id)
    # Fill profile
    profile.name = name
    profile.profile_id = profile_id
    profile.last_review_no = 0
    profile.exists = True
    # Update profile ids with new profile id
    self.profile_ids[self.last_profile_no] = profile_id
    # Increment last profile number
    self.last_profile_no += 1

@public
def add_review(
    profile_id: bytes32,
    reviewer_name: bytes32,
    score: Score,
    description: bytes32,
    url: bytes32,
):
    # Validate sender
    self.__assert_owner(msg.sender)
    # Assert profile exist
    profile: Profile = self.__get_existing_profile(profile_id)
    # Assert review does not exist
    review: Review = self.__get_new_review(profile_id, profile.last_review_no)
    # Fill review
    review.reviewer_name = reviewer_name
    review.score = score
    review.description = description
    review.url = url
    review.exists = True
    # Increment last review number
    profile.last_review_no += 1
