import os
from scapy.all import sniff
from classifier import classify_packet

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)
log_file = open("logs/packets.log", "a")

def process_packet(packet):
    classification = classify_packet(packet)
    log_entry = f"{packet.summary()} --> {classification}\n"
    print(log_entry.strip())
    log_file.write(log_entry)
    log_file.flush()

print("Starting PacketPatrol network traffic monitoring... Press Ctrl+C to stop.")
sniff(prn=process_packet, store=0)
