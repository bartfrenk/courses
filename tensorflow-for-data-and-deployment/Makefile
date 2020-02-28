
NAMESPACE := learning
NAME := tensorflow-for-data-and-deployment

PWD := $(shell pwd)

help: ## Show this help
	@echo "${NAMESPACE}-${NAME}"
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | \
	fgrep -v fgrep | sed -e 's/## */##/' | column -t -s##

init:
# install tensorflow serving: https://www.tensorflow.org/tfx/serving/setup

run/docker/test:
	@TESTDATA="${PWD}/external/serving/tensorflow_serving/servables/tensorflow/testdata"; \
	docker run -t --detach --rm -p 8501:8501 \
	    -v "$$TESTDATA/saved_model_half_plus_two_cpu:/models/half_plus_two" \
	    -e MODEL_NAME=half_plus_two \
	    tensorflow/serving

run/curl/test:
	@curl -d '{"instances": [1.0, 2.0, 5.0]}' -s \
        -X POST http://localhost:8501/v1/models/half_plus_two:predict | jq '.'

