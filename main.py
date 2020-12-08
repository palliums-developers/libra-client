import bech32
from libra_client.canoser import hex_to_int_list
# code = "lbr1p7ujcndcl7nudzwt8fglhx6wxn08kgs5tm6mz4usw5p72t"

# def segwit_scriptpubkey(witver, witprog):
#     """Construct a Segwit scriptPubKey for a given witness program."""
#     print(bytes(witprog).hex()[:32])
#     return bytes([witver + 0x50 if witver else 0, len(witprog)] + witprog)
#
# # data = "tlb1pgc28wuxspzzmvghzen74dczc8a3y46c9y0xeq7g9g63ya"
# #
# # # value = "f72589b71ff4f8d139674a3f7369c69bcf64428bdeb62af2"
# # #
# # # value = bech32.encode("tlb", 1, hex_to_int_list(value))
# # # print(value)
# #
# # ver, prog = bech32.decode("tlb", data)
# # # print(prog)
# # segwit_scriptpubkey(ver, prog).hex()
#
addr = "00000000000000000000000042414e4b"
print(addr.upper())


