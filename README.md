To build:
gcloud builds submit --tag gcr.io/pima-gcp/cc-sf-integration-app

To deploy:
gcloud run deploy cc-sf-integration-app --image gcr.io/pima-gcp/cc-sf-integration-app --platform managed --allow-unauthenticated --region europe-west1