$(function () {
    //Slider
    const intro = $("#intro");

    intro.slick({
        infinite: true,
        speed: 800,
        dots: false,
        autoplay: true,
        arrows: false,
        slidesToShow: 1,
        slidesToScroll: 1,
    });

    $("#intro__arrow--prev").on("click", function (event) {
        event.preventDefault();

        intro.slick('slickPrev');
    });

    $("#intro__arrow--next").on("click", function (event) {
        event.preventDefault();

        intro.slick('slickNext');
    });

    //Select
    $(".select").each(function () {

        let $this = $(this),
            selectOption = $this.find('option'),
            selectOptionLenght = selectOption.length,
            selectedOption = selectOption.filter(':selected'),
            dur = 500;

        $this.hide();

        $this.wrap('<div class="select"></div>');
        $('<div>', {
            class: 'select__gap',
            text: 'Select category...'
        }).insertAfter($this);

        let selectGap = $this.next('.select__gap'),
            caret = selectGap.find('.caret');

        $('<ul>', {
            class: 'select__list'
        }).insertAfter(selectGap);

        let selectList = selectGap.next('.select__list');

        for (let i = 0; i < selectOptionLenght; i++) {
            $('<li>', {
                class: 'select__item',
                html: $('<span>', {
                    text: selectOption.eq(i).text()
                })
            }).attr('data-value', selectOption.eq(i).val()).appendTo(selectList);
        }

        let selectItem = selectList.find('li');

        selectList.slideUp(0);

        selectGap.on('click', function () {

            if (!$(this).hasClass('on')) {
                $(this).addClass('on');
                selectList.slideDown(dur);

                selectItem.on('click', function () {
                    let chooseItem = $(this).data('value');

                    $('select').val(chooseItem).attr('selected', 'selected');
                    selectGap.text($(this).find('span').text());

                    selectList.slideUp(dur);
                    selectGap.removeClass('on');
                });
            } else {
                $(this).removeClass('on');
                selectList.slideUp(dur);
            }

        });

    });

    new WOW().init();
});
