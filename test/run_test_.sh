#!/bin/bash

help() {
    echo "This is a test tool for Blog Linker."
    echo "****************************************"
    echo "./run_test_.sh <command>"
    echo "command:"
    echo -e "\tinit\tinit your http server."
    echo -e "\ttest\tcrawel local html file with your test json file."
    echo -e "\thelp\tprint this help."
    echo "****************************************"

}
test() {
    echo "all new links are results for your links resolution rule."
    echo "get all links for test.example1.json..."
    python3 ../src/main.py -b test.example1.json -s ../blog_json_config/history_links.json
    echo "done"

    echo "get all links for test.example2.json..."
    python3 ../src/main.py -b test.example2.json -s ../blog_json_config/history_links.json
    echo "done"
}

if [ "$1" == "init" ]; then
    echo "http server will start. please run './run_test_.sh test' in another terminal. "
    python3 -m http.server
elif [ "$1" == "test" ]; then
    test
elif [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    help
else
    echo "args error"
    help
fi
