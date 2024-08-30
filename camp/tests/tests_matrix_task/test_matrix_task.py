

import pytest

from camp.matrix_task.main import Matrix

MatrixType = list[tuple[Matrix, Matrix]]


@pytest.mark.parametrize(
    ["matrix", "expected_size"],
    [
        [
            Matrix(
                [
                    [1, 2],
                    [1, 2],
                ],
            ),
            (2, 2),
        ],
        [
            Matrix(
                [
                    [1],
                ],
            ),
            (1, 1),
        ],

    ],
)
def test_matrix_size(
    matrix: Matrix,
    expected_size: tuple[int, int],
) -> None:
    """Testing matrix size."""
    assert matrix.size == expected_size


@pytest.mark.parametrize(
    ["matrix1", "matrix2", "result"],
    [
        [
            Matrix(
                [
                    [1, 2],
                    [1, 2],
                ],
            ),
            Matrix(
                [
                    [1, 2],
                    [1, 2],
                ],
            ),
            Matrix(
                [
                    [2, 4],
                    [2, 4],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                ],
            ),
            Matrix(
                [
                    [-1],
                ],
            ),
            Matrix(
                [
                    [-2],
                ],
            ),
        ],
    ],
)
def test_matrix_addition(
    matrix1: Matrix,
    matrix2: Matrix,
    result: Matrix,
) -> None:
    """Test matrix addition."""
    assert matrix1 + matrix2 == result


@pytest.mark.parametrize(
    ["matrix", "result"],
    [
        [
            Matrix(
                [
                    [1, 2],
                    [1, 2],
                ],
            ),
            Matrix(
                [
                    [2, 4],
                    [2, 4],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                    [-1],
                ],
            ),
            Matrix(
                [
                    [-2],
                    [-2],
                ],
            ),
        ],
    ],
)
def test_matrix_inplace_addition(
    matrix: Matrix,
    result: Matrix,
) -> None:
    """Test in-place matrix addition."""
    matrix += matrix
    assert matrix == result


@pytest.mark.parametrize(
    "invalid_matrix",
    [
        [
            None,
        ],
        [
            123,
        ],
        [
            "Not a matrix",
        ],
    ],
)
def test_matrix_invalid_addition(
    invalid_matrix: None | int | str,
) -> None:
    """Test matrix addition."""
    matrix1 = Matrix(
        [
            [1, 2],
            [1, 2],
        ],
    )
    with pytest.raises(
        ValueError,
        match=r"Unsupported operand for \+: 'Matrix' and '.*'",
    ):
        assert matrix1 + invalid_matrix


@pytest.mark.parametrize(
    ["matrix1", "matrix2", "result"],
    [
        [
            Matrix(
                [
                    [1, 1],
                    [1, 1],
                ],
            ),
            Matrix(
                [
                    [2, 2],
                    [2, 2],
                ],
            ),
            Matrix(
                [
                    [-1, -1],
                    [-1, -1],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [3],
                ],
            ),
            Matrix(
                [
                    [1],
                ],
            ),
            Matrix(
                [
                    [2],
                ],
            ),
        ],
    ],
)
def test_matrix_subtraction(
    matrix1: Matrix,
    matrix2: Matrix,
    result: Matrix,
) -> None:
    """Test matrix subtraction."""
    assert matrix1 - matrix2 == result


@pytest.mark.parametrize(
    ["matrix1", "matrix2", "result"],
    [
        [
            Matrix(
                [
                    [1, 2],
                    [1, 2],
                ],
            ),
            Matrix(
                [
                    [2, 4],
                    [2, 4],
                ],
            ),
            Matrix(
                [
                    [-1, -2],
                    [-1, -2],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                    [-1],
                ],
            ),
            Matrix(
                [
                    [-1],
                    [-1],
                ],
            ),
            Matrix(
                [
                    [0],
                    [0],
                ],
            ),
        ],
    ],
)
def test_matrix_inplace_subtraction(
    matrix1: Matrix,
    matrix2: Matrix,
    result: Matrix,
) -> None:
    """Test in-place matrix subtraction."""
    matrix1 -= matrix2
    assert matrix1 == result


@pytest.mark.parametrize(
    "invalid_matrix",
    [
        [
            None,
        ],
        [
            123,
        ],
        [
            "Not a matrix",
        ],
    ],
)
def test_matrix_invalid_subtraction(
    invalid_matrix: None | int | str,
) -> None:
    """Test matrix addition."""
    matrix1 = Matrix(
        [
            [1, 2],
            [1, 2],
        ],
    )
    with pytest.raises(
        ValueError,
        match=r"Unsupported operand for \-: 'Matrix' and '.*'",
    ):
        assert matrix1 - invalid_matrix


