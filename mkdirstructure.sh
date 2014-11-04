#!/bin/bash
#This script will create the directory structure for the files we use int he subtraction.

mkdir orig
mv *w.fits *w.weight.fits orig

for i in {0..10};
do
mkdir V$i
mv *w_fakesV$i.fits* V$i
done

