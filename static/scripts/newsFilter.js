function render(json) {
    let block = $('#news-container a:last').clone();
    $('#news-container').empty();
    let articles = json['data'];
    for (let article of articles) {
        block.attr('href', '/news/detail/' + article['slug']);
        $('.single-content', block).text(article['title']);
        $('img.single-news-img', block).attr('src', article['url_to_image']);
        $('.single-time', block).text(article['published_at']);
        block.appendTo('#news-container');
        block = $('#news-container a:last').clone();
    }
}

function ajaxSend(url, params) {
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
        },
    }).then(response => response.json()).then(json => render(json)).catch(error => console.log(error));
}

let formElement = document.getElementById('filter-form');
formElement.addEventListener('submit', (e) => {
    e.preventDefault();
    let url = formElement.action;
    let params = new URLSearchParams(new FormData(formElement)).toString();
    ajaxSend(url, params);
});