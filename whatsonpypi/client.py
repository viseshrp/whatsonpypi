"""
API client for querying PyPI JSON endpoints.
"""

from __future__ import annotations

from typing import Any, Optional, Literal

from requests import Request, Session, hooks
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .constants import PYPI_BASE_URL
from .exceptions import PackageNotFoundError, PackageNotProvidedError


class WoppResponse:
    """
    A structured wrapper for PyPI JSON API responses.
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
        return self.json.get("releases", []) or []

    @property
    def releases_pkg_info(self) -> dict[str, Any]:
        return self.json.get("releases_pkg_info", {}) or {}

    @property
    def latest_releases(self) -> list[str]:
        return self.releases[:5]


class WoppClient:
    """
    Synchronous client for accessing the PyPI JSON API.
    """

    def __init__(
        self,
        pool_connections: bool = True,
        request_hooks: Optional[dict[str, list[Any]]] = None,
    ) -> None:
        self.base_url: str = PYPI_BASE_URL
        self.session: Optional[Session] = Session() if pool_connections else None
        self.request_hooks: dict[str, list[Any]] = request_hooks or hooks.default_hooks()

    def request(
        self,
        package: Optional[str] = None,
        version: Optional[str] = None,
        timeout: float = 3.1,
        max_retries: int = 3,
    ) -> WoppResponse:
        """
        Sends a GET request to the PyPI API and returns a structured WoppResponse.

        :param package: The package name to query
        :param version: Optional version string
        :param timeout: Request timeout in seconds
        :param max_retries: Retry attempts for failed requests
        :return: WoppResponse object with parsed data
        :raises PackageNotProvidedError: if package is None
        :raises PackageNotFoundError: if the PyPI API returns 404
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
        request = Request(**req_kwargs)
        prepared_request = session.prepare_request(request)

        retries = Retry(
            total=max_retries,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        response = session.send(
            prepared_request,
            timeout=timeout,
            allow_redirects=True,
        )

        if response.status_code == 404:
            raise PackageNotFoundError

        cleaned = response.cleaned_json  # type: ignore[attr-defined]
        return WoppResponse(response.status_code, cleaned)

    def _build_url(
        self,
        package: Optional[str],
        version: Optional[str],
    ) -> str:
        """
        Construct a fully qualified PyPI API URL.

        :param package: The package name
        :param version: Optional version
        :return: URL string
        :raises PackageNotProvidedError: if package is None
        """
        if package is None:
            raise PackageNotProvidedError

        return (
            f"{self.base_url}/{package}/{version}/json"
            if version
            else f"{self.base_url}/{package}/json"
        )
