document.addEventListener('DOMContentLoaded', () => {
    let lastScrollTop = 0;
    const header = document.querySelector('.header-main-page');
    
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (scrollTop > lastScrollTop) {
            header.style.display = 'none';
        } else {
            header.style.display = '';
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    }, false);
    })