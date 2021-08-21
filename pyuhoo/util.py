"""Define various utility functions."""
import json
from codecs import decode, encode
from hashlib import md5, sha256
from typing import Any, cast

from Crypto.Cipher import AES
from Crypto.Cipher._mode_ecb import EcbMode
from Crypto.Util.Padding import pad


def json_pp(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, separators=(",", ": "))


def salted_hash(password: str, u_id: str) -> str:
    salt: bytes = b"@uhooinc.com"
    salted_hash = sha256()
    salted_hash.update(bytes(u_id, "utf-8") + bytes(password, "utf-8") + salt)
    hexdigest: str = salted_hash.hexdigest()
    return hexdigest


def encrypted_hash(code: str, pt_hash: str) -> str:
    code_hash = md5()
    code_hash.update(bytes(code, "utf-8"))
    code_hash_hex: str = code_hash.hexdigest()

    key: bytes = decode(bytes(code_hash_hex, "utf-8"), "hex")

    pt_hash_padded: bytes = pad(bytes(pt_hash, "utf-8"), 16)

    cipher: EcbMode = cast(EcbMode, AES.new(key, AES.MODE_ECB))
    ct: bytes = cipher.encrypt(pt_hash_padded)
    return str(encode(ct, "hex"), "utf-8")
