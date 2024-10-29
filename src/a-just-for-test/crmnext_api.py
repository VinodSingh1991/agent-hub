import requests


def getListPayLoad():
    return {
        "LookUpRequest": {"ControlKey": "CustomView_3"},
        "ListingRequest": {
            "ContentFilter": {
                "PageIndex": 1,
                "PageSize": 100,
                "ABCFilter": "All",
                "OrderBy": "DESC",
                "OrderField": "CaseID"
            }
        },
        "RequestMode": 0
    }

class APITool:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_request(self, endpoint, data, headers=None):
        """
        Sends a POST request to the given endpoint with the provided data and headers.

        Parameters:
        - endpoint (str): The API endpoint (path) to which the request is sent.
        - data (dict): The data to send in the POST request.
        - headers (dict, optional): Additional headers for the request.

        Returns:
        - dict: The JSON response from the API or an error message.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raises an error for bad HTTP status
            return response.json()  # Returns JSON response as a Python dictionary
        except requests.exceptions.RequestException as e:
            # Handle errors, e.g., network issues, bad status codes
            return {"error": str(e)}


# Example Usage:
if __name__ == "__main__":
    api_tool = APITool(base_url="http://localhost:5003/mydevapp/DomainLookup")
    endpoint = "LoadCustomView?x=g4zhyfd7lwfzmnq669sgqqa7sz"
    data = getListPayLoad()
    headers = {"Authorization": "Bearer YOUR_TOKEN", "Content-Type": "application/json"}

    response = api_tool.post_request(endpoint, data, headers)
    print(response)



