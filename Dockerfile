FROM ubuntu:20.04 AS builder

# Env variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH="$PYTHONPATH:/code/SuperBuild/install/lib/python3.8/dist-packages:/code/SuperBuild/src/opensfm" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/code/SuperBuild/install/lib"

# Prepare directories
WORKDIR /code

# Copy everything
COPY . ./

# Run the build
RUN bash configure.sh install

# Clean Superbuild
RUN rm -rf \
  /code/SuperBuild/build/opencv \
  /code/SuperBuild/download \
  /code/SuperBuild/src/ceres \
  /code/SuperBuild/src/entwine \
  /code/SuperBuild/src/gflags \
  /code/SuperBuild/src/hexer \
  /code/SuperBuild/src/lastools \
  /code/SuperBuild/src/laszip \
  /code/SuperBuild/src/mvstexturing \
  /code/SuperBuild/src/opencv \
  /code/SuperBuild/src/opengv \
  /code/SuperBuild/src/pcl \
  /code/SuperBuild/src/pdal \
  /code/SuperBuild/src/openmvs \
  /code/SuperBuild/build/openmvs \
  /code/SuperBuild/src/vcg \
  /code/SuperBuild/src/zstd

# find in /code and delete...
RUN find /code \
# ...*static* libraries...
  -type f -name "*.a" -delete \
# ...and intermediate object files
  -or -type f -name "*.o" -delete

### END Builder

### Use a second image for the final asset to reduce the number and
# size of the layers.
FROM ubuntu:20.04

# Env variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH="$PYTHONPATH:/code/SuperBuild/install/lib/python3.8/dist-packages:/code/SuperBuild/src/opensfm" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/code/SuperBuild/install/lib"

WORKDIR /code

# Copy everything we built from the builder
COPY --from=builder /code /code

# Copy the Python libraries installed via pip from the builder
COPY --from=builder /usr/local /usr/local

# Install shared libraries that we depend on via APT, but *not*
# the -dev packages to save space!
RUN bash configure.sh installruntimedepsonly \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
  && apt-get update -y \
  && apt-get install --no-install-recommends -y \
  curl \
  nodejs \
  imagemagick \
  gdal-bin \
  git \
  libgdal-dev

#prepare node installation
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -

#install obj2gltf
RUN npm -g install github:AnalyticalGraphicsInc/obj2gltf.git

COPY ua_postprocessing.py /code/ua_postprocessing.py
COPY awscli_util.py /code/awscli_util.py


# Entry point
ENTRYPOINT ["python3", "/code/run.py"]
