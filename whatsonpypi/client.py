# -*- coding: utf-8 -*-

"""
API client
"""
from __future__ import unicode_literals  # unicode support for py2

from requests import Request, Session, hooks
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .constants import PYPI_BASE_URL
from .exceptions import PackageNotProvidedError, PackageNotFoundError


class WoppResponse(object):
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
    def name(self):
        return self.info.get('name')

    @property
    def latest_version(self):
        return self.info.get('version')

    @property
    def summary(self):
        return self.info.get('summary')

    @property
    def description(self):
        return self.info.get('description')

    @property
    def homepage(self):
        return self.info.get('home_page')

    @property
    def pypi_url(self):
        return self.info.get('project_url') or self.info.get('package_url')

    @property
    def project_urls(self):
        return self.info.get('project_urls')

    @property
    def requires_python(self):
        return self.info.get('requires_python')

    @property
    def license(self):
        return self.info.get('license')

    @property
    def author(self):
        return self.info.get('author')

    @property
    def author_email(self):
        return self.info.get('author_email')

    @property
    def releases(self):
        # todo : tail or head for latest or oldest releases
        release_content = self.content.get('releases')
        return list(release_content.keys()) if release_content else []


class WoppClient(object):
    """
    Client for accessing the PyPI API
    """

    def __init__(self, pool_connections=True, request_hooks=None):
        # client specific info goes here.
        self.base_url = PYPI_BASE_URL
        self.session = Session() if pool_connections else None
        # default_hooks() returns {'response': []}
        self.request_hooks = request_hooks or hooks.default_hooks()

    def request(self, package=None, version=None, timeout=3.1, max_retries=3, ):
        """
        Make a HTTP GET request with the provided params

        :param timeout: request timeout seconds
        :param max_retries: number of times to retry on failure
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
        # instantiate Request
        request = Request(**req_kwargs)
        # Applies session-level state such as cookies to your request
        prepared_request = session.prepare_request(request)

        # use the adapter for retries
        retries = Retry(
            total=max_retries,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        # and fire!
        response = session.send(
            prepared_request,
            timeout=timeout,
            allow_redirects=True,
        )

        if response.status_code == 404:
            raise PackageNotFoundError("Sorry, but that package couldn't be found on PyPI.")

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
            raise PackageNotProvidedError('A package name is needed to proceed.')

        if version is not None:
            url = "{}/{}/{}/json".format(self.base_url, package, version)
        else:
            url = "{}/{}/json".format(self.base_url, package)

        return url
