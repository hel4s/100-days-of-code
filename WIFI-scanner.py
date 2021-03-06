from scapy.all import Dot11, Dot11Beacon, Dot11Elt, sniff
from threading import Thread
import pandas
import time
import os

networks = pandas.DataFrame(
    columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"]
)
networks.set_index("BSSID", inplace=True)


def callback(packet):
    if packet.haslayer("Dot11Beacon"):
        # extract the MAC address of the network
        bssid = packet["Dot11"].addr2
        ssid = packet["Dot11Elt"].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"
        # extact network stats
        stats = packet["Dot11Beacon"].network_stats()
        # get the channel of the AP
        channel = stats.get("channel")
        # get the crypto
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)


if __name__ == "__main__":
    interface = "eth0"
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()
    # start sniffing
    sniff(prn=callback, iface=interface)
