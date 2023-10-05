var Delta = Quill.import('delta');

var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],
  ['code-block'],

  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],
  [{ 'indent': '-1'}, { 'indent': '+1' }],
  [{ 'direction': 'rtl' }],

  [{ 'color': [] }, { 'background': [] }],
  [{ 'font': [] }],

  ['clean']
];

var quill = new Quill('#editor', {
  modules: {
    toolbar: toolbarOptions
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
    let rc = quill.getText();
    let t = $("#title").text();
    var server_data = [
        {"key": k},
        {"title": t},
        {"content": c},
        {"raw_content": rc}
    ];

    $.ajax({
        type: "POST",
        url: "/save",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            if (result.res == "success") {
                $("#spinner").hide();
                $("#success").show();
                $("#success").fadeOut(1000);
            }
       }
    });

    $("#save").prop("disabled", false);
});