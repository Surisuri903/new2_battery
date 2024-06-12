$(window).on('load', function () {

    document.getElementById("door_falling").volume = 0.4;
    document.getElementById("door_opening").volume = 0.4;
    document.getElementById("dying").volume = 0.4;
    document.getElementById("winning").volume = 0.4;

    // Selectors
    let timer_started = js_vars.time_start !== 0,
        timeoutModal = $('#timeout-modal'),
        panel = $('#zurich-prosocial-game-side-panel'),
        h = panel.innerHeight(),
        audios = $('#audio-container'),
        keys = $('.key-holder div div'),
        doorDivs = $('.door'),
        egoArrows = $('.arrow-ego'),
        alterArrows = $('.arrow-alter'),
        players = {'ego': $('div[data-player=ego]'), 'alter': $('div[data-player=alter]')},
        canvasContainer = $('#canvas-container'),
        grid = document.querySelector('#canvas-grid'),
        canvas = document.querySelector('#canvas-zurich-prosocial-game'),
        ctxGrid = grid.getContext("2d"),
        ctx = canvas.getContext("2d"),
        canvasW, canvasH, tileW, tileH,

        // Game parameters
        Game = Object.assign({}, js_vars.game),
        GameStatus = Object.assign({}, js_vars.game_status),
        atlas = new Image(),
        atlasTransparent = new Image(),
        deathTimer = {'ego': [], 'alter': []},
        closedDoors = {'ego': [], 'alter': []},
        doorFalling = {'ego': false, 'alter': false},
        alterMoving,
        p = 0;

    Game.updateStatus = function () {
        GameStatus.timestamp = new Date().getTime();
        liveSend(GameStatus);
    };

    Game.setElementsSize = function () {
        canvasContainer.width(h);
        canvas.height = grid.height = h;
        canvas.width = grid.width = h;
        canvasW = canvas.clientWidth;
        canvasH = canvas.clientHeight;
        tileW = Math.round(canvasW / Game.cols);
        tileH = canvasH / Game.rows;

        $('.emoji').css({'width': tileW - tileW / 4, 'height': tileW - tileW / 4});
        $('.emoji-container[data-player=alter] .emoji').css({'background': Game.alter_color})
        ;
        $('.arrow-container').css({'width': tileW});
        $('.door img').css({'width': tileW - 1, 'height': tileH - 1});
        $('.doors-holder div').width(doorDivs.width()).height(tileH - 1);
        $('.key-holder img').css({'width': tileW - tileW / 4});
        $('.key-holder div').width(keys.width()).height(keys.height());
    };

    Game.drawGrid = function () {
        for (let x = 0; x <= canvasW; x += tileW) {
            ctxGrid.moveTo(0.05 + x + p, p);
            ctxGrid.lineTo(0.05 + x + p, canvasH + p);
        }

        for (let x = 0; x <= canvasH; x += tileH) {
            ctxGrid.moveTo(p, 0.05 + x + p);
            ctxGrid.lineTo(canvasW + p, 0.05 + x + p);
        }
        ctxGrid.strokeStyle = '#000000';
        ctxGrid.lineWidth = 0.1;
        ctxGrid.stroke();
    };

    Game.drawMap = async function () {
        if (ctx === null) {
            return;
        }
        for (var y = 0; y < Game.rows; y++) {
            for (var x = 0; x < Game.cols; x++) {
                let t = Game.map[((y * Game.cols) + x)],
                    h = atlas.naturalHeight;
                ctx.drawImage(atlas, t * h, 0, h, h, x * tileW, y * tileH, tileW, tileH);
            }
        }
        this.drawGrid();
    };

    Game.disablePath = function (path) {
        for (let i = 0; i < path.length; i++) {
            let s = path[i],
                y = s[0],
                x = s[1],
                t = Game.map[((y * Game.cols) + x)],
                h = atlasTransparent.naturalHeight;
            ctx.drawImage(atlasTransparent, t * h, 0, h, h, x * tileW, y * tileH, tileW, tileH);
        }
    };

    window.liveRecv = (data) => Game.initTimer(data);

    if (timer_started) {
        liveSend('start_timer');
    }

    Game.initTimer = function (data) {
        timer_started = true;

        let currentDate = new Date(),
            remainingTimeoutSeconds = data.time_left,
            milliseconds = Math.floor(remainingTimeoutSeconds * 1000);
        $('#sec-left').countdown(currentDate.valueOf() + milliseconds)
            .on('update.countdown', function (event) {
                if (Game.player_end('ego') && (Game.player_end('alter') || Game.is_solo_game)) {
                    $(this).countdown('stop');
                }

                $(this).html(event.offset.totalSeconds);

                let door_num = GameStatus.doors.filter(d => d.fallen === true).length,
                    secondsPassed = Game.sec_per_trial - event.offset.totalSeconds;

                if (Game.doors_times[door_num] <= secondsPassed) {
                    Game.setFallingDoors(door_num);
                }
            })
            .on('finish.countdown', function () {
                if (!Game.player_end('ego') || !Game.player_end('alter')) {
                    timeoutModal.modal('show');
                    GameStatus.timeout = true;
                    Game.updateStatus();
                }
                Game.end();
            })
    };

    Game.getPosition = function (s) {
        // TODO: fix Uncaught Type s
        return {'left': s[1] * tileW + tileW / 2, 'top': s[0] * tileH + tileH / 2}
    };

    Game.setPosition = function (el, s, dir = false, delay = false) {
        if (!dir) {
            el.animate(Game.getPosition(s), 200);
        } else {
            let egoArrow = $('.arrow-active');
            egoArrow.off('click', Game.arrowAction);
            el.animate({opacity: 0}, 200, function () {
                el.css(Game.getPosition(s));
                el.attr('data-dir', s[2]);
                if (delay) {
                    setTimeout(function () {
                        el.animate({opacity: 1}, 200, function () {
                            egoArrow.on('click', Game.arrowAction);
                            if (closedDoors['ego'].length === 0) {
                                egoArrow.show();
                            }
                        })
                    }, 1000 * Game.sec_interval_ego_step - 400)
                } else {
                    el.animate({opacity: 1}, 200, function () {
                        egoArrow.on('click', Game.arrowAction);
                        if (closedDoors['ego'].length === 0) {
                            egoArrow.show();
                        }
                    })
                }

            });
        }
    };

    Game.setPlayers = function () {
        let egoPath = GameStatus.ego_path === -1 ? 0 : GameStatus.ego_path;
        Game.setPosition(players['ego'], Game.paths['ego'][egoPath][GameStatus.ego_position]);

        if (!Game.is_solo_game) {
            Game.setPosition(players['alter'], Game.paths['alter'][Game.alter_path][GameStatus.alter_position]);
            if (GameStatus.ego_position > 0) {
                if (closedDoors['alter'].length === 0) {
                    Game.moveAlter();
                } else {
                    Game.alterUseKey(closedDoors['alter'][0]);
                }
            }
        }

        if (GameStatus.dead_players.indexOf('ego') > -1) {
            players['ego'].addClass('emoji-dead');
        } else if (GameStatus.dead_players.indexOf('alter') > -1) {
            players['alter'].addClass('emoji-dead');
        }
    };

    Game.setArrows = function (delay = true) {
        if (GameStatus.ego_position > 0 && GameStatus.ego_position < Game.paths_length) {
            egoArrows.hide();
            egoArrows.eq(GameStatus.ego_path).addClass('arrow-active');
            let egoArrow = $('.arrow-active');
            Game.setPosition(egoArrow, Game.paths['ego'][GameStatus.ego_path][GameStatus.ego_position + 1], true, delay);
            if (closedDoors['ego'].length > 0) {
                egoArrow.hide();
            }
        } else if (GameStatus.ego_position === 0) {
            egoArrows.on('click', Game.arrowAction);
            Game.setPosition(egoArrows.eq(0), Game.paths['ego'][0][GameStatus.ego_position + 1], true, delay);
            Game.setPosition(egoArrows.eq(1), Game.paths['ego'][1][GameStatus.ego_position + 1], true);
        }
        if (GameStatus.alter_position === 0 && !Game.is_solo_game) {
            Game.setPosition(alterArrows.eq(0), Game.paths['alter'][0][GameStatus.alter_position + 1], true, delay);
            Game.setPosition(alterArrows.eq(1), Game.paths['alter'][1][GameStatus.alter_position + 1], true, delay);
        } else if (GameStatus.alter_position > 0) {
            alterArrows.hide();
        }
    };

    Game.setAlterPath = function () {

        if (GameStatus.alter_position !== 0) {
            Game.disablePath(Game.paths['alter'][Math.abs(Game.alter_path - 1)]);
        } else {
            setTimeout(function () {
                Game.disablePath(Game.paths['alter'][Math.abs(Game.alter_path - 1)]);
                GameStatus.alter_position++;
                alterArrows.hide();
                Game.setPosition(players['alter'], Game.paths['alter'][Game.alter_path][GameStatus.alter_position]);
                if (GameStatus.ego_position > 0) {
                    if (!timer_started) {
                        liveSend('start_timer');
                    }
                    Game.setArrows();
                    Game.moveAlter();
                }

                Game.updateStatus();

            }, 1000 * 2)
        }
    };

    Game.moveAlter = function () {
        alterMoving = setInterval(function () {
            if (Game.player_end('alter') || GameStatus.ego_path === -1 || doorFalling['alter']) {
                clearInterval(alterMoving);
                if (Game.player_end('alter')) {
                    Game.updateStatus();
                    let winningSound = audios.find('#winning');
                    Game.playAudio(winningSound, Game.end);
                }
                return;
            }
            GameStatus.alter_position++;
            Game.setPosition(players['alter'], Game.paths['alter'][Game.alter_path][GameStatus.alter_position]);
        }, 1000 * Game.sec_interval_alter_step)
    };

    Game.moveEgo = function () {
        GameStatus.ego_position++;
        Game.updateStatus();

        Game.setPosition(players['ego'], Game.paths['ego'][GameStatus.ego_path][GameStatus.ego_position]);
        if (GameStatus.alter_position > 0 || Game.is_solo_game) {
            if (!timer_started) {
                liveSend('start_timer');
            }
            if (!Game.player_end('ego')) {
                Game.setArrows();
            }
        }

        if (Game.player_end('ego')) {
            let winningSound = audios.find('#winning');
            Game.playAudio(winningSound, Game.end);
        }
    };

    Game.arrowAction = function () {

        egoArrows.hide();
        if (GameStatus.ego_path === -1) {
            GameStatus.ego_path = egoArrows.index($(this));
            Game.disablePath(Game.paths['ego'][Math.abs(GameStatus.ego_path - 1)]);
            Game.moveEgo();
            if (GameStatus.alter_position > 0 && !Game.is_solo_game) {
                Game.moveAlter();
            }

        } else if (!doorFalling['ego']) {
            Game.moveEgo();
        }
    };

    Game.toggleEmojiBlockedAnimation = function (player) {
        if (
            GameStatus.dead_players.indexOf(player) === -1 &&
            closedDoors[player].length >= 1
        ) {
            players[player].children('.emoji').addClass('emoji-blocked');
        } else if (
            GameStatus.dead_players.indexOf(player) !== -1 ||
            closedDoors[player].length === 0
        ) {
            players[player].children('.emoji').removeClass('emoji-blocked');
        }
    };

    Game.start = function () {
        this.setElementsSize();
        this.drawMap();
        console.log(GameStatus)

        if (GameStatus.ego_position > 0) {
            Game.disablePath(Game.paths['ego'][Math.abs(GameStatus.ego_path - 1)]);
        }
        if (!Game.is_solo_game) {
            Game.setAlterPath();
            setTimeout(function(){

                if (GameStatus.ego_position == 0) {
                 GameStatus.ego_path = 0;
                 Game.disablePath(Game.paths['ego'][Math.abs(GameStatus.ego_path - 1)]);
                 Game.moveEgo();
                 Game.moveAlter();
                 Game.updateStatus();
             }}, 10000);
        }

        this.setFallenDoors();
        this.setArrows(delay = false);
        this.setPlayers();

        $('#zurich-prosocial-game').animate({opacity: 1}, 1000);
    };

    Game.player_end = function (player) {
        if (player === 'ego') {
            return GameStatus.ego_position === Game.paths_length || GameStatus.dead_players.indexOf(player) > -1
        } else {
            return GameStatus.alter_position === Game.paths_length || GameStatus.dead_players.indexOf(player) > -1
        }
    };

    Game.get_other_player = function (player) {
        let other = {'ego': 'alter', 'alter': 'ego'};
        return other[player];
    };

    Game.player_dies = function (player) {
        if (GameStatus.dead_players.indexOf(player) === -1) {
            if (player === 'ego') {
                GameStatus.ego_lost = true;
            }

            let dyingSound = audios.find('#dying');
            GameStatus.dead_players.push(player);
            Game.toggleEmojiBlockedAnimation(player);
            players[player].addClass('emoji-dead');

            Game.updateStatus();
            Game.playAudio(dyingSound, Game.end);
        }
    }

    Game.setDeathTimer = function (player, time) {
        deathTimer[player].push(
            setTimeout(function () {
                Game.player_dies(player);
            }, time)
        );
        let t = new Date().getTime();
        GameStatus.death_timers_start[player].push(t);
        Game.updateStatus();
    };
    Game.end = function () {

        if (GameStatus.timeout ||
            (Game.player_end('ego') && (Game.player_end('alter') || Game.is_solo_game))
        ) {
            let egoArrow = $('.arrow-active');
            egoArrow.off('click', Game.arrowAction);
            $('#ego-keys .key-holder div div').off('click', Game.egoUseKey);
            clearInterval(alterMoving);

            setTimeout(function () {
                $('#zurich-prosocial-game').animate({opacity: 0}, 1000, function () {
                    $('#form').submit();
                });
            }, 1000 * 1.2)
        }
    };

    Game.getPath = function (player, is_active) {
        let p;
        if (player === 'ego') {
            p = is_active ? Game.paths['ego'][GameStatus.ego_path] : Game.paths['ego'][Math.abs(GameStatus.ego_path - 1)];
        } else {
            p = is_active ? Game.paths['alter'][Game.alter_path] : Game.paths['alter'][Math.abs(Game.alter_path - 1)]
        }
        return p
    };

    Game.playAudio = async function (audio_elm, ended_func = null) {
        try {
            await audio_elm[0].play();
            if (ended_func) {
                audio_elm.on('ended', ended_func);
            }
        } catch (err) {
            console.log(err);
            if (ended_func) {
                ended_func();
            }
        }
    }

    Game.setFallingDoors = function (door_num) {
        let tilePs, canvasPs,
            doorIdx = GameStatus.doors.indexOf(GameStatus.doors.filter(d => d.order === door_num)[0]);

        let updateDoorStatus = function (player, door_num, step) {
            let door = GameStatus.doors[doorIdx];
            door.fallen = true;
            if (door.active) {
                door.closed = true;
                door.step = step + closedDoors[door.player].length;
            } else {
                step++;
                while (
                    GameStatus.doors.filter(
                        d => d.active === false && d.fallen === true && d.player === player && d.step === step
                    ).length > 0
                    ) {
                    step++;
                }
                door.step = step
            }
            liveSend(GameStatus);
        }

        let raiseFall = function (door_num) {
            let d = doorDivs.eq(doorIdx),
                doorFallingSound = audios.find('#door_falling'),
                door = {
                    'div': d, 'color': d.attr('data-door-color'), 'player': d.attr('data-player-path'),
                    'top': d.position().top + d.height(), 'active': d.attr('data-active') === 'True'
                };

            if (door.active) {
                doorFalling[door.player] = true;
                if (door.player === 'ego') {
                    $('.arrow-active').hide();
                } else {
                    clearInterval(alterMoving);
                }
            }

            Game.playAudio(doorFallingSound);

            let pathForDoor = Game.getPath(door.player, door.active),
                step = door.div.attr('data-player-path') === 'ego' ?
                    GameStatus.ego_position : GameStatus.alter_position;

            if (door.active) {
                closedDoors[door.player].push(door);
            }

            updateDoorStatus(door.player, door_num, step);

            canvasPs = canvasContainer.offset();
            tilePs = Game.getPosition(pathForDoor[GameStatus.doors[doorIdx].step]);

            door.div.animate({top: '-=' + door.top + 'px'}, 350, function () {
                setTimeout(function () {

                    door.div.css({
                        position: 'absolute',
                        transform: 'translate(-50%, -50%)',
                        left: tilePs.left + canvasPs.left,
                        zIndex: 999
                    });
                    if (!door.active) door.div.css({opacity: 0.4});

                    door.div.animate({top: tilePs.top + canvasPs.top}, 300, function () {
                        canvasContainer.addClass('shaking');

                        setTimeout(function () {
                            canvasContainer.removeClass('shaking');
                            if (door.active) {
                                Game.toggleEmojiBlockedAnimation(door.player);
                                doorFalling[door.player] = false;
                                Game.setDeathTimer(door.player, 800 * Game.kill_time_when_blocked);
                                Game.alterUseKey(door);
                            }
                        }, 1000 * 0.3);
                    });
                }, 1000);
            });
        };

        raiseFall(door_num);
    };

    Game.setFallenDoors = function () {
        let doorsToSet = GameStatus.doors.filter(
                d => d.fallen === true && (d.active === false || d.closed === true)
            ),
            canvasPs = canvasContainer.offset();

        for (let i = 0; i < doorsToSet.length; i++) {
            let d = $('#' + doorsToSet[i].id),
                door = {
                    'div': d, 'color': d.attr('data-door-color'), 'player': d.attr('data-player-path'),
                    'top': d.position().top + d.height(), 'active': d.attr('data-active') === 'True'
                },
                pathForDoor = Game.getPath(door.player, door.active),
                tilePs = Game.getPosition(pathForDoor[doorsToSet[i].step]);

            door.div.css({
                position: 'absolute', transform: 'translate(-50%, -50%)',
                top: tilePs.top + canvasPs.top,
                left: tilePs.left + canvasPs.left, zIndex: 999
            });
            if (!door.active) {
                door.div.css({opacity: 0.4});
            } else {
                let t = new Date().getTime(),
                    startTime = GameStatus.death_timers_start[door.player].shift(),
                    timeToDie = startTime !== undefined ?
                        (800 * Game.kill_time_when_blocked) - parseInt((t - startTime)) :
                        800 * Game.kill_time_when_blocked;

                Game.setDeathTimer(door.player, timeToDie);
                closedDoors[door.player].push(door);
                Game.toggleEmojiBlockedAnimation(door.player);
            }
            door.div.show();
        }

        Game.end();
    };

    Game.openDoor = function (k, open_for, open_by) {

        if (GameStatus.dead_players.indexOf(open_for) > -1) {
            return;
        }

        let doorDiv = closedDoors[open_for][0],
            door = GameStatus.doors.filter(d => d.closed === true && d.player === open_for).sort((a, b) => a.order - b.order)[0];

        if (k.attr('class') === door.color && door.active) {
            let tilePs = door.player === 'ego' ? Game.getPosition(Game.paths['ego'][GameStatus.ego_path][door.step]) : Game.getPosition(Game.paths['alter'][Game.alter_path][door.step]),
                canvasPs = canvasContainer.offset(),
                doorOpeningSound = audios.find('#door_opening'),
                keyIdx = $('#' + open_by + '-keys').find('.key-holder div div').index(k);

            // Remove key from list based on index
            GameStatus.keys[open_by][keyIdx] = null;

            door.closed = false;
            closedDoors[open_for].splice(0, 1);
            clearTimeout(deathTimer[open_for].shift());
            GameStatus.death_timers_start[open_for].splice(0, 1);
            if (open_by === 'ego') {
                GameStatus.ego_num_doors_open += 1;
            }
            Game.updateStatus();

            if (closedDoors[open_for].length === 0) {
                Game.toggleEmojiBlockedAnimation(open_for);
            }

            Game.playAudio(doorOpeningSound);
            k.css({
                position: 'absolute',
                transform: 'translate(-50%, -50%)',
                zIndex: 999
            }).animate({left: tilePs.left + canvasPs.left, top: tilePs.top + canvasPs.top}, 400, function () {
                k.animate({opacity: 0}, 300, function () {
                    k.remove();
                });
                doorDiv.div.animate({opacity: 0}, 300, function () {
                    doorDiv.div.remove();
                    if (open_for === 'ego' && closedDoors[open_for].length === 0) {
                        $('.arrow-active').show();
                    }
                });
                if (door.player === 'alter' || open_by === 'alter') {
                    Game.moveAlter();
                }
            });
        }
    };

    Game.playerHasKey = function (player, door) {
        let hasKey = false;
        $('#' + player + '-keys .key-holder div div').each(function (i, k) {
            if (k.className === door.color) hasKey = true;
        });
        return hasKey
    };

    Game.alterUseKey = function (door) {
        if (door.player === 'alter' && Game.playerHasKey('alter', door)) {
            setTimeout(function () {
                let key = $('#alter-keys .key-holder div').find('.' + door.color).eq(0);
                Game.openDoor(key, 'alter', 'alter');
            }, 1000 * Game.sec_for_alter_to_open_door)
        } else if (door.player === 'ego') {
            Game.alterHelp(closedDoors['ego'][0]);
        }
    };

    Game.alterHelp = function (door) {
        if (Game.playerHasKey(door.player, door)) {
            return;
        }

        let canHelp = Game.playerHasKey('alter', door) && GameStatus.alter_position !== Game.paths_length &&
            (Game.help_other === 'help' ||
                (Game.help_other === 'tit_for_tat' && Game.ego_helped));

        if (canHelp) {
            setTimeout(function () {
                let key = $('#alter-keys .key-holder div').find('.' + door.color).eq(0);
                clearInterval(alterMoving);
                Game.openDoor(key, 'ego', 'alter');
            }, 1000 * Game.sec_for_alter_to_help)
        }
    };

    Game.egoUseKey = function () {
        if (!doorFalling['ego'] &&
            closedDoors['ego'].length > 0 &&
            GameStatus.dead_players.indexOf('ego') === -1 &&
            Game.playerHasKey('ego', closedDoors['ego'][0])) {
            Game.openDoor($(this), 'ego', 'ego');
        } // new modification
        if (
            !doorFalling['alter'] &&
            closedDoors['alter'].length > 0 &&
            GameStatus.dead_players.indexOf('alter') === -1 &&
            !Game.playerHasKey('alter', closedDoors['alter'][0])
            && Game.playerHasKey('ego', closedDoors['alter'][0])
            && GameStatus.ego_position !== Game.paths_length
        ) {
            Game.ego_helped = true;
            GameStatus.ego_helped = 1;
            Game.openDoor($(this), 'alter', 'ego');
        }
    };

    $('#ego-keys .key-holder div div').on('click', Game.egoUseKey);

    let imgsToLoad = 2;
    atlas.onload = function () {
        imgsToLoad--;
        if (imgsToLoad === 0) {
            Game.start();
        }
    };
    atlasTransparent.onload = function () {
        imgsToLoad--;
        if (imgsToLoad === 0) {
            Game.start();
        }
    }

    atlas.src = "/static/game/imgs/" + Game.atlas;
    atlasTransparent.src = "/static/game/imgs/" + Game.atlas_transparent;

});
