let clndr = {};

let events = [
    { date: '2023-10' + '-' + '10', title: 'Persian Kitten Auction', location: 'Center for Beautiful Cats' },
    { date: '2023-10' + '-' + '19', title: 'Cat Frisbee', location: 'Jefferson Park' },
    { date: '2023-10' + '-' + '23', title: 'Kitten Demonstration', location: 'Center for Beautiful Cats' },
    { date: '2023-10' + '-' + '07',    title: 'Small Cat Photo Session', location: 'Center for Cat Photography' }
  ];

$(".calendar").clndr({
    template: $('#clndr-template').html(),
    events: events,
    clickEvents: {
      click: function(target) {
        if(target.events.length) {
          var daysContainer = $('#mini-clndr').find('.days-container');
          daysContainer.toggleClass('show-events', true);
          $('#mini-clndr').find('.x-button').click( function() {
            daysContainer.toggleClass('show-events', false);
          });
        }
      }
    },
    adjacentDaysChangeMonth: true,
    forceSixRows: true
  });