To build:
gcloud builds submit --tag gcr.io/pima-gcp/cc-sf-integration-app

To deploy:
gcloud run deploy pima-integration-app \
--image gcr.io/pima-gcp/pima-integration \
--platform managed \
--allow-unauthenticated \
--region europe-west1 \
--network=default \
--subnet=default \ 