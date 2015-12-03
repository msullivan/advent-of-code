(for I in `seq 1 5000`; do printf "%d: " $I; head -c$I 1.realinput > 1.input; sh 1.sh; done) | grep -- -1 | head -n1
