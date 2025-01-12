from typing import List

import pytest

from tests.plugins import PluginCanHandleUrl, generic_negative_matches


def pytest_collection_modifyitems(items):  # pragma: no cover
    # type: (List[pytest.Item])
    # remove empty parametrized tests
    items[:] = [
        item
        for item in items
        if not any(
            marker.name == "skip" and str(marker.kwargs.get("reason", "")).startswith("got empty parameter set")
            for marker in item.own_markers
        )
    ]


def pytest_generate_tests(metafunc):  # pragma: no cover
    # type: (pytest.Metafunc)
    if metafunc.cls is not None and issubclass(metafunc.cls, PluginCanHandleUrl):
        if metafunc.function.__name__ == "test_can_handle_url_positive":
            metafunc.parametrize("url", metafunc.cls.should_match + [url for url, groups in metafunc.cls.should_match_groups])

        elif metafunc.function.__name__ == "test_can_handle_url_negative":
            metafunc.parametrize("url", metafunc.cls.should_not_match + generic_negative_matches)

        elif metafunc.function.__name__ == "test_capture_groups":
            metafunc.parametrize("url,groups", metafunc.cls.should_match_groups, ids=[
                "URL={0} GROUPS={1}".format(url, groups)
                for url, groups in metafunc.cls.should_match_groups
            ])
