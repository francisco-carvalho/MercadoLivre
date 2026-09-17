from requests.exceptions import HTTPError

from api import search_items


try:
    results = search_items(
        site_id="MLA",
        query="Samsung Galaxy S25",
        limit=50,
        offset=0,
    )

    print(f"Total found: {results['paging']['total']}")
    print(f"Records returned: {len(results['results'])}")

    print("\nFirst item:")
    print(results["results"][0])

except HTTPError as error:
    print(f"HTTP error: {error}")
    #print(f"Response body: {error.response.text}")