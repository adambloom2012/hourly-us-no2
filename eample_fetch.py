from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
# Your client credentials
client_id = ''
client_secret = ''

# Create a session
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Get token for the session
token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
                          client_secret=client_secret, include_client_id=True)

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

request = {
    "input": {
        "bounds": {
            "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -94.04798984527588,
                            41.7930725281021,
                        ],
                        [
                            -94.04803276062012,
                            41.805773608962866,
                        ],
                        [
                            -94.06738758087158,
                            41.805901566741305,
                        ],
                        [
                            -94.06734466552734,
                            41.7967199475024,
                        ],
                        [
                            -94.06223773956299,
                            41.79144072064381,
                        ],
                        [
                            -94.0504789352417,
                            41.791376727347966,
                        ],
                        [
                            -94.05039310455322,
                            41.7930725281021,
                        ],
                        [
                            -94.04798984527588,
                            41.7930725281021,
                        ],
                    ]
                ],
            },
        },
        "data": [
            {
                "type": "sentinel-2-l2a",
                "dataFilter": {
                    "timeRange": {
                        "from": "2022-10-01T00:00:00Z",
                        "to": "2022-10-31T00:00:00Z",
                    }
                },
                "processing": {"harmonizeValues": "false"},
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

# save response as geoTIFF if 200
if response.status_code == 200:
    with open("exac_match.tiff", "wb") as f:
        f.write(response.content)
# print error message if not 200
else:
    print(f"Error: {response.status_code}")
    print(response.text)