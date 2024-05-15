import json
import os
from sentinelhub import SentinelHubRequest, MimeType, DataCollection, CRS, BBox

def get_true_color_image(bbox, time_interval):
    with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
        config_dict = json.load(f)

    evalscript_true_color = """
    //VERSION=3
    function setup() {
        return {
            input: ["B04", "B03", "B02"],
            output: { bands: 3 }
        }
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
    """

    request = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=time_interval,
                mosaicking_order="leastCC",
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=BBox(bbox, crs=CRS.WGS84),
        size=(512, 512),
        **config_dict,
    )

    config = SentinelHubConfig(**config_dict)
    client = SentinelHubDownloadClient(config)

    return client.download_data(request)