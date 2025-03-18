# aip-servers

Agent Interoperability Protocol Servers


## Installation

```shell
git clone https://github.com/unibaseio/aip-servers.git
cd aip-servers
pip install aip-agent git+https://github.com/unibaseio/aip-agent.git
```

### Requirements

- MEMBASE_ID must be unique for each instance
- MEMBASE_ACCOUNT must have balance in BNB testnet
- Environment variables must be set:
  - `MEMBASE_ID`: Unique identifier for the instance
  - `MEMBASE_ACCOUNT`: Account with BNB testnet balance
  - `MEMBASE_SECRET_KEY`: Secret key of account for authentication
  - `MEMBASE_SSE_URL`: (Required for SSE tools) Public endpoint URL

## Servers

### memory server

```shell
python src/memory_server/grpc_server.py
```

### beeper server

```shell
python src/beeper_server/grpc_server.py
```