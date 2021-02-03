import email_normalize

from asgiref.sync import async_to_sync


@async_to_sync
async def normalize_email(email_address: str) -> email_normalize.Result:
    normalizer = email_normalize.Normalizer()
    return await normalizer.normalize(email_address)