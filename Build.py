import os
import sys
import subprocess
from datetime import datetime
from scripts.build.files import get_instruction_files, get_rootfs_files
from scripts.build.instructions import load_instructions
from scripts.build.context import create_context
import glob
from ruamel.yaml import YAML

DOCKERFILE = "./Dockerfile"

REF = os.getenv("IMAGE_TAG")
EVENT = os.getenv("GITHUB_EVENT_NAME")
WORKSPACE = os.getenv("GITHUB_WORKSPACE")
SHA = os.getenv("GITHUB_SHA")
CHANGED_FILES = os.getenv("CHANGED_FILES", "instructions/Development/v.yaml").split(" ")

ALLINSTRUCTIONS = {}
CONTAINERINSTRUCTIONS = {}
ROOTFS = get_rootfs_files()


def create_dockerfile(tag, instructions):
    content = []
    run = []
    content.append(f"FROM {instructions['base']}")
    content.append(f"ENV CONTAINER_TYPE='{tag}'")
    if instructions.get("S6"):
        content.append("ENV S6_BEHAVIOUR_IF_STAGE2_FAILS=2")
        content.append("ENV S6_CMD_WAIT_FOR_SERVICES=1")

    if len(instructions.get("env", [])) != 0:
        for env in instructions["env"]:
            content.append(f"ENV {env}={instructions['env'][env]}")

    if tag in ROOTFS:
        content.append(f"COPY rootfs/{tag} /")

    if len(instructions.get("needs", [])) == 0:
        content.append("COPY rootfs/common /")
        run.append("chmod +x /usr/bin/container")

        if instructions.get("alpine-packages") is not None:
            run.append(
                "echo '@edge http://dl-cdn.alpinelinux.org/alpine/edge/main' >> /etc/apk/repositories"
            )

    if instructions.get("alpine-packages") is not None:
        run.append(
            f"apk add --no-cache {' '.join(instructions['alpine-packages'])} && rm -rf /var/cache/apk/*"
        )

    if instructions.get("debian-packages") is not None:
        run.append(
            f"apt update && apt install -y --no-install-recommends --allow-downgrades {' '.join(instructions['debian-packages'])}"
            + " && rm -fr /tmp/* /var/{cache,log}/* /var/lib/apt/lists/*"
        )

    if instructions.get("python-packages") is not None:
        run.append(
            f"python3 -m pip install --no-cache-dir -U pip && python3 -m pip install --no-cache-dir -U {' '.join(instructions['python-packages'])} && "
            + " find /usr/local \( -type d -a -name test -o -name tests -o -name '__pycache__' \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \;"
        )

    if len(instructions.get("run", [])) != 0:
        run.append(" && ".join(instructions["run"]))

    if instructions.get("S6"):
        content.append("COPY rootfs/s6/install /s6/install")
        run.append("bash /s6/install && rm -R /s6")

    content.append(f"RUN {' && '.join(run)}")

    if instructions.get("entrypoint") is not None:
        content.append(f"ENTRYPOINT {instructions['entrypoint']}")

    date = datetime.now()
    content.append("LABEL maintainer='hi@ludeeus.dev'")
    content.append(f"LABEL build.date='{date.year}-{date.month}-{date.day}'")
    content.append(f"LABEL build.sha='{SHA}'")

    with open(DOCKERFILE, "w") as df:
        df.write("\n".join(content))
        df.write("\n")


def needs_build(tag, instructions):
    for changed_file in [x for x in CHANGED_FILES if not x.startswith("docs")]:
        if tag in changed_file:
            return True
        for needs in instructions.get("needs", []):
            if needs in changed_file:
                return True
        if "rootfs/common" in changed_file:
            return True
        if "rootfs/s6" in changed_file and instructions.get("S6"):
            return True
    return False


def build_tag(CONTAINER):
    create_context(CONTAINER, load_instructions(CONTAINER))
    buildx = "docker buildx build"
    if PUBLISH:
        args = " --output=type=image,push=true"
    elif "build" in sys.argv:
        args = " --load"
    else:
        args = " --output=type=image,push=false"
    if "-base" in CONTAINER and "build" not in sys.argv:
        args += " --platform linux/arm,linux/arm64,linux/amd64"
    else:
        args += " --platform linux/amd64"
    args += " --no-cache"
    args += " --compress"
    args += f" -t ludeeus/container:{CONTAINER}"
    if CONTAINER == "alpine-base":
        args += f" -t ludeeus/container:latest"
    args += f" -f {DOCKERFILE}"
    args += " ."
    run_command(buildx + args)


def run_command(command):
    print(command)
    cmd = subprocess.run([x for x in command.split(" ")])
    if cmd.returncode != 0:
        exit(1)


def main(runtype):
    needs = None
    if len(runtype) == 1:
        print("Runtype is missing")
        exit(1)
    publish = "publish" in runtype

    if "needs" in runtype:
        if "0" in runtype:
            needs = 0
        if "1" in runtype:
            needs = 1
        if "2" in runtype:
            needs = 2
        if "3" in runtype:
            needs = 3
        if "4" in runtype:
            needs = 4

    build_tag(CONTAINER)
    return
    for tag in sorted(
        INSTRUCTIONS, key=lambda x: len(INSTRUCTIONS[x].get("needs", []))
    ):
        if needs is not None:
            if len(INSTRUCTIONS[tag].get("needs", [])) == needs:
                build_tag(tag, INSTRUCTIONS[tag], publish)
        else:
            build_tag(tag, INSTRUCTIONS[tag], publish)


if len(sys.argv) < 2:
    print(
        """
  usage builder.py [tag] options

  options:
    --publish       Publishes the tag to docker hub
"""
    )
    exit()
else:
    CONTAINER = sys.argv[1]
    PUBLISH = "--publish" in sys.argv
    main(sys.argv)
