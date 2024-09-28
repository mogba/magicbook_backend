import os
from supabase import create_client, Client
from supabase.client import ClientOptions

_url: str = os.environ.get("SUPABASE_URL")
_key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(_url, _key,
  options=ClientOptions(
    postgrest_client_timeout=10,
    storage_client_timeout=10,
    schema="public",
  ))

SUPABASE_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('SUPABASE_DB_NAME'),
    'USER': os.environ.get('SUPABASE_DB_USER'),
    'PASSWORD': os.environ.get('SUPABASE_DB_PASSWORD'),
    'HOST': os.environ.get('SUPABASE_DB_HOST'),
    'PORT': os.environ.get('SUPABASE_DB_PORT'),
}
