# -*- coding: utf-8 -*-

"""Utility methods"""
from __future__ import unicode_literals  # unicode support for py2


def clean_response(r, *args, **kwargs):
    """
    Hook called after a response is received.
    Used to modify response.

    :param r: requests.models.Response object
    :param args:
    :param kwargs:
    :return: modified Response object
    """

    def convert_pkg_info(pkg_url_list):
        """
        Converts a list of package info dicts
        into a dict, where the key is the type
        of package.. eg: sdist
        :param pkg_url_list:
        :return: dict
        """
        package_urls = {}
        if pkg_url_list:
            for pkg_url in pkg_url_list:
                package_urls.update({
                    pkg_url.get('packagetype'): {
                        'md5': pkg_url.get('digests').get('md5'),
                        'sha256': pkg_url.get('digests').get('sha256'),
                        'filename': pkg_url.get('filename'),
                        'has_sig': pkg_url.get('has_sig'),
                        'size': pkg_url.get('size'),
                        'upload_time': pkg_url.get('upload_time'),
                        'url': pkg_url.get('url'),
                    }})
        return package_urls

    # only run hooks for 200
    if r.status_code == 200:
        r.hook_called = True  # flag to confirm hook was called.

        dirty_response = r.json()
        cleaned_response = {}

        info = dirty_response.get('info')
        if info:
            cleaned_response = {
                'name': info.get('name'),
                'current_version': info.get('version'),
                'summary': info.get('summary'),
                'description': info.get('description'),
                'homepage': info.get('home_page'),
                'package_url': info.get('project_url') or info.get('package_url'),
                'project_urls': info.get('project_urls'),
                'requires_python': info.get('requires_python'),
                'license': info.get('license'),
                'author': info.get('author'),
                'author_email': info.get('author_email'),
                'current_release_url': info.get('release_url'),
                'dependencies': info.get('requires_dist'),
            }

        # todo: do everything below only if needed,
        # based on click options... eg: --detailed
        current_pkg_urls = dirty_response.get('urls')
        cleaned_response.update({
            'current_pkg_urls': convert_pkg_info(current_pkg_urls),
        })

        releases = dirty_response.get('releases')
        if releases:
            releases_info = {}
            for key, val in releases.items():
                releases_info[key] = convert_pkg_info(val)

            cleaned_response.update({
                'releases': releases_info,
            })

        # if we never added the release list info before,
        # add the minimal release info anyway
        if 'releases' not in cleaned_response:
            cleaned_response.update({
                'releases': list(releases.keys()) if releases else [],
            })

        r.cleaned_json = cleaned_response
    return r
