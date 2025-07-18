#  Copyright (c) 2025. Centre National d'Etudes Spatiales (CNES).
#
#  This file is part of PANDORA2D
#
#      https://github.com/CNES/Pandora2D
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""
Test various P2D_INVALID_MASK_RIGHT generation.
"""

# pylint: disable=redefined-outer-name

import numpy as np
import pytest

from pandora2d import criteria
from pandora2d.constants import Criteria


@pytest.fixture()
def criteria_name():
    return Criteria.P2D_INVALID_MASK_RIGHT.name


@pytest.mark.parametrize(
    ["make_cost_volumes", "expected"],
    [
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 1},
                "col_disparity": {"init": 0, "range": 2},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.full((6, 8), 0),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.full((6, 8), 0),
            id="No right mask",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 1},
                "col_disparity": {"init": 0, "range": 2},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [1, 1, 1, 1, 1, 0, 0, 0],
                    [1, 1, 1, 1, 1, 0, 0, 0],
                    [1, 1, 1, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with one invalid point",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 1},
                "col_disparity": {"init": 0, "range": 2},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                ]
            ),
            id="Right mask with 1 point with all invalid disparities",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 1},
                "col_disparity": {"init": 0, "range": 2},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 3,
            },
            # When P2D_LEFT_BORDER is raised for a point, no other criteria is raised for this point.
            # In this case, P2D_LEFT_BORDER is raised so P2D_INVALID_MASK_RIGHT is not present on edges.
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 1, 1, 1, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with 1 point with all invalid disparities and window_size=3",
        ),
    ],
    indirect=["make_cost_volumes"],
)
def test_right_mask(make_cost_volumes, criteria_name, expected):
    """
    Test that the produced P2D_INVALID_MASK_RIGHT band is correct according to the right mask.
    """

    cost_volumes = make_cost_volumes

    result = criteria.get_validity_dataset(cost_volumes.criteria).sel(criteria=criteria_name)["validity"].data

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    ["make_cost_volumes", "expected"],
    [
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 2},
                "col_disparity": {"init": 0, "range": 3},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with row disp=[-2,2] and col disp=[-3,3]",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 0},
                "col_disparity": {"init": 0, "range": 1},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with no row disp and col disp=[-1,1]",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 2, "range": 1},
                "col_disparity": {"init": 0, "range": 0},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 1, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with row disp=[1,3] and no col disp",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 2, "range": 1},
                "col_disparity": {"init": -3, "range": 1},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with row disp=[1,3] and col disp=[-4,-2]",
        ),
    ],
    indirect=["make_cost_volumes"],
)
def test_disparities(make_cost_volumes, criteria_name, expected):
    """
    Test that the produced P2D_INVALID_MASK_RIGHT band is correct according to disparities.
    """

    cost_volumes = make_cost_volumes

    result = criteria.get_validity_dataset(cost_volumes.criteria).sel(criteria=criteria_name)["validity"].data

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    ["make_cost_volumes", "expected"],
    [
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 2},
                "col_disparity": {"init": 0, "range": 3},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
                "roi": {
                    "row": {"first": 2, "last": 7},
                    "col": {"first": 2, "last": 9},
                },
            },
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with ROI, row disp=[-2,2] and col disp=[-3,3]",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 0},
                "col_disparity": {"init": 0, "range": 1},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 1,
                "window_size": 1,
                "roi": {
                    "row": {"first": 4, "last": 9},
                    "col": {"first": 0, "last": 7},
                },
            },
            np.array(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with ROI, no row disp and col disp=[-1,1]",
        ),
    ],
    indirect=["make_cost_volumes"],
)
def test_roi(make_cost_volumes, criteria_name, expected):
    """
    Test that the produced P2D_INVALID_MASK_RIGHT band is correct according to ROI.
    """

    cost_volumes = make_cost_volumes

    result = criteria.get_validity_dataset(cost_volumes.criteria).sel(criteria=criteria_name)["validity"].data

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    ["make_cost_volumes", "expected"],
    [
        # This test should fail once we have corrected the way we apply masks to subpixel disparities
        pytest.param(
            {
                "row_disparity": {"init": 2, "range": 1},
                "col_disparity": {"init": 0, "range": 0},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 2,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 1, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with row disp=[1,3] and no col disp, subpix=2",
        ),
        # This test should fail once we have corrected the way we apply masks to subpixel disparities
        pytest.param(
            {
                "row_disparity": {"init": 2, "range": 1},
                "col_disparity": {"init": -3, "range": 1},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 1],
                "subpix": 4,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 0, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with row disp=[1,3] and col disp=[-4,-2], subpix=4",
        ),
    ],
    indirect=["make_cost_volumes"],
)
def test_subpix(make_cost_volumes, criteria_name, expected):
    """
    Test that the produced P2D_INVALID_MASK_RIGHT band is correct according to subpix.
    """

    cost_volumes = make_cost_volumes

    result = criteria.get_validity_dataset(cost_volumes.criteria).sel(criteria=criteria_name)["validity"].data

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    ["make_cost_volumes", "expected"],
    [
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 2},
                "col_disparity": {"init": 0, "range": 3},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [2, 1],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
            id="Right mask with step=[2,1], row disp=[-2,2] and col disp=[-3,3]",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 0, "range": 0},
                "col_disparity": {"init": 0, "range": 1},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [1, 3],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                ]
            ),
            id="Right mask with step=[1,3], no row disp and col disp=[-1,1]",
        ),
        pytest.param(
            {
                "row_disparity": {"init": 2, "range": 1},
                "col_disparity": {"init": -3, "range": 1},
                "msk_left": np.full((6, 8), 0),
                "msk_right": np.array(
                    [
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 0, 0, 0, 0],
                        [0, 0, 0, 0, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 2, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                    ]
                ),
                "step": [4, 2],
                "subpix": 1,
                "window_size": 1,
            },
            np.array(
                [
                    [0, 0, 0, 1],
                    [0, 0, 0, 0],
                ]
            ),
            id="Right mask with step=[4,2], row disp=[1,3] and col disp=[-4,-2]",
        ),
    ],
    indirect=["make_cost_volumes"],
)
def test_step(make_cost_volumes, criteria_name, expected):
    """
    Test that the produced P2D_INVALID_MASK_RIGHT band is correct according to step.
    """

    cost_volumes = make_cost_volumes

    result = criteria.get_validity_dataset(cost_volumes.criteria).sel(criteria=criteria_name)["validity"].data

    np.testing.assert_array_equal(result, expected)
