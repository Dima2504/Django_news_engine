$(document).ready(function () {
    let inProgress = false;
    let page = 2;
    $(window).scroll(function () {
        if ($(this).scrollTop() + $(this).height() >= $(document).height() - 800 && !inProgress) {
            let request = new XMLHttpRequest();
            request.open('GET', window.location.pathname + `?page=${page}`);
            request.responseType = 'json';
            request.setRequestHeader('Content-type', 'application/x-www-form-url');
            request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            request.addEventListener('readystatechange', function () {
                if (request.readyState === 4 && request.status === 200) {
                    let articles = request.response['data'];
                    for (let article of articles) {
                        let block = $('#news-container a:last').clone();
                        block.attr('href', '/news/detail/' + article['slug']);
                        $('.single-content', block).text(article['title']);
                        $('img.single-news-img', block).attr('src', article['url_to_image']);
                        $('.single-time', block).text(article['published_at']);
                        block.appendTo('#news-container');
                    }
                    if (request.response['has_next']) {
                        inProgress = false;
                        page++;
                    }
                }
            });
            request.send();
            inProgress = true;
        }
    })
});