@pytest.mark.parametrize(
    ["matrix1", "matrix2", "result"],
    [
        [
            Matrix(
                [
                    [1, 1, 1],
                    [2, 2, 2],
                    [3, 3, 3],
                ],
            ),
            Matrix(
                [
                    [4, 4, 4],
                    [5, 5, 5],
                    [6, 6, 6],
                ],
            ),
            Matrix(
                [
                    [15, 15, 15],
                    [30, 30, 30],
                    [45, 45, 45],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                ],
            ),
            Matrix(
                [
                    [2],
                ],
            ),
            Matrix(
                [
                    [-2],
                ],
            ),
        ],
    ],
)
def test_matrix_multiplication(
    matrix1: Matrix,
    matrix2: Matrix,
    result: Matrix,
) -> None:
    """Test matrix multiplication."""
    result_matrix = matrix1 * matrix2
    assert result_matrix == result


@pytest.mark.parametrize(
    ["matrix", "number", "result"],
    [
        [
            Matrix(
                [
                    [1, 2, 3],
                    [3, 4, 5],
                    [5, 6, 7],
                ],
            ),
            2,
            Matrix(
                [
                    [2, 4, 6],
                    [6, 8, 10],
                    [10, 12, 14],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                ],
            ),
            -1,
            Matrix(
                [
                    [1],
                ],
            ),
        ],
    ],
)
def test_matrix_scalar_multiplication(
    matrix: Matrix,
    number: int,
    result: Matrix,
) -> None:
    """Test matrix multiplication by scalar."""
    result_matrix = matrix * number
    assert result_matrix == result


@pytest.mark.parametrize(
    ["matrix", "number", "result"],
    [
        [
            Matrix(
                [
                    [1, 2, 3],
                    [3, 4, 5],
                    [5, 6, 7],
                ],
            ),
            2,
            Matrix(
                [
                    [2, 4, 6],
                    [6, 8, 10],
                    [10, 12, 14],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                ],
            ),
            -1,
            Matrix(
                [
                    [1],
                ],
            ),
        ],
    ],
)
def test_matrix_inplace_scalar_multiplication(
    matrix: Matrix,
    number: int,
    result: Matrix,
) -> None:
    """Test in-place matrix multiplication by scalar."""
    matrix *= number
    assert matrix == result


@pytest.mark.parametrize(
    "invalid_matrix",
    [
        [
            None,
        ],
        [
            123,
        ],
        [
            "Not a matrix",
        ],
    ],
)
def test_matrix_invalid_multiplication(
    invalid_matrix: None | int | str,
) -> None:
    """Test matrix addition."""
    matrix1 = Matrix(
        [
            [1, 2],
            [1, 2],
        ],
    )
    with pytest.raises(
        ValueError,
        match=r"Unsupported operand for \*: 'Matrix' and '.*'",
    ):
        assert matrix1 * invalid_matrix


@pytest.mark.parametrize(
    ["matrix", "result"],
    [
        [
            Matrix(
                [
                    [1, 2, 3],
                    [3, 4, 5],
                    [5, 6, 7],
                ],
            ),
            Matrix(
                [
                    [1, 3, 5],
                    [2, 4, 6],
                    [3, 5, 7],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1, 2],
                    [3, -4],
                ],
            ),
            Matrix(
                [
                    [-1, 3],
                    [2, -4],
                ],
            ),
        ],
    ],
)
def test_matrix_transpose(
    matrix: Matrix,
    result: Matrix,
) -> None:
    """Test matrix transpose."""
    result_matrix = matrix.transpose()
    assert result_matrix == result


@pytest.mark.parametrize(
    ["matrix", "power", "result"],
    [
        [
            Matrix(
                [
                    [1, 2, 3],
                    [3, 4, 5],
                    [5, 6, 7],
                ],
            ),
            2,
            Matrix(
                [
                    [22, 28, 34],
                    [40, 52, 64],
                    [58, 76, 94],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [1, 2, 3],
                    [3, 4, 5],
                    [5, 6, 7],
                ],
            ),
            0,
            Matrix(
                [
                    [1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                ],
            ),
            3,
            Matrix(
                [
                    [468, 576, 684],
                    [1062, 1305, 1548],
                    [1656, 2034, 2412],
                ],
            ),
        ],
    ],
)
def test_matrix_pow(
    matrix: Matrix,
    power: int,
    result: Matrix,
) -> None:
    """Test matrix power by scalar."""
    result_matrix = matrix ** power
    assert result_matrix == result


def test_matrix_invalid_pow() -> None:
    """Test matrix addition."""
    matrix1 = Matrix(
        [
            [1, 2],
            [1, 2],
        ],
    )
    with pytest.raises(
        ValueError,
        match="Power must be a non-negative integer",
    ):
        assert matrix1 ** -2


@pytest.mark.parametrize(
    ["matrix", "result"],
    [
        [
            Matrix(
                [
                    [1, 2],
                    [1, 2],
                ],
            ),
            Matrix(
                [
                    [-1, -2],
                    [-1, -2],
                ],
            ),
        ],
        [
            Matrix(
                [
                    [-1],
                    [-1],
                ],
            ),
            Matrix(
                [
                    [1],
                    [1],
                ],
            ),
        ],
    ],
)
def test_matrix_negation(
    matrix: Matrix,
    result: Matrix,
) -> None:
    """Test matrix negation."""
    result_matrix = -matrix
    assert result_matrix == result
