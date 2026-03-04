import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.rest_api.typing import RESTAPIConfig
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


NYC_TAXI_API_CONFIG: RESTAPIConfig = {
    "client": {
        # Base URL for the NYC taxi REST API
        "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        # The API returns paginated JSON (1,000 records per page).
        # We use a page-number based paginator and stop when an empty page is returned.
        "paginator": PageNumberPaginator(
            base_page=1,
            page_param="page",
            # This API returns a JSON array (no "total" field), so we
            # disable total pages detection and stop on empty page.
            total_path=None,
            stop_after_empty_page=True
        ),
        },
    "resource_defaults": {
        # This API has no stable unique identifier in the payload, so `replace`
        # keeps the pipeline idempotent across repeated runs.
        "write_disposition": "replace",
        },        
    
    "resources": [
        {
            # Table/resource name in the destination
            "name": "nyc_taxi_trips",
            "columns": {
                # These fields are present in the API but may be null-only in the sample,
                # so we declare them explicitly to ensure they are materialized.
                "rate_code": {"data_type": "text"},
                "mta_tax": {"data_type": "double"},
            },            
            "endpoint": {
                # The Cloud Function uses the base URL directly; no extra path segment.
                "path": "",
                # If the API supports additional filters (e.g. year/month),
                # they can be added here as query params.
                # "params": {"year": 2019, "month": 1},
            },
        },
    ],
}


def nyc_taxi_rest_api_source():
    """Create a dlt REST API source for NYC taxi data."""
    return rest_api_source(NYC_TAXI_API_CONFIG)


taxi_pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    # Feel free to change the dataset name if desired.
    dataset_name="nyc_taxi_data",
    # Show basic progress information on stdout
    progress="log",
)


if __name__ == "__main__":
    load_info = taxi_pipeline.run(nyc_taxi_rest_api_source())
    print(load_info)  # noqa: T201

