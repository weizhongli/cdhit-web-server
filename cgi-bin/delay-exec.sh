#!/bin/sh

if [ -n "$1" ]; then
  sleep_time=$1
else
  sleep_time=30
fi

if [ -n "$2" ]; then
  cpu_usage_cutoff=$2
else
  cpu_usage_cutoff=3200.0
fi

while [ 1 ]
do
##PID   USER    PR      NI      VIRT    RES     SHR     S       %CPU    %MEM    TIME+   COMMAND
##429294        liwz    20      0       10016   4276    3200    R       11.8    0.0     0:00.03 top
##1     root    20      0       171584  13108   8408    S       0.0     0.0     1:04.49 systemd
##2     root    20      0       0       0       0       S       0.0     0.0     0:02.91 kthreadd
##3     root    0       -20     0       0       0       I       0.0     0.0     0:00.00 rcu_gp
##4     root    0       -20     0       0       0       I       0.0     0.0     0:00.00 rcu_par_gp

    cpu=0
    for i in $(top -b  -n 1 | sed -n '8, 12{s/^ *//;s/ *$//;s/  */\t/gp;};12q' | cut -f 9); do
        cpu=$(echo "$i + $cpu" | bc)
    done

    flag=$(echo "$cpu > $cpu_usage_cutoff" |bc -l)
    echo $flag
    if [ $flag -eq 1 ]; then
        echo "wait, current cpu usage $cpu"
    else
        echo "cpu available, current cpu usage $cpu"
        break
    fi

    sleep $sleep_time
done
