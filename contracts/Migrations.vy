owner: public(address)
last_completed_migration: public(uint256)

@public
def __init__():
    self.owner = msg.sender

@public
def setCompleted(completed: uint256):
    # assert(msg.sender == self.owner, "Boom bitch")
    self.last_completed_migration = completed
