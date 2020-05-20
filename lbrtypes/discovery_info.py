from canoser import Struct
from lbrtypes.account_address import AccountAddress
from crypto.x25519 import PublicKey

class DiscoveryInfo(Struct):
    _fields = [
        ("account_address", AccountAddress),
        ("validator_network_identity_pubkey", PublicKey),
        ("validator_network_address", Multiaddr),
        ("fullnodes_network_identity_pubkey", PublicKey),
        ("fullnodes_network_address", Multiaddr)
    ]