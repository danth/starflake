FROM python:3.9

WORKDIR /usr/src/starflake

# Install dependencies
COPY setup.py README.md ./
RUN pip install --no-cache-dir -e .

# Copy code
COPY . .

HEALTHCHECK CMD discordhealthcheck || exit 1
CMD [ "starflake" ]
