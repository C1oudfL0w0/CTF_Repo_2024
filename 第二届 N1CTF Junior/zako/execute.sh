#!/bin/bash

reject(){
    echo ${1}
    exit 1
}

XXXCMD=$1

awk -v str="${XXXCMD}" \
'BEGIN{
    deny="`;&$(){}[]!@#$%^&*-";
    for(i = 1; i <= length(str); i++){
        char = substr(str, i, 1);

        for(x = 1; x < length(deny)+1; x++){
            r = substr(deny, x, 1);
            if(char == r) exit 1;
        }
    }
}'

[ $? -ne 0 ] && reject "NOT ALLOW 1"

eval_cmd=`echo "${XXXCMD}" | awk -F "|" \
'BEGIN{
    allows[1] = "ls";
    allows[2] = "makabaka";
    allows[3] = "whoareu";
    allows[4] = "cut~no";
    allows[5] = "grep";
    allows[6] = "wc";
    allows[7] = "杂鱼❤~杂鱼❤~";
    allows[8] = "netstat.jpg";
    allows[9] = "awsl";
    allows[10] = "dmesg";
    allows[11] = "xswl";
}{
    num=1;
    for(i=1; i<=NF; i++){
        for(x=1; x<=length(allows); x++){
            cmpstr = substr($i, 1, length(allows[x]));
            if(cmpstr == allows[x])
                eval_cmd[num++] = $i;
        }
    }
}END{
    for(i=1; i<=length(eval_cmd); i++) {
        if(i!=1)
            printf "| %s", eval_cmd[i];
        else
            printf "%s", eval_cmd[i];
    }
}'`

[ "${XXXCMD}" = "" ] && reject "NOT ALLOW 2"


eval ${eval_cmd}
