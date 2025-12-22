# Scan IP Blocks

![Community TTP - sw8y](https://img.shields.io/badge/Community_TTP-green)

Perform a syn scan against a range of IP addresses.

## Arguments

- **ip_range (string)**: A range of IP addresses to be scanned.
  This range can be provided in CIDR notation (e.g, 10.0.0.0/16)

- **ports (string)**: Ports to be scanned for on each IP address. If this
  parameter is not provided, the default port list will be scanned.

  Default: 20,21,22,23,25,53,80,110,125,143,443,587,2525,3306,3389

## Pre-requisites

Ensure that you have the necessary package manager for your system:

- APT for Linux

- Brew for Mac

## Examples

Execute port scans against a supplied IP address block. Once execution is
complete, this TTP will uninstall the nmap scanner.

Specify a particular port to scan:

```bash
ttpforge run forgearmory//reconnaissance/scanning-ip-blocks/ttp.yaml \
  --arg ip_range=10.0.0.244/32 \
  --arg ports=80
```

Scan the list of default ports across the 10.0.0.0/24 CIDR range:

```bash
ttpforge run forgearmory//reconnaissance/scanning-ip-blocks/ttp.yaml \
  --arg ip_range=10.0.0.0/24
```

## Steps

1. **confirm-required-tools-installed**: Identifies the operating system
   and confirms that the appropriate package manager is installed.
   After, checks to confirm that the nmap scanner is installed. If not, the
   scanner will be installed.

1. **run-scan**: Runs the nmap scanner against the supplied IP address
   block and prints the results to stdout.
