#########################################################################
# File Name: script.sh
# Author: ma6174
# mail: ma6174@163.com
# Created Time: 2019年12月12日 星期四 13时26分30秒
#########################################################################
#!/bin/bash
git clone https://github.com/palliums-developers/exchange-matchengine.git


#for file in $(ls ./exchange-matchengine/violas_move/*.mvir)
#do
#	echo $file
#	./compiler $file  --deps ./exchange-matchengine/violas_move/mytoken.mv
#done

for file in $(ls ./exchange-matchengine/violas_move/*.mv)
do
	echo $file
	python3 ./violas_parse_code.py ./violas_data $file
done
