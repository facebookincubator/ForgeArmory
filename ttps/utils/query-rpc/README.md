# Query RPC

## Description
This TTP uses rpcclient to perform RPC queries against an Active Directory Domain Controller.

## Arguments
- **host**: The Domain Controller IP or hostname to target. No default (required).
- **username**: The username for RPC authentication (leave nil for anonymous query). Defaults to `NIL`.
- **password**: The password for the user (leave nil for anonymous query). Defaults to `NIL`.
- **query**: The RPC query to execute (e.g., enumdomusers, enumdomgroups, queryuser). No default (required).

## Requirements
- **Platforms:** Linux

## Example(s)
```bash
ttpforge run forgearmory//ttps/utils/query-rpc/ttp.yaml \
  --arg host=dc01.contoso.local \
  --arg username=jsmith \
  --arg password='P@ssw0rd' \
  --arg query=enumdomusers
```

```bash
# Anonymous/null session query
ttpforge run forgearmory//ttps/utils/query-rpc/ttp.yaml \
  --arg host=dc01.contoso.local \
  --arg query=enumdomusers
```

## Steps
1. **ensure_rpcclient_installed**: Install rpcclient if not already installed.
2. **execute_rpc_query**: Execute rpcclient to query RPC. Supports both authenticated and anonymous (null session) queries.
