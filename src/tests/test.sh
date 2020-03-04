declare -a get_arr=("test_domain" "test_ip")

method="GET"

for i in "${get_arr[@]}"
do
    rm "./$method/$i.out"
    touch "./$method/$i.out"
    echo "./$method/$i"
    cat "./$method/$i.in" | /bin/bash >> "./$method/$i.out"
    diff -Z -q "./$method/$i.out" "./$method/$i.check"
done

declare -a post_arr=("test")

method="POST"

for i in "${post_arr[@]}"
do
    rm "./$method/$i.out"
    touch "./$method/$i.out"
    echo "./$method/$i"
    cat "./$method/$i.in" | /bin/bash >> "./$method/$i.out"
    diff -Z -q "./$method/$i.out" "./$method/$i.check"
done