function MobileDetect() {
    var UA = navigator.userAgent.toLowerCase();
    return (/android|webos|iris|bolt|mobile|iphone|ipad|ipod|iemobile|blackberry|windows phone|opera mobi|opera mini/i.test(UA)) ? true : false;
}

jQuery(document).ready(function ($) {
    
    // Если браузер не мобильный, работаем
    if (!MobileDetect()) {
        $(".tovary__sizes-mobile").addClass(".tovary__sizes");
        $(".tovary__sizes").removeClass(".tovary__sizes-mobile");
        var

            $window = $(window), // Основное окно

            $target = $(".header"), // Блок, который нужно фиксировать при прокрутке

            $h = $target.offset().top; // Определяем координаты верха нужного блока (например, с навигацией или виджетом, который надо фиксировать)

        $window.on('scroll', function () {

            // Как далеко вниз прокрутили страницу
            var scrollTop = window.pageYOffset || document.documentElement.scrollTop;

            // Если прокрутили скролл ниже макушки нужного блока, включаем ему фиксацию
            if (scrollTop > $h) {

                $target.addClass("header__scrolled");

                // Иначе возвращаем всё назад
            } else {

                $target.removeClass("header__scrolled");
            }
        });
    }
    else{
        $(".tovary__sizes").addClass("tovary__sizes-mobile");
        $(".tovary__sizes-mobile").removeClass("tovary__sizes");
    }

    $('#openAlert').click(function () {
        $('#le-alert').addClass('in'); // shows alert with Bootstrap CSS3 implem
      });
  
    $('.close').click(function () {
        $(this).parent().removeClass('in'); // hides alert with Bootstrap CSS3 implem
    });

    // Get all elements with class="closebtn"
    var close = document.getElementsByClassName("closebtn");
    var i;
    
    // Loop through all close buttons
    for (i = 0; i < close.length; i++) {
        // When someone clicks on a close button
        close[i].onclick = function(){
        
            // Get the parent of <span class="closebtn"> (<div class="alert">)
            var div = this.parentElement;
        
            // Set the opacity of div to 0 (transparent)
            div.style.opacity = "0";
        
            // Hide the div after 600ms (the same amount of milliseconds it takes to fade out)
            setTimeout(function(){ div.style.display = "none"; }, 600);
        }
    }

    const images = document.querySelectorAll("img");

    const imgOptions = {};
    const imgObserver = new IntersectionObserver((entries, imgObserver) => {
    entries.forEach((entry) => {
        if (!entry.isIntersecting) return;

        const img = entry.target;
        img.src = img.src.replace("tr:bl-80", "tr:bl-0");
        imgObserver.unobserve(entry.target);
    });
    }, imgOptions);

    images.forEach((img) => {
        imgObserver.observe(img);
    });
});

document.body.onload = function () {
    setTimeout(function () {
        var preloader = document.getElementById('page-preloader');
        if (!preloader.classList.contains('done')) {
            preloader.classList.add('done');
        }
    }, 1000);
}
