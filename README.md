![build](https://github.com/glacion/kubectl/workflows/build/badge.svg)
[![Docker](https://img.shields.io/docker/v/glacion/kubectl)](https://hub.docker.com/r/glacion/kubectl)

# Kubectl

Kubectl and few other binaries packaged in a container

## Installation

```bash
docker pull glacion/kubectl
```

## Usage

```bash
docker run --rm -it -v "${PWD}/.kube/config:/root/.kube/config" glacion/kubectl
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
