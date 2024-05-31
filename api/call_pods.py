from kubernetes import client, config
import uuid

config.load_incluster_config()
api_instance = client.CoreV1Api()

def crear_pod(key_instance):
    sufx = str(uuid.uuid4())[:8]
    pod_name = str("bot-scraper-" + sufx)

    pod = client.V1Pod(
        metadata=client.V1ObjectMeta(name=pod_name),
        spec=client.V1PodSpec(
            containers=[
                client.V1Container(
                    name="news-drop-container-1",
                    image="gcr.io/news-drop/news-drop-container:0.1.9",
                    env=[
                        client.V1EnvVar(name="key_instance", value=key_instance),
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
            ]
        )
    )

    instance = api_instance.create_namespaced_pod(namespace="api-namescape-news-drop", body=pod)
    return pod_name


