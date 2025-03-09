#!/bin/bash
for k in {1..1700}
do
./molscat-basic <$k> $k.out
done
