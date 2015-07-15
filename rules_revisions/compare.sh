#!/usr/bin/env bash

#vimdiff <(tidy -iq $1/IEEE_SoutheastCon_2016_Hardware_Competition_R.html) <(tidy -iq $2/IEEE_SoutheastCon_2016_Hardware_Competition_R.html)
vimdiff <(html2text $1/IEEE_SoutheastCon_2016_Hardware_Competition_R.html) <(html2text $2/IEEE_SoutheastCon_2016_Hardware_Competition_R.html)
