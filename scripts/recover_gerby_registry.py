"""Read live tags over Railway key SSH.

Railway CLI v5 connects with a key
registered via `railway ssh keys`. The
target is the User/HostName pair that
`railway ssh config --dry-run` prints.
"""

import argparse
import base64
import datetime
import hashlib
import json
import shlex
import subprocess
from pathlib import Path


REMOTE = """
import base64, hashlib, json, os, pathlib
p = pathlib.Path('/app/gerby/tags')
b = p.read_bytes()
print(base64.b64encode(json.dumps({
    'sha256': hashlib.sha256(b).hexdigest(),
    'data': base64.b64encode(b).decode(),
    'deployment': os.environ.get(
        'RAILWAY_DEPLOYMENT_ID'),
    'instance': os.environ.get(
        'RAILWAY_REPLICA_ID'),
    'commit': os.environ.get(
        'RAILWAY_GIT_COMMIT_SHA'),
}).encode()).decode())
"""


def recover(target, known_hosts, output):
    result = subprocess.run(
        [
            "ssh",
            # Pinned host key, no agent.
            "-o", "StrictHostKeyChecking=yes",
            "-o",
            "UserKnownHostsFile="
            + str(known_hosts),
            "-o", "ForwardAgent=no",
            "-o", "BatchMode=yes",
            target,
            "python -c "
            + shlex.quote(REMOTE),
        ],
        stdin=subprocess.DEVNULL,
        capture_output=True,
    )
    if result.returncode:
        raise SystemExit(
            result.stderr.decode(errors="replace")
            or "Railway SSH failed"
        )
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
        "deployment": payload["deployment"],
        "instance": payload["instance"],
        "commit": payload["commit"],
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
    print("Deployment:", payload["deployment"])
    print("SHA256:", digest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        required=True,
        help="User@ssh.railway.com",
    )
    parser.add_argument(
        "--known-hosts",
        required=True,
        help="Pinned ssh.railway.com key",
    )
    parser.add_argument(
        "--output", required=True
    )
    args = parser.parse_args()
    recover(
        args.target,
        args.known_hosts,
        args.output,
    )
