import os
import time
from rotel import Rotel
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as OTLPHTTPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter as OTLPGRPCSpanExporter

from rotel import OTLPExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

#
# Configure OpenTelemetry SDK to export to the localhost Rotel
#

# Define the service name resource for the tracer.
resource = Resource(
    attributes={
        SERVICE_NAME: "pyrotel-test"  # Replace `NAME_OF_SERVICE` with the name of the service you want to trace.
    }
)

# Create a TracerProvider with the defined resource for creating tracers.
provider = TracerProvider(resource=resource)

# Create the OTel exporter to send to the localhost Rotel agent
exporter = OTLPHTTPSpanExporter(endpoint = "http://localhost:4318/v1/traces")

if os.environ.get("USE_GRPC") is not None:
    exporter = OTLPGRPCSpanExporter(endpoint = "http://localhost:4317")

# Create a processor with the OTLP exporter to batch and send trace spans.
# You could also use the BatchSpanProcessor, but since Rotel runs locally
# and will batch, you can emit spans immediately.
processor = SimpleSpanProcessor(exporter)
provider.add_span_processor(processor)

# Set the TracerProvider as the global tracer provider.
trace.set_tracer_provider(provider)

# Define a tracer for external use in different parts of the app.
service1_tracer = trace.get_tracer("service1")

#
# Configure Rotel to export to Axiom
#

otlp_exporter = OTLPExporter(
    endpoint="https://api.axiom.co",
    protocol="http", # Axiom only supports HTTP
    headers={
        "Authorization": f"Bearer {os.environ['AXIOM_API_TOKEN']}",
        "X-Axiom-Dataset": os.environ["AXIOM_DATASET"],
    },
)

rotel = Rotel(
    enabled=True,
    exporter=otlp_exporter,
)

def main():
    rotel.start()

    print("Hello from example!")
    with service1_tracer.start_as_current_span("example_span") as span:
        span.set_attribute("example_attribute", "example_value")
        print("Hello from example span!")
        time.sleep(1)
        print("Goodbye from example span!")

    rotel.stop()


if __name__ == "__main__":
    main()
