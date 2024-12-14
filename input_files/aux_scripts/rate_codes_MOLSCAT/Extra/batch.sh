#!/bin/bash
for k in {1..1150..1}
do
./molscat-basic_H2 <$k> $k.out
done
