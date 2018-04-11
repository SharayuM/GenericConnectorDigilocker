import hashlib
import time

def encrypt_string(format_iso_now):
	hash_string="SRSvpVGVsKqQeZ3Qm5yDH8T"+format_iso_now
	my_str_as_bytes = str.encode(hash_string)
	sha_signature=hashlib.sha256(my_str_as_bytes).hexdigest()

	return sha_signature
