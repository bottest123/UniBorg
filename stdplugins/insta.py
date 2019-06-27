
import aiohttp
import time
from datetime import tzinfo, datetime
from uniborg.util import admin_cmd

apikey= "gJsZ7jenunpxezRbN0FQ4cNCP"


@borg.on(admin_cmd("ig (.*)"))
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://rest.farzain.com/api/ig_profile.php?id={}&apikey={}"
    input_str = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str, Config.rapikey))
    response_api = await response_api_zero.json()
    if response_api["cod"] == 200:
        await event.edit(
            """**{}**
**Name:** {}
**Username:** {}
**URL:** {}
**Bio:** {}
**Followers:** {}
**Following:** {}
**Post:** {}
**Profile Picture:**  {}  {}""".format(
                input_str,               
                response_api["info"]["full_name"],
                response_api["info"]["username"],
                response_api["info"]["url_bio"],
                response_api["info"]["bio"],
                response_api["count"]["followers"],
                response_api["count"]["following"],
                response_api["count"]["post"],
                response_api["info"]["profile_pict"]
            )
        )
    else:
        await event.edit(  
            """**{}**
**Name:** {}
**Username:** {}
**URL:** {}
**Bio:** {}
**Followers:** {}
**Following:** {}
**Post:** {}
**Profile Picture:**  {}  {}""".format(
                input_str,               
                response_api["info"]["full_name"],
                response_api["info"]["username"],
                response_api["info"]["url_bio"],
                response_api["info"]["bio"],
                response_api["count"]["followers"],
                response_api["count"]["following"],
                response_api["count"]["post"],
                response_api["info"]["profile_pict"]
            )
        )