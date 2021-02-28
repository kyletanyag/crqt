<template>
<select id="mySelect" style="width: 581px; height:300px;" rows="10" multiple="multiple">
    <option id="id1" value="value1">id1</option>
    <option id="id2" value="value2">id2</option>
    <option id="id3" value="value3">id3</option>
    <option id="id4" value="value4">id4</option>
    <option id="id5" value="value5">id5</option>
    <div class="text-center py-2">
                    <button type="submit" class="btn btn-primary" @click="saveTextAsFile">Submit</button>
                </div>
</select>
                
</template>
<script>
    function saveTextAsFile() {
        var textToWrite = document.getElementById('mySelect').value;
        var textFileAsBlob = new Blob([textToWrite], {type: 'text/plain'});
        var fileNameToSaveAs = "directive.txt";

        var downloadLink = document.createElement("a");
        downloadLink.download = fileNameToSaveAs;
        downloadLink.innerHTML = "Download File";
        console.log("innerHTML -> " + downloadLink.innerHTML);
//        if ($('#sel1').val() == '') {
//            alert('Please select ACCOUNT NAME, SCHEDULE and TASK first.');
//        }
//        else {
            window.webkitURL != null;
            downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
//        }
        downloadLink.click();
    }

    var button = document.getElementById('save');
    button.addEventListener('click', saveTextAsFile);
</script>