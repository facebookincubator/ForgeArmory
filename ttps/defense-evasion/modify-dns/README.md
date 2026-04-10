# Add Windows Local DNS Record

![Meta TTP](https://img.shields.io/badge/Meta_TTP-blue)

This TTP (Tactic, Technique, and Procedure) to add a local DNS record to the Windows `C:\\Windows\\System32\\drivers\\etc\\hosts` file.

## Arguments

- **ip_address**: IP address of the DNS record.
- **domain**: Domain/Sub-domain of the DNS record.

### Example Usage

Add a local DNS record to point example.com to `127.0.0.1`.
```bash
.\ttpforge.exe run forgearmory//utils/modify-dns/ttp.yaml \
--arg ip_address=127.0.0.1 \
--arg  domain=example.com
```
