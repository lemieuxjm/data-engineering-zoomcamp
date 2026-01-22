# base Docker image that we will build on
FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas pyarrow

# set up the working directory inside the container
WORKDIR /app
ENV PATH="/app/.venv/bin/:$PATH"

# copy py files to container
COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

# copy the script to the container. 1st name is source file, 2nd (.) is destination
COPY ingest-data.py .

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["uv", "run", "python", "ingest-data.py"]