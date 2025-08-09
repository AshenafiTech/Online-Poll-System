from django.urls import get_resolver

print("\nRegistered URL names:")
for url_pattern in get_resolver().reverse_dict.keys():
    if isinstance(url_pattern, str):
        print(url_pattern)
