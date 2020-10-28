#!/usr/bin/env bash
set -eux
# environment {{{1 -----------------------------------------------------------
GDAL_VERSION=v2.4.0
LIBKML_VERSION=1.3.0
NETCDF_VERSION=4.7.2
PROJ_VERSION=6.2.0
GEOS_VERSION=3.7.0
NPROC=$(nproc)
echo -e "Configuring builds with \\e[33m$NPROC\\e[39m processors"

BUILD_DEPS="
	autoconf \
	automake \
	boost-dev \
	bison \
	build-base \
	ca-certificates \
	coreutils \
	curl \
	expat-dev \
	flex \
	freetype-dev \
	gettext \
	gettext-dev \
	git \
	lapack \
	libtool \
	libxml2 \
	libxml2-dev \
	libxslt-dev \
	linux-headers \
	glib \
	glib-dev \
	make \
	minizip-dev \
	openblas-dev \
	openssl \
	pkgconfig \
	procps \
	python3-dev \
	subversion \
	unzip \
	uriparser-dev \
	wget \
	zip \
	zlib-dev"

PERSISTS="\
	boost \
	make \
	g++ \
	gcc \
	cmake \
	expat \
	tar \
	openblas \
	file \
	gdal \
	gdal-dev \
	geos \
	gfortran \
	libc-dev \
	minizip \
	musl \
	musl-dev \
	python3 \
	python3-dev \
	python2 \
	python2-dev \
	py-gdal \
	py-pip \
	sqlite \
	sqlite-dev \
	uriparser \
	zlib"
# environment 1}}} ------------------------------------------------------------
# functions {{{1 -------------------------------------------------------------
# compileMessage {{{2 --------------------------------------------------------
compileMessage() {
	echo -e "Installing \\e[32m$1\\e[39m version \\e[36m$2\\e[39m"
}
# compileMessage 2}}} --------------------------------------------------------
# functions 1}}} -------------------------------------------------------------
# install {{{1 ---------------------------------------------------------------
# apk {{{2 -------------------------------------------------------------------
apk update && apk upgrade && \
	apk add --no-cache \
		--repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
		--repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
	$BUILD_DEPS $PERSISTS && \
	update-ca-certificates
# apk 2}}} -------------------------------------------------------------------
# PROJ {{{2 ------------------------------------------------------------------
compileMessage PROJ $PROJ_VERSION
mkdir /build && cd /build && \
	wget -q -O proj.tar.gz --no-verbose \
		http://download.osgeo.org/proj/proj-$PROJ_VERSION.tar.gz && \
	tar xzvf proj.tar.gz && \
	rm -f proj.tar.gz && \
	cd proj-$PROJ_VERSION/ && \
	./configure --prefix=/usr && \
	set -ex echo $NPROC && \
	make -j$NPROC && \
	make install && \
	cd .. && rm -rf proj-$PROJ_VERSION
# PROJ 2}}} ------------------------------------------------------------------
# LIBKML {{{2 ----------------------------------------------------------------
compileMessage LIBKML $LIBKML_VERSION
cd /build && \
	wget -q -O libkml.tar.gz --no-verbose \
		"https://github.com/libkml/libkml/archive/${LIBKML_VERSION}.tar.gz" && \
	tar --extract --file libkml.tar.gz && \
	cd libkml-${LIBKML_VERSION} && mkdir build && \
	cd build && cmake .. && make && make install && cd ../.. && \
	rm -r /build/*
# LIBKML 2}}} ----------------------------------------------------------------
# GEOS {{{2 ------------------------------------------------------------------
compileMessage GEOS $GEOS_VERSION
mkdir -p /build && cd /build && \
	wget --no-verbose \
		https://github.com/libgeos/geos/archive/${GEOS_VERSION}.tar.gz && \
	tar xzf $GEOS_VERSION.tar.gz && \
	cd geos-${GEOS_VERSION} && mkdir build && cd build && \
	cmake -DCMAKE_INSTALL_PREFIX=/usr ../ && \
	make install && cd ../.. && \
	rm -rf geos-${GEOS_VERSION}
# GEOS 2}}} ------------------------------------------------------------------
# NETCDF {{{2 ----------------------------------------------------------------
compileMessage NETCDF $NETCDF_VERSION
cd /build && \
	wget -q -O netcdf.tar.gz --no-verbose \
		"https://www.unidata.ucar.edu/downloads/netcdf-$NETCDF_VERSION.tar.gz" \
	&& tar -xzf netcdf.tar.gz && \
	cd netcdf && ./configure --prefix=/usr/local && make && make install && \
	cd .. && rm -rf netcdf
# NETCDF 2}}} ----------------------------------------------------------------
# GDAL {{{2 ------------------------------------------------------------------
compileMessage GDAL $GDAL_VERSION
cd /build && \
	wget -q -O gdal.tar.gz --no-verbose \
	"https://github.com/OSGeo/gdal/archive/${GDAL_VERSION}.tar.gz" && \
	tar --extract --file gdal.tar.gz --strip-components 1 && \
	cd gdal && \
	./configure --prefix=/usr \
		--with-libkml \
		--with-geos \
		--with-geotiff \
		--with-curl \
		--with-netcdf \
		--without-bsb \
		--without-dwgdirect \
		--without-ecw \
		--without-fme \
		--without-gnm \
		--without-grass \
		--without-grib \
		--without-hdf4 \
		--without-hdf5 \
		--without-idb \
		--without-ingress \
		--without-jasper \
		--without-mrf \
		--without-mrsid \
		--without-pcdisk \
		--without-pcraster \
		--without-webp \
	&& make -j$NPROC && make install
GDAL_VERSION=$(gdal-config --version | awk -F'[.]' '{print $1"."$2}')
# GDAL 2}}} ------------------------------------------------------------------
# python related {{{2 --------------------------------------------------------
pip install --upgrade pip --no-cache-dir && \
	pip install GDAL==$GDAL_VERSION \
		--no-cache-dir
pip install -r /requirements.txt --no-cache-dir 
# python related 2}}} --------------------------------------------------------
# installs 1}}} --------------------------------------------------------------
# cleanup {{{1 ---------------------------------------------------------------
cd / && \
	rm -rf /build && \
	rm -rf /var/cache/apk/* #&& \
  #apk del $BUILD_DEPS
# cleanup 1}}} ---------------------------------------------------------------
