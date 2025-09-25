from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

evalscript = """
//VERSION=3
function setup() {
  return {
    input: [
      {
        bands: [
          "B01",
          "B02",
          "B03",
          "B04",
          "B05",
          "B06",
          "B07",
          "B08",
          "B8A",
          "B09",
          "B11",
          "B12",
        ],
        units: "DN",
      },
    ],
    output: {
      id: "default",
      bands: 12,
      sampleType: SampleType.UINT16,
    },
  }
}

function evaluatePixel(sample) {
  return [
    sample.B01,
    sample.B02,
    sample.B03,
    sample.B04,
    sample.B05,
    sample.B06,
    sample.B07,
    sample.B08,
    sample.B8A,
    sample.B09,
    sample.B11,
    sample.B12,
  ]
}
"""

def get_sentinel_data(
        client_id: str,
        client_secret: str,
        gdf,  # GeoDataFrame with 'bbox' column ) -> None:
) -> None:
    # Create a session
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                          client_secret=client_secret, include_client_id=True)
    for site_id, geometry in zip(gdf['Site Num'], gdf['bbox']):
        request = {
            "input": {
                "bounds": {
                    "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                    "bbox" : geometry
                },
                "data": [
                    {
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": "2024-01-01T00:00:00Z",
                                "to": "2024-12-31T00:00:00Z",
                            }
                        },
                        "processing" : {
                            "upsampling": "BILINEAR",
                            "downsampling": "BILINEAR"
                        }
                    }
                ],
            },
    "output": {
        "width": 120,
        "height": 120,
        "responses": [
            {
                "identifier": "default",
                "format": {"type": "image/tiff"},
            }
        ],
    },
            "evalscript": evalscript,
        }

        url = "https://sh.dataspace.copernicus.eu/api/v1/process"
        response = oauth.post(url, json=request)

        # process response
        # save response as geoTIFF if 200
        if response.status_code == 200:
            with open("exac_match.tiff", "wb") as f:
                f.write(response.content)
        # print error message if not 200
        else:
            print(f"Error: {response.status_code}")
            print(response.text)