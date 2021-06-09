# download from github
repos=`cat github.txt`
for repo in $repos; do
    echo $repo
#     echo ${repo#*/}
    if [ -d benchmarks/${repo#*/} ]; then
        echo "====== already exist"
    else
        git clone https://github.com/$repo benchmarks/${repo#*/}
    fi
done

# exit 0


# find all the .kicad_pcb files
files=`find benchmarks -name *.kicad_pcb`
# echo $files
mkdir -p output
for f in $files; do
    echo $f
    json="output/${f//\//-}.json"
    # if the pathname contains space, the for loop won't pick up the full path
    if [ -f $f ]; then
        # run racket
        if ! [ -f $json ]; then
            # DEBUG not running main.rkt
            # racket main.rkt $f $json
            echo "skip"
        fi
        echo "... $json"
        if [ -f $json ]; then
            python3 main.py $json
        fi
    fi
done
# run rkt
# run py
# racket main.rkt benchmarks/HHKB_controller.kicad_pcb out.json
# python main.py out.json