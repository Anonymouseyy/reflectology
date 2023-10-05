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
    let d = document.getElementById("date-input").value;
    var server_data = [
        {"key": k},
        {"title": t},
        {"content": c},
        {"raw_content": rc},
        {"date": d}
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

    change = new Delta();
    $("#save").prop("disabled", false);
});

var change = new Delta();
quill.on('text-change', function(delta) {
  change = change.compose(delta);
});


window.onbeforeunload = function() {
  if (change.length() > 0) {
    return 'There are unsaved changes. Are you sure you want to leave?';
  }
}

setInterval(function() {
  if (change.length() > 0) {
    let c = quill.getContents();
    let rc = quill.getText();
    let t = $("#title").text();
    let d = document.getElementById("date-input").value;
    var server_data = [
        {"key": k},
        {"title": t},
        {"content": c},
        {"raw_content": rc},
        {"date": d}
    ];

    $.ajax({
        type: "POST",
        url: "/save",
        data: JSON.stringify(server_data),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            if (result.res == "success") {
                $("#success").show();
                $("#success").fadeOut(2000);
            }
       }
    })

    change = new Delta();
  }
}, 30*1000);

// Carousel
var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("slide-items");
    if (n > slides.length) {slideIndex = 1}
        if (n < 1) {slideIndex = slides.length}
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
    slides[slideIndex-1].style.display = "block";
}
