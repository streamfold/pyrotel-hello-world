# pyrotel hello world

Install:

``` shell
uv sync
```

Run:

``` shell
# Find as test-rotel key in Bitwarden
export AXIOM_API_TOKEN=1234..
export AXIOM_DATASET=test-rotel
uv run hello.py
```

To use the OTEL gRPC SDK exporter to export to Rotel, set `USE_GRPC=1`:

``` shell
USE_GRPC=1 uv run hello.py
```
