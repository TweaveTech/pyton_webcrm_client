# Python Web CRM Client

This simple api client exposes a number of methods that allow you to fetch objects 
from WebCRM.

## Quickstart

```python
from webcrm_client.api import WebCrmAPI

my_token = 'your-token-from-webcrm'
api = WebCrmAPI(my_token)

for org in api.organisations:
	print(org.organisation_address)
```
