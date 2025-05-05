# utils.py

def get_protocol_name(proto_num):
    protocols = {
        6: "TCP",
        17: "UDP"
    }
    return protocols.get(proto_num, f"Unknown({proto_num})")
