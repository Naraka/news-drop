from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
import uuid

try:
    config.load_incluster_config()
    print("In-cluster config loaded.")
except ConfigException as e:
    print(f"Failed to load in-cluster config: {e}")
    try:
        config.load_kube_config()
        print("Local config loaded.")
    except ConfigException as e:
        print(f"Failed to load local config: {e}")
        raise RuntimeError("Failed to load any Kubernetes config")


api_instance = client.AppsV1Api()

def create_deployment(key_instance, language, country):
    sufx = str(uuid.uuid4())[:8]
    deployment_name = str("bot-scraper-" + sufx)

    container = client.V1Container(
        name="news-drop-container-1",
        image="gcr.io/news-drop/news-drop-container:0.2.0",
        env=[
            client.V1EnvVar(name="key_instance", value=key_instance),
            client.V1EnvVar(name="language", value=language),
            client.V1EnvVar(name="country", value=country),
            client.V1EnvVar(
                name="DB_USER",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name="db-credentials",
                        key="DB_USER"
                    )
                )
            ),
            client.V1EnvVar(
                name="DB_PASSWORD",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name="db-credentials",
                        key="DB_PASSWORD"
                    )
                )
            ),
            client.V1EnvVar(
                name="DB_NAME",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name="db-credentials",
                        key="DB_NAME"
                    )
                )
            ),
            client.V1EnvVar(
                name="DB_HOST",
                value_from=client.V1EnvVarSource(
                    secret_key_ref=client.V1SecretKeySelector(
                        name="db-credentials",
                        key="DB_HOST"
                    )
                )
            )
        ],
        resources=client.V1ResourceRequirements(
            limits={
                "cpu": "10m",
                "memory": "50Mi"
            },
            requests={
                "cpu": "4m",
                "memory": "20Mi"
            }
        )
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "news-drop"}),
        spec=client.V1PodSpec(containers=[container])
    )

    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={'matchLabels': {'app': 'news-drop'}}
    )

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=deployment_name),
        spec=spec
    )

    api_response = api_instance.create_namespaced_deployment(
        namespace="bots",
        body=deployment
    )

    return deployment_name