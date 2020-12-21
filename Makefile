.PHONY: run
run: build
	docker run --rm -it glacion/kubectl:$(VERSION)

.ONESHELL: build
.PHONY: build
build:
	docker build \
	--build-arg version=$(VERSION) \
	--build-arg revision=$(REVISION) \
	--build-arg date=$(shell date --iso-8601=second) \
	-t glacion/kubectl:$(VERSION) .

.PHONY: push
push: build
	docker image push glacion/kubectl:$(VERSION)