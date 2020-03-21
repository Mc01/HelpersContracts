# @SECTION: Const
# .
# .
# .
# Enums for Scoring Values
NEEDS_IMPROVEMENT: constant(uint256) = 0
MEETS_EXPECTATIONS: constant(uint256) = 1
OUTSTANDING: constant(uint256) = 2

# @SECTION: Structures
# .
# .
# .
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

# @SECTION: Variables
# .
# .
# .
# Contract owner
owner: public(address)

# Whitelisted users
# Key: address -> Value: bool
whitelist: public(map(address, bool))

# List of user ids
# Key: profile_no -> Value: profile_id
# Behaves like an array
# Maps numbers like 0 to profile_id
profile_ids: public(map(uint256, bytes32))
last_profile_no: public(uint256)

# Map of user profiles
# Key: profile_id -> Value: Profile
profiles: public(map(bytes32, Profile))

# Map of user reviews
# Key: profile_id -> SecondKey: review_no -> Value: Review
reviews: public(map(bytes32, map(uint256, Review)))

# @SECTION: Constructor
# .
# .
# .
@public
def __init__():
    self.owner = msg.sender
    self.last_profile_no = 0

# @SECTION: Parsers and value checkers
# .
# .
# .
@private
def __is_valid_scoring_value(value: uint256):
    assert value in [
        NEEDS_IMPROVEMENT,
        MEETS_EXPECTATIONS,
        OUTSTANDING,
    ]

@private
def __parse_score(score: Score) -> Score:
    self.__is_valid_scoring_value(score.effectivness)
    self.__is_valid_scoring_value(score.humanism)
    self.__is_valid_scoring_value(score.responsibility)
    self.__is_valid_scoring_value(score.autonomy)
    self.__is_valid_scoring_value(score.progress)
    self.__is_valid_scoring_value(score.autonomy)
    return score

# @SECTION: Access control
# .
# .
# .
@private
def __assert_owner(msg_sender: address):
    assert msg_sender == self.owner

@private
def __assert_valid_sender(msg_sender: address):
    assert msg_sender == self.owner or self.whitelist[msg_sender]

# @SECTION: Profile getters
# .
# .
# .
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

# @SECTION: Review getters
# .
# .
# .
@private
def __get_new_review(profile_id: bytes32, review_no: uint256) -> Review:
    review: Review = self.reviews[profile_id][review_no]
    assert not review.exists
    return review

# @SECTION: Public methods
# .
# .
# .
@public
def add_to_whitelist(user: address):
    self.__assert_owner(msg.sender)
    self.whitelist[user] = True

@public
def remove_from_whitelist(user: address):
    self.__assert_owner(msg.sender)
    self.whitelist[user] = False

@public
def create_profile(
    name: bytes32,
    profile_id: bytes32,
):
    self.__assert_valid_sender(msg.sender)
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
    self.__assert_valid_sender(msg.sender)
    # Assert profile exist
    profile: Profile = self.__get_existing_profile(profile_id)
    # Assert review does not exist
    review: Review = self.__get_new_review(profile_id, profile.last_review_no)
    # Fill review
    review.reviewer_name = reviewer_name
    review.score = self.__parse_score(score)
    review.description = description
    review.url = url
    review.exists = True
    # Increment last review number
    profile.last_review_no += 1
