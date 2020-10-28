FROM code.ornl.gov:4567/6ng/choppy-lite/rasterpy:latest

LABEL maintainer="Joshua N. Grant <grantjn@ornl.gov>"
LABEL version='0.1.0'

COPY choppy-lite.py /usr/local/bin/choppy-lite.py
COPY choppy.py /usr/local/bin/choppy.py

RUN chmod +x /usr/local/bin/choppy-lite.py && \
	chmod +x /usr/local/bin/choppy.py && \
	mkdir /data

WORKDIR /data

ENTRYPOINT [ "choppy-lite.py" ]
