// Fix css animations being run on page load.
// From http://www.pencilscoop.com/2014/03/prevent-css-transitions-running-on-page-load/
window.addEventListener('load',function load() {
    window.removeEventListener('load', load, false);
    document.body.classList.remove('load');
},false);
