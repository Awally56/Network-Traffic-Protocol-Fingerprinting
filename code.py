from scapy.all import sniff, IP, TCP, UDP, Raw
import socket
import struct
import time

def protocol_name(proto_num):
    proto_map = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        47: "GRE",
        50: "ESP",
        51: "AH",
        89: "OSPF"
    }
    return proto_map.get(proto_num, f"Unknown({proto_num})")

def port_to_service(port):
    services = {
        20: "FTP-DATA",
        21: "FTP",
        22: "SSH",
        23: "TELNET",
        25: "SMTP",
        53: "DNS",
        67: "DHCP",
        68: "DHCP",
        80: "HTTP",
        110: "POP3",
        143: "IMAP",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S"
    }
    return services.get(port, "Unknown")

def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        proto = protocol_name(ip_layer.proto)
        print(f"\n[IP] {ip_layer.src} -> {ip_layer.dst} | Protocol: {proto}")

        if TCP in packet:
            tcp_layer = packet[TCP]
            service = port_to_service(tcp_layer.dport)
            print(f"[TCP] {tcp_layer.sport} -> {tcp_layer.dport} | Service: {service}")
            if Raw in packet:
                payload = packet[Raw].load[:50]
                print(f"[Payload] {payload}")

        elif UDP in packet:
            udp_layer = packet[UDP]
            service = port_to_service(udp_layer.dport)
            print(f"[UDP] {udp_layer.sport} -> {udp_layer.dport} | Service: {service}")
            if Raw in packet:
                payload = packet[Raw].load[:50]
                print(f"[Payload] {payload}")

def start_sniffing():
    print("Starting protocol fingerprinting...")
    sniff(prn=packet_callback, store=0, count=50)

if __name__ == "__main__":
    start_sniffing()
