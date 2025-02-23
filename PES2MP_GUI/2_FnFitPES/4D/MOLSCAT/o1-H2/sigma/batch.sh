#!/bin/bash
for k in {1..852}
do
./molscat-basic <$k> $k.out
done
