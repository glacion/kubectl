import logging
import os
from sys import exit
from time import sleep
from typing import Iterator, Set

from dotenv import load_dotenv
from github import Github
from github.GithubException import UnknownObjectException
from github.Repository import Repository
from github.Workflow import Workflow
from semver import VersionInfo, parse_version_info


def get_from_github(repo_name: str, github_client: Github) -> Set[VersionInfo]:
    logging.info("getting kubectl releases from github")
    repo = github_client.get_repo(repo_name)
    tags = [
        tag.name.strip("kubernetes-")
        for tag in repo.get_tags()
        if tag.name.startswith("kubernetes-")
    ]
    return {parse_version_info(tag) for tag in tags}


def get_from_dockerhub(repo_name: str) -> Set[VersionInfo]:
    import requests

    logging.info("getting image releases from dockerhub")

    session = requests.Session()
    retval = set()
    response = session.get(
        f"https://hub.docker.com/v2/repositories/{repo_name}/tags/"
    ).json()

    while True:
        for image in response["results"]:
            retval.add(parse_version_info(image["name"]))
        if response["next"] == None:
            break

        logging.info(f"found new page at {response['next']}")
        response = session.get(response["next"]).json()

    return retval


def discard(versions: Set[VersionInfo]) -> Set[VersionInfo]:
    return {
        version
        for version in versions
        if version.prerelease == None and version.build == None
    }


def get_versions(github_client: Github):
    releases = get_from_github("kubernetes/kubectl", github_client)
    releases = discard(releases)
    images = get_from_dockerhub("glacion/kubectl")
    return releases - images


def sort_versions(versions: Set[VersionInfo]):
    return [version for version in sorted(versions)]


def dispatch(versions, workflow):
    for version in versions:
        logging.info(f"dispatching build request for version {version}")
        response = workflow.create_dispatch("main", {"version": str(version)})
        if not response:
            logging.error("failed to dispatch")
            break
        logging.info("sleeping for 5 seconds")
        sleep(5)


logging.basicConfig(level=logging.INFO)
load_dotenv()

access_token = os.getenv("TOKEN")
github_client = Github(access_token)
workflow = github_client.get_repo("glacion/kubectl").get_workflow("build.yaml")

versions = get_versions(github_client)
versions = sort_versions(versions)
if len(versions) == 0:
    logging.info(f"found no new releases")
else:
    logging.info(f"found {len(versions)} new releases")
    dispatch(versions, workflow)
