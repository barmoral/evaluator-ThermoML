import os

from openff.evaluator.backends import ComputeResources
from openff.evaluator.backends.dask import DaskLocalCluster
from openff.evaluator.server import EvaluatorServer
from openff.evaluator.client import EvaluatorClient
from openff.evaluator.client import ConnectionOptions

# define client to submit queries
port = 8118
evaluator_client = EvaluatorClient(ConnectionOptions(server_port=port))

# define available / preferred resources
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
resources = ComputeResources(
    number_of_threads=1,
    number_of_gpus=1,
    preferred_gpu_toolkit=ComputeResources.GPUToolkit.CUDA,
)

with DaskLocalCluster(number_of_workers=1, resources_per_worker=resources) as calculation_backend:
    # spin up server
    evaluator_server = EvaluatorServer(calculation_backend=calculation_backend, delete_working_files=False, port=port)
    evaluator_server.start(asynchronous=True)

    # estimate data set by submitting calculation schemas to newly-created server
    request, exception = evaluator_client.request_estimate(
        property_set=data_set,
        force_field_source=force_field_source,
        options=estimation_options,
    )

    # Wait for the results.
    results, exception = request.results(synchronous=True, polling_interval=30)
    assert exception is None