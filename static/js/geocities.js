function randomGeoImg() {
    var urls = ["http://i.mycommentspace.com/188/18833.gif",
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

function createBlinks() {
    var els = document.querySelectorAll('*');
    for (var i = 0; i < els.length; i++) {
        if (Math.random() < .1) {
            console.log("picked an element to make blink");
            var el = els[i]
            var f = function() {
                console.log("made an element blink");
                el.classList.add('blink');
            }
            setTimeout(f, Math.random() * 200);
        }
    }
    blink();
}

function blink() {
    var els = document.querySelectorAll('.blink');
    for (var i = 0; i < els.length; i++) {
        if (els[i].style.visibility == 'visible') {
            els[i].style.visibility = 'hidden';
        } else {
            els[i].style.visibility = 'visible';
        }
    }
    setTimeout(blink, 2000);
}
function runGeoFuncs() {
    geoImage();
    geoMarquee();
    createBlinks();
}

if (window.onload) {
	var prev = window.onload;
	window.onload = function() {
		prev();
		runGeoFuncs();
	}
} else {
	window.onload = runGeoFuncs;
}
