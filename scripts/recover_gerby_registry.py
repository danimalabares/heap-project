"""Read live tags via CLI v4.6.0."""

import argparse
import base64
import datetime
import hashlib
import json
import os
import shlex
import subprocess
from pathlib import Path


REMOTE = """
import base64, hashlib, json, pathlib
p = pathlib.Path('/app/gerby/tags')
b = p.read_bytes()
print(base64.b64encode(json.dumps({
    'sha256': hashlib.sha256(b).hexdigest(),
    'data': base64.b64encode(b).decode(),
}).encode()).decode())
"""


def recover(cli, instance, output):
    config = (
        Path.home() / ".railway/config.json"
    )
    user = json.loads(config.read_text())[
        "user"
    ]
    env = dict(os.environ)
    env["RAILWAY_NO_AUTO_UPDATE"] = "1"
    env["RAILWAY_API_TOKEN"] = (
        user.get("accessToken")
        or user["token"]
    )
    result = subprocess.run(
        [
            str(cli),
            "ssh",
            "-d",
            instance,
            "--",
            "python -c "
            + shlex.quote(REMOTE),
        ],
        env=env,
        capture_output=True,
        check=True,
    )
    # v4 SSH adds CRLF to stdout.
    payload = json.loads(
        base64.b64decode(
            b"".join(result.stdout.split()),
            validate=True,
        )
    )
    data = base64.b64decode(
        payload["data"], validate=True
    )
    digest = hashlib.sha256(data).hexdigest()
    if digest != payload["sha256"]:
        raise ValueError(
            "Backup checksum mismatch"
        )
    output = Path(output)
    # Never replace any previous backup.
    with output.open("xb") as stream:
        stream.write(data)
    metadata = {
        "instance": instance,
        "remote_path": "/app/gerby/tags",
        "sha256": digest,
        "bytes": len(data),
        "recovered_at_utc": (
            datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat()
        ),
    }
    sidecar = output.with_suffix(
        output.suffix + ".json"
    )
    with sidecar.open("x") as stream:
        json.dump(metadata, stream, indent=2)
        stream.write("\n")
    print("Recovered", len(data), "bytes")
    print("SHA256:", digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cli", required=True
    )
    parser.add_argument(
        "--instance", required=True
    )
    parser.add_argument(
        "--output", required=True
    )
    args = parser.parse_args()
    recover(
        args.cli, args.instance, args.output
    )
