import secrets
import time


CROCKFORD_BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
ULID_LENGTH = 26


def generate_ulid() -> str:
    """Generate a 26-character ULID string."""
    timestamp_ms = int(time.time() * 1000)
    randomness = secrets.randbits(80)
    value = (timestamp_ms << 80) | randomness

    chars = []
    for _ in range(ULID_LENGTH):
        chars.append(CROCKFORD_BASE32[value & 0b11111])
        value >>= 5

    return "".join(reversed(chars))
