




const form = document.querySelector("#uploadForm"),
fileInput = document.querySelector(".file-input"),
progressArea = document.querySelector(".progress-area"),
uploadedArea = document.querySelector(".uploaded-area");

form.addEventListener("click", () =>{
  fileInput.click();
});

fileInput.onchange = ({target})=>{
  uploadFile(target.files)
}

function uploadFile(files){
  let file = files[0]
  let name = file.name;

    if(file){

      if (files.length <=1) {

        if(name.length >= 12){
          let splitName = name.split('.');
          name = splitName[0].substring(0, 13) + "... ." + splitName[1];
        } 
      } else {
          name = `${files.length} files`
        }


      let xhr = new XMLHttpRequest();
      xhr.open("POST", SendUploadURL);
      xhr.upload.addEventListener("progress", ({loaded, total}) =>{
        let fileLoaded = Math.floor((loaded / total) * 100);
        let fileTotal = Math.floor(total / 1000);
        let fileSize;
        (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024*1024)).toFixed(2) + " MB";
        let progressHTML = `<li class="row">
                              <i class="bi bi-file-earmark-fill"></i>
                              <div class="content">
                                <div class="details">
                                  <span class="name">${name} • Uploading</span>
                                  <span class="percent">${fileLoaded}%</span>
                                </div>
                                <div class="progress-bar">
                                  <div class="progress" style="width: ${fileLoaded}%"></div>
                                </div>
                              </div>
                            </li>`;
        uploadedArea.classList.add("onprogress");
        progressArea.innerHTML = progressHTML;
        if(loaded == total){
          progressArea.innerHTML = "";
          let uploadedHTML = `<li class="row row-cols-2">
                                <div class="content upload">
                                  <i class="bi bi-file-earmark-fill"></i>
                                  <div class="details">
                                    <span class="name">${name} • Uploaded</span>
                                    <span class="size">${fileSize}</span>
                                  </div>
                                </div>
                                <i class="bi bi-check text-end"></i>
                              </li>`;
          uploadedArea.classList.remove("onprogress");
          uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
        }
      });
      let data = new FormData(form);

      for (let file = 0; file < files.length; file++) {
                  
        data.append("uploads", files[file].data);

      }

      xhr.send(data);


      // xhr.addEventListener('loadend', function () {
      //   console.log(fileNumber ,  filesCount)
      // 	if(fileNumber < filesCount - 1) {
      // 		// As there are more files to upload, call the upload function again.
      // 		uploadFile(++fileNumber);
      // 	}
      // }, false);

  }
}

$(document).ready(function(){
    const uploadDropArea = document.querySelector('form#uploadForm');

    // const uploadDropArea = document.querySelector('form#uploadForm');
    let fileInput = document.querySelector('.file-input');
    
    // Utility function to prevent default browser behavior
    function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
    }
    
    // Preventing default browser behavior when dragging a file over the container
    uploadDropArea.addEventListener('dragover', preventDefaults);
    uploadDropArea.addEventListener('dragenter', preventDefaults);
    uploadDropArea.addEventListener('dragleave', preventDefaults);
    
    // Handling dropping files into the area
    uploadDropArea.addEventListener('drop', handleDrop);
    
    // We’ll discuss `handleDrop` function down the road
    function handleDrop(e) {
        e.preventDefault();

        // Getting the list of dragged files
        const files = e.dataTransfer.files;

        // Checking if there are any files
        if (files.length) {
        // Assigning the files to the hidden input from the first step
        fileInput.files = files;

        // Processing the files for previews (next step)
        handleFiles(files);
        }
    }

    function handleFiles(files) {
        for (const file of files) {
            // Initializing the FileReader API and reading the file
            const reader = new FileReader();
            reader.readAsDataURL(file);

            // Once the file has been loaded, fire the processing
            reader.onloadend = function (e) {

            };
        }
        }

    // We’ll discuss `isValidFileType` function down the road
    function isValidFileType(file) {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        return allowedTypes.includes(file.type);
    }

    uploadDropArea.addEventListener('dragover', () => {
        uploadDropArea.classList.add('drag-over');
    });
    
    uploadDropArea.addEventListener('dragleave', () => {
    uploadDropArea.classList.remove('drag-over');
    });

});
