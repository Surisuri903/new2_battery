$(function () {
    let start = js_vars.task.start,
        goal = js_vars.task.goal,
        minMoves = js_vars.task.min_moves,
        bonus = js_vars.bonus_per_trial,
        loss_per_extra_move = js_vars.loss_per_extra_move,
        towerTask = $('#tower-task'),
        rodsTask = $('#tower-task .rod'),
        rodsGoal = $('#tower-goal .rod'),
        RBY = {
            "R": "<div class=\"ball R\"></div>",
            "B": "<div class=\"ball B\"></div>",
            "Y": "<div class=\"ball Y\"></div>"
        },
        ifFirstMove = true,
        inputConfigSolved = false,
        moves = [],
        numMoves = 0,
        additionalBonus = null,
        spanNumMoves = $('span.num_moves'),
        inputTimeFirstMove = $('input[name=time_first_move]'),
        inputTimeLastMove = $('input[name=time_last_move]');

    let setFirstMoveTime = function (event) {
        if (ifFirstMove) {
            ifFirstMove = false;
            let d = new Date();
            inputTimeFirstMove.val(d.getTime());
        }
    };

    let setLastMoveTime = function (event) {
        if (!ifFirstMove) {
            let d = new Date();
            inputTimeLastMove.val(d.getTime());
        }
    };

    let resetMoves = function () {
        numMoves = 0;
        spanNumMoves.html(numMoves);
    };

    let setStart = function (start, tower) {
        resetMoves();
        let i;
        for (i = 1; i <= tower.length; i++) {
            let j;
            for (j = 1; j <= start[i].length; j++) {
                let ballColor = RBY[start[i][j - 1]];
                let rod = tower.eq(i - 1).find('.slot:nth-child(' + j + ')');
                rod.prepend(ballColor)
            }
        }
        let allBalls = rodsTask.find('.ball');
        allBalls.each(function () {
            if ($(this).parent().next(':has(.ball)').length === 0) {
                $(this).css({'cursor': 'pointer'});
            }
        })
    };

    let setGoal = function (goal, tower) {
        setStart(goal, tower)
    };

    let getCurrentState = function (tower) {
        setLastMoveTime();
        let currState = {};
        let colors = [];
        let i;
        for (i = 1; i <= tower.length; i++) {
            let balls = tower.eq(i - 1).find('.ball');
            balls.each(function () {
                colors.push($(this).attr('class').split(' ')[1]);
            });
            currState[i] = colors;
            colors = [];
        }
        moves.push(currState);
        return currState
    };

    let isGoalReached = function (goal, tower) {
        let currState = getCurrentState(tower);
        if (JSON.stringify(currState) === JSON.stringify(goal)) {
            setTimeout(function () {
                $('#task').css('display', 'none');
                window.scrollTo(0, 0);
                $('#feedback').css('display', 'block');
                $('#message-solved').css('display', 'block');
                $('#message-no-solved').css('display', 'none');
                additionalBonus = (bonus - (loss_per_extra_move * (numMoves - minMoves))) / 100;
                if (additionalBonus < 0) {
                    additionalBonus = 0
                }
                $('span.practice_payoff').html(additionalBonus.toFixed(2))
            }, 500);
            inputConfigSolved = true;
        }
    };

    let detachBalls = function () {
        $('.ball').remove()
    };

    let displayTask = function () {
        inputConfigSolved = false;
        $('#task').css('display', 'block');
        $('#feedback').css('display', 'none');
        detachBalls();
        setGoal(goal, rodsGoal);
        setStart(start, rodsTask);

        displayFeedback();
    };

    let displayFeedback = function () {
        setTimeout(function () {
            $('#task').css('display', 'none');
            $('#feedback').css('display', 'block');
            if (inputConfigSolved) {
                $('#message-solved').css('display', 'block');
                $('#message-no-solved').css('display', 'none');
            } else {
                $('#message-solved').css('display', 'none');
                $('#message-no-solved').css('display', 'block');
            }
        }, 1000 * 60);
    };

    displayTask();

    // Display tower with current configuration already set up
    setTimeout(function () {
        $('#tower-task').css('visibility', 'visible');
        $('#tower-goal').css('visibility', 'visible');
    }, 100);

    $('#try-again-button').on("click", function () {
        displayTask()
    });

    towerTask.on('click', '.ball', function () {
        let currRod = $(this).parents('.rod'),
            otherRods = $('.rod').not(currRod);
        let isTopMostBall = $(this).parent().next(':has(.ball)').length === 0;
        if ($('.selected').length === 0 && isTopMostBall) {
            $(this).addClass('selected');
            otherRods.css({"cursor": "pointer"});
            setFirstMoveTime()
        } else if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
            ++numMoves;
            spanNumMoves.html(numMoves);
            otherRods.css({"cursor": "default"});
            getCurrentState(rodsTask)
        }
    });
    towerTask.on('click', '.rod', function () {
        let selectedBall = $('.selected'),
            emptySlots = $(this).find('.slot:not(:has(*))');
        if (emptySlots.length !== 0 &&                              // rod with empty slot(s)
            $(this).find('.selected').length === 0) {        // rod with no selected ball
            emptySlots.first().append(selectedBall);                // append ball to the lowest empty slot
            selectedBall.removeClass('selected');
            rodsTask.css({"cursor": "default"});
            if (selectedBall.length > 0) {
                ++numMoves;
                spanNumMoves.html(numMoves);
            }
            isGoalReached(goal, rodsTask);
            let allBalls = rodsTask.find('.ball');
            allBalls.each(function () {
                if ($(this).parent().next(':has(.ball)').length === 0) {
                    $(this).css({'cursor': 'pointer'})
                } else {
                    $(this).css({'cursor': 'default'})
                }
            })
        }
    });
});