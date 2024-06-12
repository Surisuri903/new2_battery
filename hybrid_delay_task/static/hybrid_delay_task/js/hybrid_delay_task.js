$(function () {
    let coinsOnPlate = $($('.coin-on-plate .coin').get().reverse()),
        coinsInPig = $('.coin-in-pig .coin'),
        numCoins = $('input[name=num_coins]'),
        numRects = $('input[name=num_rect]'),
        isTimeout = $('input[name=is_timeout]'),
        rect = $('#rect'),

        rectDisplayed = js_vars.rect_displayed,
        coinInTransfer = js_vars.coin_in_transfer,
        transferDuration = js_vars.transfer_duration * 1000,
        transferStartTimestamp = js_vars.transfer_start_timestamp,
        coinOffset, transferTimer;

    if (rectDisplayed) {
        rect.show();
    }

    coinsOnPlate.each(function (i) {
        if (i < coinsInPig.length) {
            $(this).remove()
        }
    });

    let sendData = function () {
        liveSend(
            {
                num_coins: parseInt(numCoins.val()),
                num_rect: parseInt(numRects.val()),
                rect_displayed: rectDisplayed,
                coin_in_transfer: coinInTransfer,
                transfer_start_timestamp: transferStartTimestamp
            }
        )
    };

    let getNumRects = function () {
        return parseInt(numRects.val())
    };

    let getNextCoin = function () {
        return $('#large-payoff-coins-container .coin').eq(-1);
    };

    let setTransferCompleted = function (coin, coin_container) {
        coin.removeClass('coin-in-transfer').css({"top": "", "left": ""});
        coin_container.prepend(coin.detach());
        numCoins.val(+numCoins.val() + 1);
        coinInTransfer = false;
        transferDuration = js_vars.transfer_duration * 1000;
        sendData();
        setTransferTimer();
    };

    let transferAnimation = function (coin, coin_container, coin_container_offset, duration) {
        coin.animate(
            {
                "top": coin_container_offset.top,
                "left": coin_container_offset.left
            },
            duration, function () {
                setTransferCompleted(coin, coin_container);
            }
        );
    };

    let updateTransferDuration = function () {
        if (coinInTransfer) {
            transferDuration -= +new Date() - transferStartTimestamp;
        }
    };

    let getCoinInTransferOffset = function (coin, coin_container_offset) {
        let pos = coin.offset();

        if (transferDuration < js_vars.transfer_duration * 1000) {

            let passed = 1 - (transferDuration / (js_vars.transfer_duration * 1000));
            pos = {
                top: pos.top + (coin_container_offset.top - pos.top) * passed,
                left: pos.left + (coin_container_offset.left - pos.left) * passed
            }

        }

        return pos;
    };

    let setCoinInTransfer = function (coin, coin_container_offset) {
        coinOffset = getCoinInTransferOffset(coin, coin_container_offset);
        $("body").prepend(coin.detach());
        coin.addClass('coin-in-transfer').css({"top": coinOffset.top, "left": coinOffset.left});
        transferStartTimestamp = coinInTransfer ? js_vars.transfer_start_timestamp : +new Date();
        coinInTransfer = true;
    };

    let transferCoin = function () {
        if ($('#empty-pig .coin').length === js_vars.total_coins) {
            $('#form').submit()
        } else {
            let coin = getNextCoin(),
                emptyCoinDiv = $('#empty-pig').find('.coin-in-pig:not(:has(.coin))').eq(0),
                emptyCoinDivXY = emptyCoinDiv.offset();
            updateTransferDuration();
            setCoinInTransfer(coin, emptyCoinDivXY);
            sendData();
            transferAnimation(coin, emptyCoinDiv, emptyCoinDivXY, transferDuration);
        }
    };

    let setTransferTimer = function () {
        transferTimer = setTimeout(function () {
            transferCoin();
        }, 200);
    };

    setTransferTimer();

    $('#stop-button').on('click', function () {
        $('input[name=is_stopped]').val('True');
        $('#form').submit()
    });

    rect.on('click', function () {
        rectDisplayed = false;
        rect.hide();
        let n = parseInt(numRects.val());
        numRects.val(n + 1);
        sendData();
    });

    let max_waiting = js_vars.max_seconds_on_page,
        currentDate = new Date().valueOf(),
        remainingTimeoutSeconds = max_waiting * 1000 - (currentDate - js_vars.start_timer * 1000),
        milliseconds = Math.floor(remainingTimeoutSeconds);

    $('.hybrid-delay-task').countdown(currentDate.valueOf() + milliseconds)
        .on('update.countdown', function (event) {
            let totSeconds = event.offset.totalSeconds,
                timeLeft = max_waiting - totSeconds;
            if (timeLeft >= js_vars.rects_start_timers[getNumRects()] && !rectDisplayed) {
                rect.show();
                rectDisplayed = true;
                sendData();
            } else if (
                timeLeft >= js_vars.rects_start_timers[getNumRects()] + js_vars.seconds_for_timeout && rectDisplayed
            ) {
                isTimeout.val('True');
                numCoins.val(0);
                $('#form').submit()
            }
        });
})