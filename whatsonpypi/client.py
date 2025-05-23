"""
API client for querying PyPI JSON endpoints.
"""

from __future__ import annotations

from datetime import datetime
from operator import itemgetter
from typing import Any, TypeVar

from requests import Request, Session, hooks
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .constants import PYPI_BASE_URL
from .exceptions import PackageNotFoundError, PackageNotProvidedError

T = TypeVar("T")


class WoppResponse:
    """
    A structured wrapper for PyPI JSON API responses.
    """

    def __init__(self, status_code: int, json: dict[str, Any]) -> None:
        self.status_code: int = status_code
        self.json: dict[str, Any] = json
        self._cache: dict[str, Any] = {}

    def _get(self, key: str, expected_type: type[T], default: T) -> T:
        value = self.json.get(key, default)
        return value if isinstance(value, expected_type) else default

    @property
    def name(self) -> str:
        return self._get("name", str, "")

    @property
    def latest_version(self) -> str:
        return self._get("latest_version", str, "")

    @property
    def summary(self) -> str:
        return self._get("summary", str, "")

    @property
    def package_url(self) -> str:
        return self._get("package_url", str, "")

    @property
    def project_urls(self) -> dict[str, Any]:
        return self._get("project_urls", dict, {})

    @property
    def homepage(self) -> str:
        return self.project_urls.get("Homepage") or self._get("homepage", str, "")

    @property
    def project_docs(self) -> str:
        return self.project_urls.get("Documentation") or self.homepage

    @property
    def requires_python(self) -> str:
        return self._get("requires_python", str, "")

    @property
    def license(self) -> str:
        return self._get("license", str, "")

    @property
    def author(self) -> str:
        return self._get("author", str, "")

    @property
    def author_email(self) -> str:
        return self._get("author_email", str, "")

    @property
    def latest_release_url(self) -> str:
        return self._get("latest_release_url", str, "")

    @property
    def dependencies(self) -> list[str]:
        return self._get("dependencies", list, [])

    @property
    def latest_pkg_urls(self) -> dict[str, Any]:
        return self._get("latest_pkg_urls", dict, {})

    @property
    def releases(self) -> list[str]:
        value = self.json.get("releases")
        return list(value) if isinstance(value, list) else []

    @property
    def release_data(self) -> dict[str, dict[str, Any]]:
        return self._get("release_info", dict, {})

    def get_release_info(self, release: str) -> dict[str, Any]:
        """
        Returns the release information for a specific release version.
        """
        return self.release_data.get(release, {})

    def get_releases_with_dates(self) -> list[tuple[str, datetime]]:
        """
        Returns a list of releases with their upload dates.
        """
        releases_with_dates = []
        for release in self.releases:
            info = self.release_data.get(release, {})
            release_date = None
            if info:
                # loop through package types to find the first valid upload time
                for metadata in info.values():
                    upload_time = metadata.get("upload_time")
                    if upload_time:
                        try:
                            release_date = datetime.fromisoformat(
                                upload_time.replace("Z", "+00:00")
                            )
                            break
                        except ValueError:
                            continue
            if release_date:
                releases_with_dates.append((release, release_date))
        return releases_with_dates

    def get_sorted_releases(self) -> list[str]:
        """
        Returns a sorted list of releases based on their upload dates.
        Releases without dates are excluded from the list.
        The list is sorted in descending order (most recent first).

        :return: List of sorted release versions
        """
        if "sorted_releases" not in self._cache:
            # filter and sort by datetime
            sorted_releases = sorted(
                self.get_releases_with_dates(),
                key=itemgetter(1),
                reverse=True,
            )
            self._cache["sorted_releases"] = [ver for ver, _ in sorted_releases]
        sorted_versions: list[str] = self._cache["sorted_releases"]
        return sorted_versions

    def get_latest_releases(self, n: int = 20) -> list[str]:
        """
        Returns the latest `n` releases sorted by upload time (most recent first).
        """
        return self.get_sorted_releases()[:n]


class WoppClient:
    """
    Synchronous client for accessing the PyPI JSON API.
    """

    def __init__(
        self,
        pool_connections: bool = True,
        request_hooks: dict[str, Any] | None = None,
    ) -> None:
        self.base_url: str = PYPI_BASE_URL
        self.session: Session | None = Session() if pool_connections else None
        self.request_hooks: dict[str, list[Any]] = request_hooks or hooks.default_hooks()

    def request(
        self,
        package: str | None = None,
        version: str | None = None,
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

        cleaned = response.cleaned_json
        return WoppResponse(response.status_code, cleaned)

    def _build_url(
        self,
        package: str | None,
        version: str | None,
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
