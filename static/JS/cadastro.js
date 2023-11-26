function formatarTelefone(input) {
    let numeroLimpo = input.value.replace(/\D/g, '');
    if (numeroLimpo.length > 2) {
      numeroLimpo = `(${numeroLimpo.substring(0, 2)}) ${numeroLimpo.substring(2)}`;
    }
    input.value = numeroLimpo;
  }

  $(document).ready(function () {
    $('#id_state').on('change', function () {
        var selectedOption = $(this).val();

        // Make an AJAX request to the Django view
        $.ajax({
            url: '/cadastro_associado/',  // Replace with your actual URL
            data: {'state': selectedOption},
            dataType: 'json',
            success: function (data) {
              $('#id_city').empty();
              data.cities.forEach(function (city) {
                  $('#id_city').append($('<option>', {
                      value: city,
                      text: city
                  }));
              });
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });
});

$(document).ready(function () {
    if ($('#id_responsavel').is(':checked')) {
        $('#id_nome_responsavel').show();
    } else {
        $('#id_nome_responsavel').hide();
    }
    $("#id_responsavel").change(function() {
        if ($('#id_responsavel').is(':checked')) {
            $('#id_nome_responsavel').show();
        } else {
            $('#id_nome_responsavel').hide();
        }
    });
});