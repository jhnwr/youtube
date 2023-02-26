from requests_cache import CachedSession
import time
from rich import print


def rm_character(char_id):
    response = session.get("https://rickandmortyapi.com/api/character/" + str(char_id))
    print(
        response.from_cache,
        response.created_at,
        response.expires,
        response.is_expired
    )

    return response.json()


if __name__ == "__main__":
    session = CachedSession("rmapi", backend="sqlite", expire_after=1)
    print(rm_character(42))
    print(rm_character(46))
    print(rm_character(46))
    print("\n".join(session.cache.urls))
    time.sleep(2)
    session.cache.remove_expired_responses()
    print("urls in cache:\n", "\n".join(session.cache.urls))
