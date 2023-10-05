let clndr = {};

$(".calendar").clndr({
    template: $('#clndr-template').html(),
    events: events,
    clickEvents: {
      click: function(target) {
        const event = target.events.filter(x => x.date == target.date._i);
        if(event.length == 1) {
            window.location.href = '/edit?entry=' + event[0].key;
        } else if(event.length > 1) {
            document.getElementsByClassName("events-list")[0].innerHTML = "";
            for(i in event) {
                let div = document.createElement('div');
                div.className = "event"
                let a = document.createElement('a');
                a.href = '/edit?entry=' + event[i].key;
                a.innerText = event[i].display_title;
                div.appendChild(a);
                document.getElementsByClassName("events-list")[0].appendChild(div);
                var daysContainer = $('.calendar').find('.days-container');
                daysContainer.toggleClass('show-events', true);
                $('.calendar').find('.x-button').click( function() {
                    daysContainer.toggleClass('show-events', false);
                });
            }
        }
      }
    },
    adjacentDaysChangeMonth: true,
    forceSixRows: true
  });
