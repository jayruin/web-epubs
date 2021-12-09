import hashlib
from hmac import compare_digest

import pytest

from plugins.hash.multi_hash import MultiHash


@pytest.fixture
def hash_data() -> bytes:
    return b"abc"


def test_single_algorithm(hash_data: bytes):
    md5 = hashlib.md5()
    multi_hash = MultiHash(["md5"])
    md5.update(hash_data)
    multi_hash.update(hash_data)
    assert compare_digest(md5.hexdigest(), multi_hash.hexdigest()["md5"])
    assert compare_digest(md5.digest(), multi_hash.digest()["md5"])


def test_two_algorithms(hash_data: bytes):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    multi_hash = MultiHash(["md5", "sha1"])
    md5.update(hash_data)
    sha1.update(hash_data)
    multi_hash.update(hash_data)
    assert compare_digest(md5.hexdigest(), multi_hash.hexdigest()["md5"])
    assert compare_digest(md5.digest(), multi_hash.digest()["md5"])
    assert compare_digest(sha1.hexdigest(), multi_hash.hexdigest()["sha1"])
    assert compare_digest(sha1.digest(), multi_hash.digest()["sha1"])


def test_unsupported_algorithm():
    with pytest.raises(ValueError, match="Algorithm alg not supported!"):
        multi_hash = MultiHash(["alg"])
        multi_hash.update(b"alg")
