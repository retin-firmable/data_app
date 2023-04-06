$(document).ready(function() {
    // Handle form submission for CSV file upload
    $('#upload-form').submit(function(event) {
      event.preventDefault();
  
      const formData = new FormData($(this)[0]);
  
      $.ajax({
        url: '/csv',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
          $('#upload-modal').modal('hide');
          location.reload();
        },
        error: function(jqXHR, textStatus, errorThrown) {
          $('#upload-error').text(jqXHR.responseJSON.detail);
        }
      });
    });
  
    // Handle click event for column rename button
    $('.rename-column').click(function() {
      const column_id = $(this).data('column-id');
      const new_column_name = prompt("Enter new column name:");
  
      if (new_column_name !== null) {
        $.ajax({
          url: '/csv/column/' + column_id,
          type: 'PUT',
          data: JSON.stringify({ new_column_name: new_column_name }),
          contentType: 'application/json',
          success: function(data) {
            location.reload();
          },
          error: function(jqXHR, textStatus, errorThrown) {
            alert(jqXHR.responseJSON.detail);
          }
        });
      }
    });
  
    // Handle click event for delete row button
    $('.delete-row').click(function() {
      const row_id = $(this).data('row-id');
  
      $.ajax({
        url: '/csv/row/' + row_id,
        type: 'DELETE',
        success: function(data) {
          location.reload();
        },
        error: function(jqXHR, textStatus, errorThrown) {
          alert(jqXHR.responseJSON.detail);
        }
      });
    });
  });
  