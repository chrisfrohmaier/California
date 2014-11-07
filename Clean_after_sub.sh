#!/bin/bash

#Script to clean the directories after we have performed the subtractions

ym=$1

for i in $ym
do
	for j in $i/C??
	do
		for k in $j/V?
		do
			#Put in here everything you want to remove
			echo $k/hot* $k/
		done
	done
done

echo Directory $1 has been cleaned.