let title = document.getElementsByName('title')[0];
let content = document.getElementsByName('content')[0];

let buttonList = document.querySelectorAll('button');
buttonList.forEach((button) =>
    button.onclick = goToNewPage);

function goToNewPage() {
    let new_url = new URL('http://localhost:8000/data-cleaning.html');
    new_url.searchParams.set('title', title.value);
    new_url.searchParams.set('content', content.value);
    window.location = new_url;
}