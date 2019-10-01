import requests


class SkillsClassificationConnection(object):
    """
    Handles the connection to the Emsi Skills Classification API
    Provides simple functions on the various endpoints in the rest API

    Attributes:
        client_id (str): the user's client id for connecting to the API
        client_secret (str): the user's client secret for connecting to the API
        token (str): a token (valid for 1 hour) that grants access to the skills API
    """

    def __init__(self, client_id, client_secret):
        """
        Generate a token and validate that the user has access to the skills API

        Args:
            client_id (str): the user's client id for connecting to the API
            client_secret (str): the user's client secret for connecting to the API
        """
        self.client_id = client_id
        self.client_secret = client_secret

        self.token = self.get_auth_token()
        assert(self.is_valid_token())

    def get_auth_token(self):
        """
        Get an auth token from the emsi auth server. Token is valid for one hour.

        Returns:
            str: token string for using in skills requests
        """
        url = "https://auth.emsicloud.com/connect/token"

        payload = "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope=emsi_open".format(
            client_id = self.client_id,
            client_secret = self.client_secret
        )
        headers = {
            'content-type': "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.json()['access_token']

    def is_valid_token(self):
        """Checks the user's permissions to ensure that the token is still valid

        Returns:
            bool: returns True if the token is valid, otherwise False
        """
        url = "https://skills.emsicloud.com/versions"
        headers = {'authorization': 'Bearer {}'.format(self.token)}
        response = requests.request("GET", url, headers=headers)

        return response.status_code == 200

    def download_data(self, skills_endpoint, payload = None, querystring = None):
        """Function for hanlding the various requests that can be made to the Skills Classification API

        Args:
            skills_endpoint (str): the endpoint specific to the skills API e.g. `versions` for a list of the skills versions available in the API
            payload (None, optional): a json object is expected that will be passed to the API for POST requests
            querystring (None, optional): a json object is expected that will be passed to the API for get requests as part of the `params`

        Returns:
            response: requests response object from the API
        """
        url = "https://skills.emsicloud.com/" + skills_endpoint
        headers = {'authorization': 'Bearer {}'.format(self.token)}

        # if both the payload and querystring are None, then we make a simple get request
        if payload is None and querystring is None:
            response = requests.request("GET", url, headers=headers)
        # if we get a querystring object though, then we pass it to the API as part of a GET request
        elif querystring is not None:
            response = requests.request("GET", url, headers=headers, params=querystring)
        # if we get a payload object, then we use it as the body of a POST request
        elif payload is not None:
            response = requests.request("POST", url, headers=headers, json=payload)

        if response.status_code != 200:
            if not self.is_valid_token():
                self.token = self.get_auth_token()
                return self.download_data(skills_endpoint, payload)

        return response

    def list_versions(self):
        """Get the versions available in the API

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions"
        response = self.download_data(endpoint)

        return response

    def list_all_skills(self, version = 'latest'):
        """Get the full list of skills in the API

        Args:
            version (str, optional): Defaults to 'latest', which tells the API to use the latest version available

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions/{}/skills".format(version)
        response = self.download_data(endpoint)

        return response

    def search_skills(self, search_string = None, type_id = None, version = 'latest'):
        """Search for skills based on a search string or the type of skill (e.g. hard skill, soft skill, certification)

        Args:
            search_string (str, optional): the string to use when searching for a skill by name
            type_id (str, optional): the skill type id (see list_skill_types for a further breakdown)
            version (str, optional): Defaults to 'latest', which tells the API to use the latest version available

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions/{}/skills".format(version)
        querystring = {}
        assert(search_string is not None or type_id is not None)

        if search_string is not None:
            querystring['q'] = search_string
        if type_id is not None:
            querystring['typeId'] = type_id

        response = self.download_data(endpoint, querystring = querystring)

        return response

    def get_skill_by_id(self, skill_id, version = 'latest'):
        """Get the information for a particular skill based solely on its id

        Args:
            skill_id (str): Description
            version (str, optional): Defaults to 'latest', which tells the API to use the latest version available

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions/{}/skills/{}".format(version, skill_id)
        response = self.download_data(endpoint)

        return response

    def list_skill_types(self, version = 'latest'):
        """Get a list of the types of skills available (hard skills, soft skills, certifications) as well as the skill type ids

        Args:
            version (str, optional): Defaults to 'latest', which tells the API to use the latest version available

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions/{}/types".format(version)
        response = self.download_data(endpoint)

        return response

    def extract_skills(self, search_string, version = 'latest'):
        """Returns a list of skills found in a document. Document must be UTF-8 encoded.

        Note that this endpoint has a free tier monthly quota of 50 requests. Contact us if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, X-Rate-Limit-Remaining and X-Rate-Limit-Reset, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.

        Args:
            search_string (str): freeform text of a job posting, resume, etc to be tagged
            version (str, optional): Defaults to 'latest', which tells the API to use the latest version available

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions/{}/extract".format(version)
        payload = {"full_text": search_string}
        response = self.download_data(endpoint, payload = payload)

        return response

    def extract_skills_with_source(self, search_string, version = 'latest'):
        """
        Returns a list of skills found in a document. Document must be UTF-8 encoded.
        Returns additional trace information which exposes indices into the source document where skill related words were found.
        Indices are byte offsets indicating where each word was found in the document.

        Note that this endpoint has a free tier monthly quota of 50 requests. Contact us if you'd like this increased or made unlimited. Responses from this endpoint will include two headers, X-Rate-Limit-Remaining and X-Rate-Limit-Reset, which indicate how many requests you have remaining in your current quota period and when that quota will reset, respectively.

        Args:
            search_string (str): freeform text of a job posting, resume, etc to be tagged
            version (str, optional): Defaults to 'latest', which tells the API to use the latest version available

        Returns:
            response: requests type response from the API
        """
        endpoint = "versions/{}/extract?trace=true".format(version)
        payload = {"full_text": search_string}
        response = self.download_data(endpoint, payload = payload)

        return response
