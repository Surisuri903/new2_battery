$(function () {
    let isExplodedField = $('input[name=is_exploded]'),
        pointsField = $('input[name=points]'),
        totalPoints = $('.bart-total-points'),
        $balloon = $('.bart-balloon-img'),
        currentBalloon = $('.bart-current-balloon'),
        scale = 1,
        growthUnit = parseInt((parseInt($balloon.css('top')) - 20) / js_vars.max_num_pumps) * 0.01,
        numPumps = 0;

    let inflateBalloon = function () {
        scale += growthUnit
        $balloon.css({'transform': 'scale(' + scale + ')'});
    };

    let explodeBalloon = function () {
        $balloon.explode({
            "minWidth": 1, "maxWidth": 20, "radius": 300, "minRadius": 50, "release": false, "fadeTime": 100,
            "recycle": false, "recycleDelay": 0, "explodeTime": 199, "round": false, "minAngle": 0, "maxAngle": 155,
            "gravity": 0, "groundDistance": 500
        });
        isExplodedField.val('True');
        pointsField.val(0);
        numPumps = -1;
        setTimeout(function () {
            $('#form').submit()
        }, js_vars.sec_delay_submit * 1000)
    }

    let pumping = function () {
        let currentBalloonVal = +currentBalloon.html();
        if (numPumps >= 0 && numPumps <= js_vars.max_num_pumps) {
            numPumps++;
            if (numPumps < js_vars.breaking_point) {
                inflateBalloon();
                currentBalloonVal += js_vars.points_per_pump;
                currentBalloon.html(currentBalloonVal)
            } else {
                explodeBalloon()
            }
        }
    }

    let stopPumping = function () {
        if (numPumps >= 0 && numPumps <= js_vars.max_num_pumps) {
            pointsField.val(numPumps * js_vars.points_per_pump);
            isExplodedField.val('False');
            numPumps = -1;
            let currentBalloonVal = +currentBalloon.html(),
                totalPointsVal = +totalPoints.html();
            totalPoints.html(totalPointsVal + currentBalloonVal);
            setTimeout(function () {
                $('#form').submit()
            }, js_vars.sec_delay_submit * 1000)
        }
    }

    $('.bart-pump-button').on('click', pumping);
    $('.bart-stop-button').on('click', stopPumping);
});