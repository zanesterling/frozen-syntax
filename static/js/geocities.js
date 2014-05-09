function randomGeoImg() {
    var urls = ["https://images.encyclopediadramatica.es/a/a1/Bill_Gates.gif",
                "https://images.encyclopediadramatica.es/1/1b/Baby.gif",
                "http://enderpanda.com/data/images/hallo_gif_skull_1.gif",
                "https://pbs.twimg.com/profile_images/425274582581264384/X3QXBN8C.jpeg"
               ]
    return urls[Math.floor(Math.random() * urls.length)];
}

// Replace all images with random, awful geocities images
function geoImage() {
    var imgs = document.querySelectorAll('img');
    for (var i = 0; i < imgs.length; i++) {
        imgs[i].src = randomGeoImg();
    }
}

function geoMarquee() {
    var heads = document.querySelectorAll('h2');
    for (var i = 0; i < heads.length; i++) {
        if (Math.random() > .5) {
            var marq = document.createElement('marquee');
            marq.innerHTML = heads[i].innerHTML;
            heads[i].innerHTML = "";
            heads[i].appendChild(marq);
        }
    }
}
function runGeoFuncs() {
    geoImage();
    geoMarquee();
}
window.onload = runGeoFuncs;
