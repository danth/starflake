FROM python:3.9

WORKDIR /usr/src/starflake
# Data volume should be mounted here
ENV HOME=/starflake

# Install dependencies
COPY setup.py README.md ./
RUN pip install --no-cache-dir -e .

# Copy code
COPY . .

HEALTHCHECK CMD discordhealthcheck || exit 1
CMD [ "starflake" ]
