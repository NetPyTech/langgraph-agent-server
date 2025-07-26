FROM langchain/langgraph-api:3.11


# -- Adding local package . --
ADD .
# -- End of local package . --

# -- Installing all local dependencies --
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.txt
# -- End of local dependencies install --
ENV LANGSERVE_GRAPHS='{"agent": "./main.py:graph"}'

# -- Ensure user deps didn't inadvertently overwrite langgraph-api
RUN mkdir -p /api/langgraph_api /api/langgraph_runtime /api/langgraph_license &&     touch /api/langgraph_api/__init__.py /api/langgraph_runtime/__init__.py /api/langgraph_license/__init__.py
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir --no-deps -e /api
# -- End of ensuring user deps didn't inadvertently overwrite langgraph-api --
# -- Removing pip from the final image ~<:===~~~ --
RUN pip uninstall -y pip setuptools wheel &&     rm -rf /usr/local/lib/python*/site-packages/pip* /usr/local/lib/python*/site-packages/setuptools* /usr/local/lib/python*/site-packages/wheel* &&     find /usr/local/bin -name "pip*" -delete
# -- End of pip removal --

WORKDIR /


###------------ Building and Running the docker container ---------------------------

# docker build -t initial_system_workflow -f Dockerfile .

# docker run -p 8000:8000 --env-file .env initial_system_workflow (For using env files)