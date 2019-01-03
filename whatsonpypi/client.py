"""
API client
"""
from requests import Request, Session, hooks

from .constants import PYPI_BASE_URL
from .exceptions import PackageAbsentException


class WoppResponse:
    """
    Serializer for the response from PyPI
    """

    def __init__(self, status_code, json_content):
        self.status_code = status_code
        self.content = json_content
        self.ok = self.status_code < 400

    @property
    def info(self):
        return self.content.get('info')

    @property
    def latest_version(self):
        return self.info.get('version')


class WoppClient:
    """
    Client for accessing the PyPI API
    """

    def __init__(self, pool_connections=True, request_hooks=None):
        # client specific info goes here.
        self.base_url = PYPI_BASE_URL
        self.session = Session() if pool_connections else None
        # default_hooks() returns {'response': []}
        self.request_hooks = request_hooks or hooks.default_hooks()

    def request(self, timeout=3.1, package=None, version=None):
        """
        Make a HTTP GET request with the provided params

        :param timeout: request timeout seconds
        :param package: name of the python package to search
        :param version: version of the python package to search
        :return: response serialized by WoppResponse object
        """
        url = self._build_url(package, version)

        req_kwargs = {
            'method': 'GET',
            'url': url,
            'hooks': self.request_hooks,
        }

        session = self.session or Session()
        request = Request(**req_kwargs)
        # Applies session-level state such as cookies to your request
        prepared_request = session.prepare_request(request)
        response = session.send(
            prepared_request,
            timeout=timeout,
        )
        # serialize response
        wopp_response = WoppResponse(int(response.status_code), response.json())
        return wopp_response

    def _build_url(self, package=None, version=None):
        """
        Builds the URL with the path params provided.

        :param package: name of package
        :param version: version of package
        :return: fully qualified URL
        """
        if package is None:
            raise PackageAbsentException('A package name is needed to proceed.')

        if version is not None:
            url = "{}/{}/{}/json".format(self.base_url, package, version)
        else:
            url = "{}/{}/json".format(self.base_url, package)

        return url
