from canoser import DelegateT, BytesT

ED25519_PRIVATE_KEY_LENGTH = 32
ED25519_PUBLIC_KEY_LENGTH = 32
ED25519_SIGNATURE_LENGTH = 64

class Ed25519PrivateKey(DelegateT):
    delegate_type = BytesT(ED25519_PRIVATE_KEY_LENGTH)

class Ed25519PublicKey(DelegateT):
    delegate_type = BytesT(ED25519_PUBLIC_KEY_LENGTH)

class Ed25519Signature(DelegateT):
    delegate_type = BytesT(ED25519_SIGNATURE_LENGTH)