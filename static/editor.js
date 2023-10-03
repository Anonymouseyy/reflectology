var Delta = Quill.import('delta');
var quill = new Quill('#editor', {
  modules: {
    toolbar: true
  },
  placeholder: 'Compose an epic...',
  theme: 'snow'
});

$("#success").hide();
$("#spinner").hide();
$("#save").click(function(){
    $("#save").prop("disabled", true);
    $("#spinner").fadeIn(500);
    let c = quill.getContents();
    let n = $("#name").text();
    let d = $("#description").text();
    var server_data = [
        {"key": k},
        {"name": n},
        {"description": d},
        {"content": c}
    ];

    $.ajax({
        type: "POST",
        url: "/edit/note",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            if (result.res == "renamed") {
                window.location.href = "/";
            } else {
                $("#spinner").hide();
                $("#success").show();
                $("#success").fadeOut(1000);
            }
       }
    });

    $("#save").prop("disabled", false);
});

$("#success-small").hide();
$("#spinner-small").hide();
$("#save-small").click(function(){
    $("#save-small").prop("disabled", true);
    $("#spinner-small").fadeIn(500);
    let c = quill.getContents();
    let n = $("#name").text();
    let d = $("#description").text();
    var server_data = [
        {"key": k},
        {"name": n},
        {"description": d},
        {"content": c}
    ];

    $.ajax({
        type: "POST",
        url: "/edit/note",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            if (result.res == "renamed") {
                window.location.href = "/";
            } else {
                $("#spinner-small").hide();
                $("#success-small").show();
                $("#success-small").fadeOut(1000);
           }
        }
    });

    $("#save-small").prop("disabled", false);
});