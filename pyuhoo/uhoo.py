import codecs
import hashlib
import json

from Crypto.Cipher import AES

from .api import API
from .const import _LOG, CLIENT_ID


def _json_pp(obj):
    return json.dumps(obj, sort_keys=True, indent=2, separators=(",", ": "))


class uHoo(object):
    def __init__(self):
        self._api = API()
        self._auth_token = None

        self._app_version = 93
        self._client_id = CLIENT_ID

    def _pad(self, pt):
        BS = 16  # block size
        return pt + (BS - len(pt) % BS) * chr(BS - len(pt) % BS)

    def _salted_hash(self, password, u_id):
        salt = b"@uhooinc.com"
        salted_hash = hashlib.sha256()
        salted_hash.update(bytes(u_id, "utf-8") + bytes(password, "utf-8") + salt)
        hexdigest = salted_hash.hexdigest()
        return hexdigest

    def _encrypt_hash(self, code, pt_hash):
        code_hash = hashlib.md5()
        code_hash.update(bytes(code, "utf-8"))
        code_hash_hex = code_hash.hexdigest()

        key = codecs.decode(code_hash_hex, "hex")

        pt_hash_padded = self._pad(pt_hash)

        cipher = AES.new(key, AES.MODE_ECB)
        ct = cipher.encrypt(pt_hash_padded)
        return codecs.encode(ct, "hex")

    def login(self, username, password):
        app_must_update = self._api.app_must_update(self._app_version)
        if app_must_update:
            _LOG.debug(f"[login] need to update app version")

        user_config = self._api.user_config()
        _LOG.debug(f"[user_config] returned\n{_json_pp(user_config)}")
        u_id = user_config["uId"]

        user_verify_email = self._api.user_verify_email(username, self._client_id)
        _LOG.debug(f"[user_verify_email] returned\n{_json_pp(user_verify_email)}")
        code = user_verify_email["code"]
        id = user_verify_email["id"]

        salted_hash = self._salted_hash(password, u_id)
        _LOG.debug(f"[login] using salted hash {salted_hash}")

        encrypted_hash = self._encrypt_hash(code, salted_hash)
        _LOG.debug(f"[login] using encrypted hash {encrypted_hash}")

        user_login = self._api.user_login(username, encrypted_hash, id)
        _LOG.debug(f"[user_login] returned\n{_json_pp(user_login)}")

        refresh_token = user_login["refreshToken"]
        self._api.set_auth_token(refresh_token)

        return True
