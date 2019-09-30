// Variables
var face_img_data = {
  file1: null,
  file2: null
};

var face_img_DB_data = {
  file: null,
};

var face_feat_data = {
  file: null
};

var upload_data = {
  name: "",
  file: null
};

var recognize_data = {
  id1: "",
  id2: ""
};


var message = null;
var active_section = null;

function render() {
  // clear form data
  $(".form-item input").val("");
  $(".tabs li").removeClass("active");
  $(".tabs li:first").addClass("active");

  active_section = "upload";
  $("#" + active_section).show();
}
function update() {
  if (message) {
    // render message
    $(".message").html(
      '<p class="' +
        _.get(message, "type") +
        '">' +
        _.get(message, "message") +
        "</p>"
    );
  } else {
    $(".message").html("");
  }
  $("#upload, #face-match-ID, #face-match-image, #face-match-DB, #face-feature").hide();
  $("#" + active_section).show();
}

function readURL(input, id) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $(id)
                .attr('src', e.target.result)
                .width(150)
                .height(200);
        };
        reader.readAsDataURL(input.files[0]);
    }
}


$(document).ready(function() {
  active_section = "upload";

  $("#upload, #face-match-ID, #face-match-image, #face-match-DB, #face-feature").hide();
  $("#" + active_section).show();

  // listen for file added
  $("#upload #input-file").on("change", function(event) {
    //set file object to train_data
    upload_data.file = _.get(event, "target.files[0]", null);
    });

  // listen for name change
  $("#name-field").on("change", function(event) {
    upload_data.name = _.get(event, "target.value", "");
  });

  // listen tab item click on
  $(".tabs li").on("click", function(e) {
    var $this = $(this);

    active_section = $this.data("section");

    // remove all active class
    $(".tabs li").removeClass("active");
    $this.addClass("active");
    message = null;

    update();
  });

  // listen the form upload submit
  $("#upload").submit(function(event) {
    message = null;

    if (upload_data.file) {

      var upload_form_data = new FormData();
      upload_form_data.append("name", upload_data.name);
      upload_form_data.append("imagefile", upload_data.file);

      axios
        .post("/api/upload", upload_form_data)
        .then(function(response) {
          message = {
            type: "success",
            message:
              "Uploading has been done, user name: " +
              _.get(response, "data.name","Unknown user")
          };

          upload_data = { name: "", file: null };
          update();
        })
        .catch(function(error) {
          message = {
            type: "error",
            message: _.get(
              error,
              "response.data.error.message",
              "Unknown error."
            )
          };

          update();
        });
    } else {
      message = { type: "error", message: "Image is required." };
    }

    update();
    event.preventDefault();
  });

  // Face Match using UUIDs
  // listen for name-field1 for uuid1 change
  $("#name-field1").on("change", function(e) {
    recognize_data.id1 = _.get(e, "target.value", null);
  });

  // listen for name-field2 for uuid2 change
  $("#name-field2").on("change", function(e) {
    recognize_data.id2 = _.get(e, "target.value", null);
  });
  // listen for form submit
  $("#face-match-ID").submit(function(e) {
    // call to backend
    var facematch_form_data = new FormData();
    //var facematch_form_data2 = new FormData();

    facematch_form_data.append("id1", recognize_data.id1);
    facematch_form_data.append("id2", recognize_data.id2);

    axios
       .post("/api/FaceMatch_ID", {"images":[recognize_data.id1,
       recognize_data.id2]	})
      .then(function(response) {
        document.getElementById("img_uuid1").src = "data:image/jpg;base64, " + response.data.FaceMatch_ID.image1;
        document.getElementById("img_uuid1").width = 150;
        document.getElementById("img_uuid1").height = 200;
        document.getElementById("img_uuid2").src = "data:image/jpg;base64, " + response.data.FaceMatch_ID.image2;
        document.getElementById("img_uuid2").width = 150;
        document.getElementById("img_uuid2").height = 200;
        message = {
          type: "success",
          message:
            "The face match between users: " +
            response.data.FaceMatch_ID.probability
        };

        recognize_data = { id1: "", id2: ""};
        update();
      })
      .catch(function(err) {
        message = {
          type: "error",
          message: _.get(err, "response.data.error.message", "Unknown error")
        };

        update();
      });
    e.preventDefault();
  });

  // Face Match using images
  // listen for file added
  $("#face-match-image #input-file1").on("change", function(event) {
  //set file object 
  face_img_data.file1 = _.get(event, "target.files[0]", null);
  });

  $("#face-match-image #input-file2").on("change", function(event) {
    //set file object
    face_img_data.file2 = _.get(event, "target.files[0]", null);
    });

  // listen the face-match-image submit
  $("#face-match-image").submit(function(event) {
    message = null;

    if (face_img_data.file1 && face_img_data.file2) {

      var face_img_form_data = new FormData();
      face_img_form_data.append("imagefile1", face_img_data.file1);
      face_img_form_data.append("imagefile2", face_img_data.file2);

      axios
        .post("/api/FaceMatch_Image", face_img_form_data)
        .then(function(response) {
          message = {
            type: "success",
            message:
              "We found the match between the images with probability: " +
              response.data.FaceMatch_Image.probability
          };

          face_img_data = { file1: null, file2: null };
          update();
        })
        .catch(function(error) {
          message = {
            type: "error",
            message: _.get(
              error,
              "response.data.error.message",
              "Unknown error."
            )
          };

          update();
        });
    } else {
      message = { type: "error", message: "Image is required." };
    }

    update();
    event.preventDefault();
  });

  // Face Match DB
  $("#face-match-DB #input-file3").on("change", function(event) {
    //set file object 
    face_img_DB_data.file = _.get(event, "target.files[0]", null);
    });

  // listen the face-match-DB submit
  $("#face-match-DB").submit(function(event) {
    message = null;

    if (face_img_DB_data.file) {

      var face_img_DB_form_data = new FormData();
      face_img_DB_form_data.append("imagefile", face_img_DB_data.file);

      axios
        .post("/api/FaceMatch_DB", face_img_DB_form_data)
        .then(function(response) {
            document.getElementById("img_upload_db2").src = "data:image/jpg;base64, " + response.data.FaceMatch_DB.images[0];
            document.getElementById("img_upload_db2").width = 150;
            document.getElementById("img_upload_db2").height = 200;
            document.getElementById("img_upload_db3").src = "data:image/jpg;base64, " + response.data.FaceMatch_DB.images[1];
            document.getElementById("img_upload_db3").width = 150;
            document.getElementById("img_upload_db3").height = 200;
            document.getElementById("img_upload_db4").src = "data:image/jpg;base64, " + response.data.FaceMatch_DB.images[2];
            document.getElementById("img_upload_db4").width = 150;
            document.getElementById("img_upload_db4").height = 200;

            message = {
              type: "success",
              message:
                response.data.FaceMatch_DB.probability
            };
          

          face_img_DB_data = { file: null};
          update();
        })
        .catch(function(error) {
          message = {
            type: "error",
            message: _.get(
              error,
              "response.data.error.message",
              "Unknown error."
            )
          };

          update();
        });
    } else {
      message = { type: "error", message: "Image is required." };
    }

    update();
    event.preventDefault();
  });


  // Facial Feature
  $("#face-feature #input-file").on("change", function(event) {
    //set file object 
    face_feat_data.file = _.get(event, "target.files[0]", null);
    });

  // listen the face-feature submit
  $("#face-feature").submit(function(event) {
    message = null;

    if (face_feat_data.file) {
    // do send data to backend api
      var face_feat_form_data = new FormData();
      face_feat_form_data.append("imagefile", face_feat_data.file);
      axios
        .post("/api/FaceFeature", face_feat_form_data)
        .then(function(response) {
          document.getElementById("img_result").src = "data:image/jpg;base64, " + response.data.FaceFeature.img_feat;
          document.getElementById("img_result").width = 150;
          document.getElementById("img_result").height = 200;
          
          message = {
            type: "success",
            message:
             "Image features Identified"
          };

          face_feat_data = { file: null};
          update();
        },
        )
        .catch(function(error) {
          message = {
            type: "error",
            message: _.get(
              error,
              "response.data.error.message",
              "Unknown error."
            )
          };

          update();
        });
    } else {
      message = { type: "error", message: "Image is required." };
    }

    update();
    event.preventDefault();
  });

  // render the app;
  render();
});
