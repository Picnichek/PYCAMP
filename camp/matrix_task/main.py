from __future__ import annotations

from typing import TypeAlias

Matrix_data: TypeAlias = list[list[int | float]]


class Matrix:
    """Represent a mathematical matrix."""

    def __init__(
        self,
        data: Matrix_data,
    ) -> None:
        """Initialize a Matrix object with given data.

        Args:
            data (Matrix_data): The list of lists representing the matrix data.
            rows (int): The number of rows in the matrix.
            cols (int): The number of columns in the matrix.
        """
        self.data = data
        self.rows_count = len(data)
        self.cols_count = len(data[0])

    @property
    def size(self) -> tuple[int, int]:
        """Return size of the matrix.

        Returns:
            tuple: Tuple representing the number of rows and columns.
        """
        return self.rows_count, self.cols_count

    def __add__(self, other: object) -> Matrix:
        """Sum two matrices.

        Args:
            other (object): The matrix to be add.

        Raises:
            ValueError: If the other is no a matrix.

        Returns:
            Matrix: The sum of two matrix.
        """
        if not isinstance(other, Matrix):
            raise ValueError(
                f"Unsupported operand for +: 'Matrix' and '{type(other)}'",
            )
        return Matrix(
            [
                [
                    self.data[i][j] + other.data[i][j]
                    for j in range(self.cols_count)
                ]
                for i in range(self.rows_count)
            ],
        )

    def __iadd__(self, other: object) -> Matrix:
        """Implement the += operator for matrices.

        Returns:
            Self: The updated matrix.
        """
        new_matrix = self.__add__(other)
        self.data = new_matrix.data
        return self

    def __sub__(self, other: object) -> Matrix:
        """Subtract one matrix from another.

        Args:
            other (object): The matrix to subtract.

        Raises:
            ValueError: If the other is no a matrix.

        Returns:
            Matrix: The result of the subtraction.
        """
        if not isinstance(other, Matrix):
            raise ValueError(
                f"Unsupported operand for -: 'Matrix' and '{type(other)}'",
            )
        return Matrix(
            [
                [
                    self.data[i][j] - other.data[i][j]
                    for j in range(self.cols_count)
                ]
                for i in range(self.rows_count)
            ],
        )

    def __isub__(self, other: object) -> Matrix:
        """Implement the -= operator for matrices.

        Returns:
            Self: The updated matrix.
        """
        new_matrix = self.__sub__(other)
        self.data = new_matrix.data
        return self

    def __mul__(self, other: object) -> Matrix:
        """Multiple the matrix by a scalar or another matrix.

        Args:
            other (object): The scalar or matrix to multiply by

        Raises:
            ValueError: If the other is not a scalar or matrix.

        Returns:
            Matrix: The result of multiplication
        """
        if isinstance(other, (int, float)):
            return Matrix(
                [
                    [self.data[i][j] * other for j in range(self.cols_count)]
                    for i in range(self.rows_count)
                ],
            )
        if isinstance(other, Matrix):
            return self.__matmul__(other)
        raise ValueError(
            f"Unsupported operand for *: 'Matrix' and '{type(other)}'",
        )

    def __rmul__(self, other: object) -> Matrix:
        """Implement the right multiplication."""
        return self.__mul__(other)

    def __imul__(self, other: object) -> Matrix:
        """Implement the *= operator for matrices."""
        new_matrix = self.__mul__(other)
        self.data = new_matrix.data
        return self

    def __matmul__(self, other: object) -> Matrix:
        """Multiply two matrices.

        Args:
            other (object): The matrix to multiply by.

        Raises:
            ValueError: If the other is not a matrix.
            ValueError: If the cols are not equal rows

        Returns:
            Matrix: The result of the multiplication.
        """
        if not isinstance(other, Matrix):
            raise ValueError(
                f"Unsupported operand for *: 'Matrix' and '{type(other)}'",
            )
        if self.cols_count != other.rows_count:
            raise ValueError("Matrices are not aligned for multiplication")
        result = [
            [
                sum(
                    self.data[i][k] * other.data[k][j]
                    for k in range(self.cols_count)
                )
                for j in range(other.cols_count)
            ]
            for i in range(self.rows_count)
        ]
        return Matrix(result)

    def __rmatmul__(self, other: Matrix) -> Matrix:
        """Implement the right matrix multiplication."""
        return other.__matmul__(self)

    def __imatmul__(self, other: object) -> Matrix:
        """Implement the @= operator for matrices."""
        result = self.__matmul__(other)
        self.data = result.data
        self.cols_count = len(result.data[0])
        return self

    def transpose(self) -> Matrix:
        """Transpose the matrix.

        Returns:
            Matrix: The transposes matrix.
        """
        return Matrix(
            [
                [
                    self.data[j][i] for j in range(self.rows_count)
                ]
                for i in range(self.cols_count)
            ],
        )

    def __pow__(self, power: int) -> Matrix:
        """Raise the matrix to the power.

        Args:
            power (int): The power to raise the matrix to.

        Raises:
            ValueError: If the power is negative.

        Returns:
            Matrix: The result of rising the matrix.
        """
        if power < 0:
            raise ValueError(
                "Power must be a non-negative integer",
            )
        if power == 0:
            return Matrix(
                [
                    [
                        1 if i == j else 0 for j in range(self.rows_count)
                    ]
                    for i in range(self.rows_count)
                ],
            )
        result = Matrix(self.data)
        for _ in range(power - 1):
            result *= self
        return result

    def __neg__(self) -> Matrix:
        """Negative the matrix."""
        return Matrix(
            [
                [
                    -self.data[i][j] for j in range(self.cols_count)
                ] for i in range(self.rows_count)
            ],
        )

    def __eq__(self, other: object) -> bool:
        """Check if two matrices are equal.

        Args:
            other (object): The matrix to compare with.

        Returns:
            bool: Return True if the matrices are equal.
        """
        if isinstance(other, Matrix):
            return self.data == other.data
        return False
