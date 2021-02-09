import http from "../http-common";
/* eslint-disable */
class UploadFilesService {
  upload(file, onUploadProgress) {
    // let formData = new FormData();

    // formData.append("file", file);
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = (e) => { 
      const data = csvJSON(e.target.result);
      http.post("/upload", data , {
        headers: {
          "Content-Type": "application/json"
        },
        onUploadProgress
      });
    };
    
    // return http.post("/upload", data , {
    //   headers: {
    //     "Content-Type": "application/json"
    //   },
    //   onUploadProgress
    // });
  }

  getFiles() {
    return http.get("/files");
  }
}

function csvJSON(csv){

  var lines=csv.split("\n");

  var result = [];

  var headers=lines[0].split(",");

  for(var i=1;i<lines.length;i++){

	  var obj = {};
	  var currentline=lines[i].split(",");

	  for(var j=0;j<headers.length;j++){
		  obj[headers[j]] = currentline[j];
	  }

	  result.push(obj);
  }
  
  return result; //JavaScript object
  // return JSON.stringify(result); //JSON
}

export default new UploadFilesService();