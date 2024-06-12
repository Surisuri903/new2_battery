$(function () {
    let task = js_vars.task,
        rodsTask = $('#tower-task .rod'),
        rodsGoal = $('#tower-goal .rod'),
        RBY = {
            "R": "<div class=\"ball R\"></div>",
            "B": "<div class=\"ball B\"></div>",
            "Y": "<div class=\"ball Y\"></div>"
        },
        ifFirstMove = true,
        states = [],
        movesData = [],
        currMove = [],
        inputConfigSolved = $('input[name=config_solved]'),
        inputMoves = $('input[name=moves]'),
        inputStates = $('input[name=states_path]'),
        inputTimeStartTask = $('input[name=time_start_task]'),
        inputTimeFirstMove = $('input[name=time_first_move]'),
        inputTimeLastMove = $('input[name=time_last_move]');

    let setMinMoves = function () {
        $('#min-moves').text(task.min_moves);
    }

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

    let setTower = function (status, tower) {
        let i;
        for (i = 1; i <= tower.length; i++) {
            let j;
            for (j = 1; j <= status[i].length; j++) {
                let ballColor = RBY[status[i][j - 1]];
                tower.eq(i - 1).find('.slot:nth-child(' + j + ')').prepend(ballColor);
            }
        }
        let allBalls = rodsTask.find('.ball');
        allBalls.each(function () {
            if ($(this).parent().next(':has(.ball)').length === 0) {
                $(this).css({'cursor': 'pointer'})
            }
        })
    }

    let setStart = function (start, tower) {
        setTower(start, tower);
    };

    let setGoal = function (goal, tower) {
        setTower(goal, tower);
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
        states.push(currState);
        return currState
    };

    let isGoalReached = function (goal, tower) {
        let currState = getCurrentState(tower);
        if (JSON.stringify(currState) === JSON.stringify(goal)) {
            inputConfigSolved.val('True');
            inputMoves.val(JSON.stringify(movesData));
            inputStates.val(JSON.stringify(states));
            setTimeout(function () {
                $('#form').submit()
            }, 500);
        }
    };

    setStart(task.start, rodsTask);
    setGoal(task.goal, rodsGoal);
    setMinMoves();

    // Display tower with current configuration already set up
    setTimeout(function () {
        $('#tower-task').css('visibility', 'visible');
        $('#tower-goal').css('visibility', 'visible');
        inputConfigSolved.val('False');
        let d = new Date();
        inputTimeStartTask.val(d.getTime());
    }, 100);

    let rods = $('#tower-task .rod');
    let balls = $('#tower-task .ball');
    balls.on('click', function () {
        let currRod = $(this).parents('.rod'),
            otherRods = $('.rod').not(currRod);
        let currSlot = $(this).parents('.slot');
        let isTopMostBall = $(this).parent().next(':has(.ball)').length === 0;
        let d = new Date();
        if ($('.selected').length === 0 && isTopMostBall) {
            currMove.push(currSlot.attr('id'));
            currMove.push(d.getTime());
            $(this).addClass('selected');
            otherRods.css({"cursor": "pointer"});
            setFirstMoveTime()
        } else if ($(this).hasClass('selected')) {
            currMove.push(currSlot.attr('id'));
            currMove.push(d.getTime());
            movesData.push(currMove);
            currMove = [];
            $(this).removeClass('selected');
            otherRods.css({"cursor": "default"});
            getCurrentState(rodsTask)
        }
    });

    rods.on('click', function () {
        let selectedBall = $('.selected'),
            emptySlots = $(this).find('.slot:not(:has(*))');
        if (emptySlots.length !== 0 &&                   // rod with empty slot(s)
            $(this).find('.selected').length === 0 &&   // rod with no selected ball
            selectedBall.length !== 0) {                // a ball is selected
            emptySlots.first().append(selectedBall);    // append ball to lowest empty slot
            let d = new Date();
            currMove.push(emptySlots.first().attr('id'));
            currMove.push(d.getTime());
            movesData.push(currMove);
            currMove = [];
            selectedBall.removeClass('selected');
            rods.css({"cursor": "default"});
            isGoalReached(task.goal, rodsTask);
            let allBalls = rods.find('.ball');
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