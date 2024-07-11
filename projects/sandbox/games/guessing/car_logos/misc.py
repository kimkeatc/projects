
import string


def get_alphabets(*, alphabets: list = []) -> list:
    alphabets = string.ascii_lowercase
    alphabets = list(alphabets)
    return alphabets


def get_headers(headers: dict = {}) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    return headers
