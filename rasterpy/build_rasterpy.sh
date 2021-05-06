#!/usr/bin/env bash
# ex: set fdm=marker
# usage {{{1
#/ Usage:
#/       ./build.sh [OPTIONS]
#/
#/    -t|--tag)
#/       the tag to assign the docker image
#/
#/    -n|--no-cache)
#/       do not use the cache when building this image
#/
#/    -f|--file)
#/       the Dockerfile to specify during build
#/
#/    -h|-?|--help)
#/       show this help and exit
#/
# 1}}}
# environment {{{1
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT=${PROJECT:-"Rasterpy in $DIR"}
DOCKER_FILE="Dockerfile"
TAG="latest"
NOCACHED=""
# 1}}}
# functions {{{1
banner() { # {{{2
  BANNER=""
  BANNER="$BANNER\n  \033[32mRasterPy\033[39m"
  echo -e "$BANNER\n\n"
} # 2}}}
die() { # {{{2
  echo -e "\033[31mFAILURE:\033[39m $1"
  exit 1
} # 2}}}
warn() { # {{{2
  echo -e "\033[33mWARNING:\033[39m $1"
} # 2}}}
show_help() { # {{{2
  grep '^#/' "${BASH_SOURCE[0]}" | cut -c4- || \
    die "Failed to display usage information"
} # 2}}}
# 1}}}
# arguments {{{1
while :; do
  case $1 in # check arguments {{{2
    -t|--tag) # Docker tag {{{3
      TAG=$2
      shift 2
      ;; # 3}}}
    -n|--no-cache) # build without cache {{{3
      NOCACHED="--no-cache"
      shift
      ;; # 3}}}
    -f|--file) # Dockerfile to use {{{3
      DOCKER_FILE=$2
      shift 2
      ;; # 3}}}
    -h|-\?|--help) # help {{{3
      banner
      show_help
      exit
      ;; # 3}}}
    -?*) # unknown argument {{{3
      warn "Unknown option (ignored): $1"
      shift
      ;; # 3}}}
    *) # default {{{3
      break # 3}}}
  esac # 2}}}
done
# 1}}}
# logic {{{1
banner
DOCKER_BUILDKIT=1 docker build $NOCACHED  \
  -t "code.ornl.gov:4567/wstamp-analysis/choppy-lite/rasterpy:$TAG" . || \
  die "Image failed to build."
docker push "code.ornl.gov:4567/wstamp-analysis/choppy-lite/rasterpy:$TAG"
# 1}}}
