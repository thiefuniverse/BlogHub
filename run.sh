#!/bin/bash

# you need modify this owner name to your name in github.
owner_name=thiefuniverse

# you should change this project_name if you change repo name after you forked BlogLinker
project_name=BlogLinker

# config your issue button for subscribing.
issue_button_text="Subscribe Blog"

# creator_name
check_update() {
    # crawel blog and update history links file.
    # !!! blog_json_config/flythief.example.json will be modified by user
    python3 src/main.py -b blog_json_config/flythief.example.json -s blog_json_config/history_links.json
}
clean_new_links() {
    rm ./new_links.txt
}

create_issue_rvl=1
create_issue() {
    echo "create issue..."
    # create issue
    curl -H "Accept: application/json" \
    --header "Authorization: token $GITHUB_TOKEN" \
    -H "Content-type: application/json" -X POST -d '{"title":"BlogLinker_generated", "body":"this issue is created by BlogLinker for blog subscribe."}' https://api.github.com/repos/$owner_name/$project_name/issues \
    > response.json

    echo "response: "
    cat response.json
    response=$(jq .url response.json)
    if [ "$response" == "null" ]; then
       create_issue_rvl=1
       echo "create issue error"
       exit
    fi
    echo $response > issue_flag.txt
    create_issue_rvl=0
    echo "after create issue..."
}

generate_subscriber_guide() {
    issue_url=$(cat issue_flag.txt)
    issue_url=${issue_url#"\""}
    issue_url=${issue_url%"\""}

    echo -e "<!-- Place this tag where you want the button to render. --> \n <a class=\"github-button\" href=\"$issue_url\" data-icon=\"octicon-issue-opened\" aria-label=\"Issue ntkme/github-buttons on GitHub\">$issue_button_text</a>" > issue_track.html
    echo -e "\n<!-- Place this tag in your head or just before your close body tag. --> \n <script async defer src=\"https://buttons.github.io/buttons.js\"></script>" >> issue_track.html

}

comment_issue() {
    echo "comment issue..."
    post_json_data="post.json"
    issue_url=$(cat issue_flag.txt)
    issue_url=${issue_url#"\""}
    issue_url=${issue_url%"\""}
    comment_content="This blog has updated something. Maybe you want to check it. Links are here! Thanks :)    "
    links="$(cat new_links.txt)"
    echo "new links are here: $links"
    if [ "$links" == "" ]; then
        echo "no new links"
        exit
    fi
    comment_content=${comment_content}"$links"
    jq -n --arg comment_content "$comment_content" '{"body":$comment_content}' > $post_json_data

    curl -H "Accept: application/json" \
    --header "Authorization: token $GITHUB_TOKEN" \
    -H "Content-type: application/json" -X POST -d @$post_json_data $issue_url/comments
    echo "after comment issue..."
    rm $post_json_data
}

# save history_links.json
save_history() {
    if [ -f "new_links.txt" ]; then
        git config credential.helper "store --file=.git/credentials"
        echo "https://${GITHUB_TOKEN}:@github.com" > .git/credentials
        git add blog_json_config/history_links.json 
        git add issue_track.html
        git commit -m "travis ci automatically udpate history_links.json, issue_track.html"
        if [ $? == 0 ]; then
            git push origin master
            exit 0
        else
            exit 1
        fi
    fi
    exit 0
}

lock_issue() {
    issue_url=$(cat issue_flag.txt)
    issue_url=${issue_url#"\""}
    issue_url=${issue_url%"\""}
    echo "issue_url:$issue_url"
    # lock issue
    curl -H "Accept: application/json" \
    --header "Authorization: token $GITHUB_TOKEN" \
    -H "Content-type: application/json" -X PUT -d '{"locked":"true", "active_lock_reason":"too heated"}' $issue_url/lock
}

blog_linker_main() {
    if [ -f "./issue_flag.txt" ]; then
        check_update
        comment_issue
        generate_subscriber_guide
    else
        create_issue
        if [ $create_issue_rvl == 0 ];then
            lock_issue
            check_update
        fi
    fi
    save_history
    clean_new_links
}
# main entrance
if [ "$1" == "push" ]; then
    save_history
else
    blog_linker_main
fi