import requests
import json

url = "https://blinkit.com/v1/layout/search"

params = {
    "offset":12,
    "limit":12,
    "actual_query":"milk",
    "last_snippet_type":"product_card_snippet_type_2",
    "last_widget_type":"listing_container",
    "page_index":1,
    "q":"milk",
    "search_count":179,
    "search_method":"basic",
    "search_type":"type_to_search",
    "tab_position":0,
    "total_entities_processed":1,
    "total_pagination_items":179
}

headers = {
    "accept":"*/*",
    "app_client":"consumer_web",
    "app_version":"1010101010",
    "auth_key":"c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477",
    "device_id":"993b329e700dd1a2",
    "lat":"12.9694264",
    "lon":"77.7398991",
    "origin":"https://blinkit.com",
    "referer":"https://blinkit.com/s/?q=milk",
    "session_uuid":"c1ff064a-a460-4854-8ef2-04252c727410",
    "user-agent":"Mozilla/5.0",
    "cookie":"gr_1_deviceId=bff68f17-7e9f-4337-8335-7db70e79d27f; city=; _cfuvid=nRthNWVpaiSDgUnvaDtFS.PpAdc7TijJLd58UfMyNgE-1783280052.6147933-1.0.1.1-aNKSeyhTkHTGXjAPfD72KiX6h1YtZ6UdrYz05jJ571s; _gid=GA1.2.398251017.1783280060; gr_1_lat=12.9694264; gr_1_lon=77.7398991; gr_1_locality=3; gr_1_landmark=undefined; _ga_DDJ0134H6Z=GS2.2.s1783280060$o1$g1$t1783281958$j42$l0$h0; __cf_bm=ZUuDk8jcH62_ik8mC24coTHK8RZRUYIa7eSWYsP51R8-1783290778.2326295-1.0.1.1-HtHTbWA73IH9rwSdp_NjdN4uecR9CqLNfGB_5tIRjm0vIwux6hBi10sJUqZbT2mAwxjJ3poJO1.X_7dki0H6I6nwEeC6ExOIWRtm5qzeFlH1G4wf1aoE5deLSmdN2H_b; _gcl_au=1.1.1279004656.1783280060; _gat_UA-85989319-1=1; _ga=GA1.1.1606332193.1783280060; _ga_JSMJG966C7=GS2.1.s1783290785$o2$g1$t1783290786$j59$l0$h0"
}

cookies = {
    "gr_1_lat":"12.9694264",
    "gr_1_lon":"77.7398991"
}


response = requests.post(
    url,
    params=params,
    headers=headers,
    cookies=cookies
)

print(response.status_code)

if response.status_code == 200:
    print("SUCCESS")
    
    with open(
        "blinkit_response.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            response.json(),
            f,
            indent=4
        )

    print("Saved")
else:
    print(response.text[:500])