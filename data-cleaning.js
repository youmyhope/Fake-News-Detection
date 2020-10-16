var current_url = new URL(window.location);
let title = current_url.searchParams.get("title");
let content = current_url.searchParams.get("content");

query_url = new URL('http://localhost:8001/dataCleaning');
query_url.searchParams.set('title', title);
query_url.searchParams.set('content', content);

$.get(query_url, function(response){
    orginalTitle = response.orginal_title;
    orginalContent = response.orginal_content;

    finalTitle = response.final_title;
    finalContent = response.final_content;

    let final_title = document.getElementsByName("final_title")[0];
    let final_content = document.getElementsByName("final_content")[0];

    let showTitleOrginal = document.getElementsByName('show_orginal_title')[0];
    let showContentOrginal = document.getElementsByName('show_orginal_content')[0];

    final_title.value = finalTitle;
    final_content.innerText = finalContent;

    showTitleOrginal.onclick = function () {
        if (showTitleOrginal.innerText == 'Show title after data cleaning') {
            final_title.value = finalTitle;
            showTitleOrginal.innerText = 'Show orginal title';
        }
        else {
            console.log(1);
            final_title.value = orginalTitle;
            showTitleOrginal.innerText = 'Show title after data cleaning';
        }
    };

    showContentOrginal.onclick = function () {
        if (showContentOrginal.innerText == 'Show content after data cleaning') {
            final_content.innerText = finalContent;
            showContentOrginal.innerText = 'Show orginal content';
        }
        else {
            final_content.innerText = orginalContent;
            showContentOrginal.innerText = 'Show content after data cleaning';
        }
    };
    let showTheTruth = document.getElementsByName('show_the_truth')[0];
    showTheTruth.onclick = function () {
        let answer_url = new URL('http://localhost:8001/getTheTruth');
        answer_url.searchParams.set('title', finalTitle);
        answer_url.searchParams.set('content', finalContent);
        $.get(answer_url, function(response){
            answer = response.answer;
            let showResult = document.getElementsByName('show_result')[0];
            let iconResult = document.getElementsByName('icon_result')[0];
            if (answer == 0) {
                showResult.innerText = 'Fake news!!!';
                iconResult.src = "./icon/cross.png";
                iconResult.style.width = "50px";
            }
            else {
                showResult.innerText = 'True news!!!';
                iconResult.src = "./icon/check.png";
                iconResult.style.width = "50px";
            }
        }, "json");
    }
}, "json");