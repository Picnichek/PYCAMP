import argparse
import uuid
from pathlib import Path

import requests


def download_image(
    text: str,
    output_file: str | None = None,
    **filter_kwargs: str,
) -> None:
    """Download an image from cataas.com.

    Text will be rendered on the generated image.

    If there is no "output_file" provided, it will be generated automatically
    Kwargs will be passed as query params to API.Avaliable params and their
    values:
        width: Any integer
        height: Any integer
        filter: "blur", "mono", "negate", "custom"
        type: "xsmall", "small", "medium", "square"

    Example:
        python3 main.py --width=100 --height=100 --filter=mono
        -t=medium -o=greeting.png "Have a nice day"

    Raises:
        request.exceptions.HTTPError: If request returned an unsuccessful
        status code.

    """
    base_url = f"https://cataas.com/cat/says/{text}"
    response = requests.get(
        base_url,
        stream=True,
        params=filter_kwargs,
        timeout=5,
    )

    response.raise_for_status()
    output_file = output_file or f"{uuid.uuid4().hex}.jpg"
    images_dir = Path(__file__).parent / "cat_images"
    images_dir.mkdir(exist_ok=True)
    Path(images_dir / output_file).open("wb").write(response.content)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="Cats downloader",
        description="Utility to download cats images.",
    )
    parser.add_argument("text", type=str)
    parser.add_argument(
        "-o",
        "--output_file",
        help="UUID-based filename will be used as default",
    )
    parser.add_argument(
        "-t",
        "--type",
        action="store",
        type=str,
        choices=("xsmall", "small", "medium", "square"),
    )
    parser.add_argument(
        "-f",
        "--filter",
        action="store",
        type=str,
        choices=("blur", "mono", "negate", "custom"),
    )
    parser.add_argument("--width", action="store", type=str, default="50")
    parser.add_argument("--height", action="store", type=str, default="50")

    args = parser.parse_args()
    download_image(**vars(args))
