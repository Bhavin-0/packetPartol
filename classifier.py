# classifier.py

def classify_packet(packet):
    if packet.haslayer('TCP'):
        dport = packet['TCP'].dport
        if dport == 80 or dport == 443:
            return "Web Traffic"
        elif dport == 22:
            return "SSH Traffic"
        elif dport == 53:
            return "DNS Traffic"
        else:
            return "Other TCP Traffic"

    elif packet.haslayer('UDP'):
        dport = packet['UDP'].dport
        if dport == 53:
            return "DNS Traffic"
        else:
            return "Other UDP Traffic"

    return "Unknown Traffic"
