#!/bin/sh
cat "${1}/[IMPORTANT:-Info-+-Navigation]-Hub-Chapter-This-Way!.524996.html" | grep '<li><a' | cut -d'/' -f2 | cut -d'<' -f1 | awk 'BEGIN{FS=">"} {print $2 "\t" $1}' |sed 's/TheDespaxas-trunk.524999/A-sticky-situation--%5BTheDespaxas].332152/' |tr -d '"'

