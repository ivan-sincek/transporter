# Transporter

Send packets through raw sockets (requires administrative privileges).

Tested on Kali Linux v2023.1 (64-bit).

Made for network testing purposes. I hope it will help!

## How to Run

Open your preferred console from [/src/](https://github.com/ivan-sincek/transporter/tree/master/src) and run the commands shown below.

Install required packages:

```fundamental
pip3 install -r requirements.txt
```

Run the script:

```fundamental
python3 transporter.py
```

## ICMP Ping

Packet file needs to be encoded in hexadecimal format as shown below. All spacing will be stripped.

```fundamental
Ethernet II frame
  1 - destination - 6 B - \x00\x00\x00\x00\x00\x00 - set destination MAC address
  2 - source      - 6 B - \x00\x00\x00\x00\x00\x00 - set source MAC address
  3 - type        - 2 B - \x08\x00                 - IPv4
Total: 14 B

IPv4 packet
  1 - header length           - 1 B - \x45             - 20 B
  2 - differentiated services - 1 B - \x00
  3 - total length            - 2 B - \x00\x00         - calculate
  4 - identification          - 2 B - \x00\x00         - optional
  5 - fragment offset         - 2 B - \x40\x00         - don't fragment
  6 - time to live            - 1 B - \x40             - 64 hops
  7 - protocol                - 1 B - \x01             - ICMP
  8 - header checksum         - 2 B - \x00\x00         - optional
  9 - source                  - 4 B - \x00\x00\x00\x00 - set source IP address
 10 - destination             - 4 B - \x00\x00\x00\x00 - set destination IP address
Total: 20 B

ICMP packet
  1 - type            - 1 B - \x08                             - echo
  2 - code            - 1 B - \x00                             - ICMP subtype
  3 - checksum        - 2 B - \x00\x00                         - calculate
  4 - identifier      - 2 B - \x00\x00                         - optional
  5 - sequence number - 2 B - \x00\x00                         - optional
  6 - timestamp       - 8 B - \x00\x00\x00\x00\x00\x00\x00\x00 - not required
  7 - data
Total: 8 | 16 B
```

Maximum IPv4 packet size is 65535 B.

Maximum non-fragmented ICMP packet size is 1500 B.

## Command and Control Over ICMP

Because firewalls can block reverse and bind TCP connections, it is possible to control your shell over ICMP if the ICMP traffic is permitted.

Search the Internet for additional information.

## Usage

```fundamental
Transporter v2.5 ( github.com/ivan-sincek/transporter )

Usage:   python3 transporter.py -i interface -p protocol -f file       [-o out         ]
Example: python3 transporter.py -i eth0      -p 0        -f packet.txt [-o response.txt]

DESCRIPTION
    Send packets through raw sockets
INTERFACE
    Network interface to use
    -i <interface> - eth0 | wlan0 | etc.
PROTOCOL
    Network protocol to use
    Use '0' for ICMP
    Use '6' for TCP
    Use '7' for UDP
    Search web for additional network protocol numbers
    -p <protocol> - 0 | 6 | 17 | etc.
FILE
    File with the packet to send
    -f <file> - packet.txt | etc.
OUT
    Output file
    -o <out> - response.txt | etc.
```
