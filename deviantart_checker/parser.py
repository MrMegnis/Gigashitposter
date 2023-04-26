from deviantart_python_api.deviant_art import DeviantArt

da = DeviantArt("24178", "7b472c20aea66646e9f9219c6c3da2c9")


def get_tag_last_deviant_id(tag):
    deviant = da.browse_tag(tag, limit=1)
    # print(deviant)
    return deviant["results"][0]["deviationid"]
