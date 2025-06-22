// kanban_board.js
$(function() {
    $('.card').draggable({
      start: function(event, ui) {
        $(this).addClass('hovered');
      },
      stop: function(event, ui) {
        $(this).removeClass('hovered');
      },
      revert: 'invalid',
      cursor: 'move',
    });
  
    $('.column').droppable({
      drop: function(event, ui) {
        console.log(ui.draggable.attr('id') + " dropped into " + $(this).attr('id'));
        var card_id = ui.draggable.attr('id');
        var column_id = $(this).attr('id');
  
        $.ajax({
          url: '/kanban_board/',
          method: 'POST',
          data: {
            card_id: card_id,
            column_id: column_id,
          },
          success: function() {
            ui.draggable.detach().appendTo($('#' + column_id));
          },
          error: function() {
            alert('An error occurred while updating the card status.');
          },
        });
      },
    });
  });
 