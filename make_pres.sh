#!/bin/bash

FP="./_presentations/$1.html"

echo "---" >> $FP
echo "layout: presentation" >> $FP
echo "pres_title: $1" >> $FP
echo "---" >> $FP
echo "" >> $FP
echo "class: center, middle" >> $FP
echo "# $1" >> $FP
echo "" >> $FP
echo "---" >> $FP
echo "" >> $FP

vim $FP 
