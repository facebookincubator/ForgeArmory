#!/usr/bin/env python3
"""Enumerate AD usernames via Kerberos AS-REQ without pre-authentication."""

import argparse
import re
from datetime import datetime, timezone

from impacket.krb5 import constants
from impacket.krb5.asn1 import AS_REQ, KERB_PA_PAC_REQUEST, seq_set, seq_set_iter
from impacket.krb5.kerberosv5 import KerberosError, sendReceive
from impacket.krb5.types import KerberosTime, Principal
from pyasn1.codec.der import encoder
from pyasn1.type.univ import noValue

STATUS_MAP = {
    25: "VALID",  # KDC_ERR_PREAUTH_REQUIRED
    6: "NOT FOUND",  # KDC_ERR_C_PRINCIPAL_UNKNOWN
    18: "DISABLED",  # KDC_ERR_CLIENT_REVOKED
    23: "EXPIRED",  # KDC_ERR_KEY_EXPIRED
}
PREFIX = {"VALID": "[+]", "NOT FOUND": "[-]", "NO PREAUTH": "[!]"}


def parse_dc_address(dc_str):
    """Return (host, port) from a DC address string."""
    m = re.match(r"^\[([^\]]+)\](?::(\d+))?$", dc_str)
    if m:
        return m.group(1), int(m.group(2)) if m.group(2) else None
    if dc_str.count(":") > 1:
        return dc_str, None
    if ":" in dc_str:
        host, port = dc_str.rsplit(":", 1)
        return host, int(port)
    return dc_str, None


def build_as_req(username, domain):
    """Build an AS-REQ without pre-authentication data."""
    as_req = AS_REQ()
    as_req["pvno"] = 5
    as_req["msg-type"] = int(constants.ApplicationTagNumbers.AS_REQ.value)

    # PA-DATA: only PA-PAC-REQUEST (no pre-auth credentials)
    pa_pac = KERB_PA_PAC_REQUEST()
    pa_pac["include-pac"] = True

    as_req["padata"] = noValue
    as_req["padata"][0] = noValue
    as_req["padata"][0]["padata-type"] = int(
        constants.PreAuthenticationDataTypes.PA_PAC_REQUEST.value
    )
    as_req["padata"][0]["padata-value"] = encoder.encode(pa_pac)

    req_body = seq_set(as_req, "req-body")
    opts = [
        constants.KDCOptions.forwardable.value,
        constants.KDCOptions.renewable.value,
        constants.KDCOptions.proxiable.value,
    ]
    req_body["kdc-options"] = constants.encodeFlags(opts)

    client = Principal(username, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
    server = Principal(
        "krbtgt/%s" % domain, type=constants.PrincipalNameType.NT_PRINCIPAL.value
    )
    seq_set(req_body, "cname", client.components_to_asn1)
    seq_set(req_body, "sname", server.components_to_asn1)
    req_body["realm"] = domain

    now = KerberosTime.to_asn1(datetime.now(timezone.utc))
    req_body["till"] = now
    req_body["rtime"] = now
    req_body["nonce"] = 0

    ciphers = (
        int(constants.EncryptionTypes.aes256_cts_hmac_sha1_96.value),
        int(constants.EncryptionTypes.aes128_cts_hmac_sha1_96.value),
        int(constants.EncryptionTypes.rc4_hmac.value),
    )
    seq_set_iter(req_body, "etype", ciphers)

    return encoder.encode(as_req)


def check_user(username, domain, dc_host, dc_port):
    """Send AS-REQ and return status string."""
    try:
        sendReceive(build_as_req(username, domain), domain, dc_host, port=dc_port)
        return "NO PREAUTH"
    except KerberosError as e:
        return STATUS_MAP.get(e.getErrorCode(), "UNKNOWN (%d)" % e.getErrorCode())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True)
    parser.add_argument("--dc", required=True)
    parser.add_argument("userlist")
    args = parser.parse_args()

    dc_host, dc_port = parse_dc_address(args.dc)
    dc_port = dc_port or 88
    domain = args.domain.upper()

    with open(args.userlist) as f:
        users = [line.strip() for line in f if line.strip()]

    for user in users:
        status = check_user(user, domain, dc_host, dc_port)
        pfx = PREFIX.get(status, "[!]")
        print("%s %-14s %s@%s" % (pfx, status, user, domain))
