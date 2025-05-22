"""
API client
"""

from typing import Any, Optional

from requests import Request, Session, hooks
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .constants import PYPI_BASE_URL
from .exceptions import PackageNotFoundError, PackageNotProvidedError


class WoppResponse:
    """
    Serializer for the response from PyPI
    """

    def __init__(self, status_code: int, json: dict[str, Any]) -> None:
        self.status_code = status_code
        self.json = json
        self.ok = self.status_code < 400

    @property
    def name(self) -> Optional[str]:
        return self.json.get("name")

    @property
    def latest_version(self) -> Optional[str]:
        return self.json.get("latest_version")

    @property
    def summary(self) -> Optional[str]:
        return self.json.get("summary")

    @property
    def homepage(self) -> Optional[str]:
        return self.json.get("homepage")

    @property
    def package_url(self) -> Optional[str]:
        return self.json.get("package_url")

    @property
    def project_urls(self) -> dict[str, str]:
        return self.json.get("project_urls", {}) or {}

    @property
    def project_docs(self) -> Optional[str]:
        return self.project_urls.get("Documentation") or self.homepage

    @property
    def requires_python(self) -> Optional[str]:
        return self.json.get("requires_python")

    @property
    def license(self) -> Optional[str]:
        return self.json.get("license")

    @property
    def author(self) -> Optional[str]:
        return self.json.get("author")

    @property
    def author_email(self) -> Optional[str]:
        return self.json.get("author_email")

    @property
    def latest_release_url(self) -> Optional[str]:
        return self.json.get("latest_release_url")

    @property
    def dependencies(self) -> list[str]:
        return self.json.get("dependencies", []) or []

    @property
    def latest_pkg_urls(self) -> dict[str, str]:
        return self.json.get("latest_pkg_urls", {}) or {}

    @property
    def releases(self) -> list[str]:
        # all releases
        return self.json.get("releases", []) or []

    @property
    def releases_pkg_info(self) -> dict[str, Any]:
        # info of every release's package
        return self.json.get("releases_pkg_info", {}) or {}

    @property
    def latest_releases(self) -> list[str]:
        # last 5 releases
        return self.releases[:5]


class WoppClient:
    """
    Client for accessing the PyPI API
    """

    def __init__(self, pool_connections: bool = True, request_hooks: Any = None) -> None:
        self.base_url = PYPI_BASE_URL
        self.session = Session() if pool_connections else None
        # default_hooks() returns {'response': []}
        self.request_hooks = request_hooks or hooks.default_hooks()

    def request(
        self,
        package: Optional[str] = None,
        version: Optional[str] = None,
        timeout: float = 3.1,
        max_retries: int = 3,
    ) -> WoppResponse:
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
            "method": "GET",
            "url": url,
            "hooks": self.request_hooks,
            "headers": {
                "Accept": "application/json",
                "User-Agent": "https://github.com/viseshrp/whatsonpypi",
            },
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
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # and fire!
        response = session.send(
            prepared_request,
            timeout=timeout,
            allow_redirects=True,
        )

        if response.status_code == 404:
            raise PackageNotFoundError

        # serialize response
        wopp_response = WoppResponse(int(response.status_code), response.cleaned_json)
        return wopp_response

    def _build_url(
        self,
        package: Optional[str] = None,
        version: Optional[str] = None,
    ) -> str:
        """
        Builds the URL with the path params provided.

        :param package: name of package
        :param version: version of package
        :return: fully qualified URL
        """
        if package is None:
            raise PackageNotProvidedError

        url = (
            f"{self.base_url}/{package}/{version}/json"
            if version is not None
            else f"{self.base_url}/{package}/json"
        )

        return url
