#!/bin/bash
set -e -o pipefail

DIFFS="modules/appgw"

cd /Users/lpawlega/Git/vm-series-gh-actions/

if [ "$DIFFS" ]; then
  EXAMPLES_DISCOVERY=$(for M in $(echo "$DIFFS" | tr ',' '\n' | grep modules); do
    echo $(grep -rl "$M" examples/*/*.tf | sed -E "s/^(examples\/.*)\/.*$/\1/g")
  done | sort -u | awk NF)

  EXAMPLES_COMBINED=$(echo "$(echo $EXAMPLES_DISCOVERY | tr ' ' ','),$DIFFS" | tr ',' '\n' | awk NF | grep examples | sort -u)

  echo "::set-output name=examples::$(echo -n $EXAMPLES_COMBINED | tr ' ' ',')"
fi

cd -