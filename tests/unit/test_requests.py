# Copyright 2021 Kersten Henrik Breuer (kersten-breuer@outlook.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests the `requests` module."""

import pytest
from openapi_core.validation.request.datatypes import OpenAPIRequest

from apiprimed.requests import starlette_to_openapi_request, validate_request
from apiprimed.api_spec import OpenApiSpec
from openapi_core.exceptions import OpenAPIError


from .fixtures.starlette import (
    VALID_STARLETTE_REQUEST,
    INVALID_STARLETTE_REQUEST,
    FakeStareletteRequest,
)
from .fixtures.specs import EXAMPLE_SPEC
from .fixtures.utils import null_context_manager


@pytest.mark.asyncio
async def test_starlette_to_openapi_request():
    """Test the `starlette_to_openapi_request` conversion function."""
    starlette_request = VALID_STARLETTE_REQUEST

    openapi_request = await starlette_to_openapi_request(starlette_request)

    assert isinstance(openapi_request, OpenAPIRequest)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "star_request,expect_error",
    [
        (VALID_STARLETTE_REQUEST, False),
        (INVALID_STARLETTE_REQUEST, True),
    ],
)
async def test_validate_request(
    star_request: FakeStareletteRequest, expect_error: bool
):
    """Test the "validate_request" function."""
    spec = OpenApiSpec(spec_path=EXAMPLE_SPEC["json_path"])

    cm = pytest.raises(OpenAPIError) if expect_error else null_context_manager()
    with cm:
        await validate_request(star_request, spec=spec)
