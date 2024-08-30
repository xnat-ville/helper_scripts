#!/bin/sh

sed -e 's-/SCANS.*dcm--' -e "s/''//g" -e "s/'//g" $1

