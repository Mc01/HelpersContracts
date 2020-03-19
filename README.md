# HelpersContracts

## Architecture

1. Frontend
2. Flask as API layer
- `/create` - submits new opinion for phone number
- `/verify` - retrieves opinion for phone number
- `/whitelist` - add address to whiteliste
- `/list` - retrieves all participants, requires whitelist
3. Keys, ABI and Web3 communication layer
- assumption: `testnet` servers
- keys on backend layer
- transaction fees on backend keys
- integrates Web3 as API
4. Vyper layer
- `whitelist` -> premium users/integrators
- `opinionList` -> read for whitelisted addresses
- `opinionMapping` (phone_number -> []opinions) -> free access
