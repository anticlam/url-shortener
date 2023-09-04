Monday update:

**Settings:**
- Added the allowed hosts array to `.env`.
- Switched to `eval` in `DEBUG`.
- Added `load_dotenv` to `asgi`, `wsgi`.

**Base urls.py:**
- Switched to `LinkViewSet`.
- Switched to standard API url path convention.

**Shortener Model:** 
- Added a `db_table`.
- Moved the shorten link creation to the serializer.
- Switched the link fields to `charfield`.
- Added database indexing.

**Shortener Serializer:**
- Added URL validation and link creation logic.
- The URL is now generated with hashing and a random element.
- Added a simple cache for faster link retrieval.

**Shortener Views:**
- Added throttle.
- Added caching.
- Switched to `viewsets`.

**User Model:**
- Added a `db_table`
- Switched to `AbstractBaseUser`.
- Added database indexing.

**User Serializer:**
- Added hashed cache for retrieving emails for validation.
- Removed username field as a requirement.

**User urls:**
- Switched to `DRF` router.

**User Views:**
- Switched to `viewsets`.

- Most importantly, all using PEP8 formatting (I think)

URL shortener api with custom user authentication using Django and DRF. Unregistered users can use shortened URLs but cannot create them unless they register and log in.

Credits: @jod35 @OtchereDev

