document.addEventListener("DOMContentLoaded", function () {
    let textarea = document.getElementById("pasteTextarea");
    let wordCountDisplay = document.getElementById("wordCount");

    function countWords() {
        let text = textarea.value.trim();
        let words = text.length > 0 ? text.split(/\s+/).length : 0;
    
        // Update word count display
        wordCountDisplay.textContent = words;
    
        let wordCounterContainer = document.querySelector(".word-counter");
        let detectButton = document.getElementById("detectButton");
        let wordWarning = document.getElementById("wordWarning");
    
        // Change color and show/hide warning based on word count
        if (words >= 300) {
            wordCounterContainer.style.color = "green";
            detectButton.disabled = false; // Enable the button
            wordWarning.style.display = "none"; // Hide the warning message
        } else {
            wordCounterContainer.style.color = "red";
            detectButton.disabled = true; // Disable the button
            wordWarning.style.display = "block"; // Show the warning message
        }
    }
    
    // Call countWords when the page loads to ensure the button starts as disabled
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("detectButton").disabled = true;
        document.getElementById("wordWarning").style.display = "block"; // Show warning initially
    });
    
    // Call countWords when the page loads to ensure the button starts as disabled
    document.addEventListener("DOMContentLoaded", function () {
        document.getElementById("detectButton").disabled = true;
    });
    

    // Detect user typing or pasting manually
    textarea.addEventListener("input", countWords);

    // Function to paste text from clipboard
    function pasteText() {
        navigator.clipboard.readText()
            .then(text => {
                textarea.value = text;
                textarea.style.color = "white";
                countWords();
            })
            .catch(err => {
                alert('Failed to paste text. Please allow clipboard access.');
            });
    }

    // Attach paste function to the paste button
    document.querySelector(".paste-button").addEventListener("click", pasteText);

    // Handle file uploads
    document.getElementById("fileInput").addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const fileType = file.name.split('.').pop().toLowerCase();
            if (fileType === "txt") {
                readTextFile(file);
            } else if (fileType === "pdf") {
                readPDF(file);
            } else if (fileType === "docx") {
                readDOCX(file);
            } else {
                alert("Only .txt, .pdf, and .docx files are supported.");
            }
        }
    });

    // Function to read .txt file
    function readTextFile(file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            textarea.value = event.target.result;
            textarea.style.color = "white";
            countWords(); // Count words immediately after file is uploaded
        };
        reader.readAsText(file);
    }

    // Function to read .pdf file using PDF.js
    function readPDF(file) {
        const reader = new FileReader();
        reader.onload = function () {
            const typedarray = new Uint8Array(reader.result);
            pdfjsLib.getDocument(typedarray).promise.then(pdf => {
                let textContent = "";
                let promises = [];
                for (let i = 1; i <= pdf.numPages; i++) {
                    promises.push(pdf.getPage(i).then(page => {
                        return page.getTextContent().then(content => {
                            textContent += content.items.map(item => item.str).join(" ") + " ";
                        });
                    }));
                }
                Promise.all(promises).then(() => {
                    textarea.value = textContent;
                    textarea.style.color = "white";
                    countWords(); // Count words immediately after file is uploaded
                });
            });
        };
        reader.readAsArrayBuffer(file);
    }

    // Function to read .docx file using Mammoth.js
    function readDOCX(file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            let arrayBuffer = reader.result;
            mammoth.extractRawText({ arrayBuffer: arrayBuffer })
                .then(function (result) {
                    textarea.value = result.value;
                    textarea.style.color = "white";
                    countWords(); // Count words immediately after file is uploaded
                })
                .catch(function (err) {
                    alert("Error reading DOCX file.");
                });
        };
        reader.readAsArrayBuffer(file);
    }

    // Allow drop by preventing the default behavior
    function allowDrop(event) {
        event.preventDefault();
    }

    // Handle file drop
    function handleDrop(event) {
        event.preventDefault();
        
        const files = event.dataTransfer.files;
        const fileInput = document.getElementById('fileInput');

        // Optionally, update the file input with the dropped files
        if (files.length > 0) {
            fileInput.files = files;
            alert("File successfully uploaded!");

            // Read and display the dropped file's content
            handleFileUpload(files[0]);
        }
    }

    // Handle the file upload (optional)
    function handleFileUpload(file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const fileContent = event.target.result;
            // Process the file content (e.g., display it in the text area)
            document.getElementById('pasteTextarea').value = fileContent;
            countWords(); // Count words immediately after file is uploaded
        };
        reader.readAsText(file);
    }

    // Handle drag over event
    document.getElementById('uploadArea').addEventListener('dragover', function(event) {
        event.preventDefault();
        this.classList.add('dragover'); // Add a class when file is dragged over
    });

    // Handle drag leave event
    document.getElementById('uploadArea').addEventListener('dragleave', function(event) {
        this.classList.remove('dragover'); // Remove class when drag leaves the area
    });

    // Attach drop event to the upload area
    document.getElementById('uploadArea').addEventListener('drop', handleDrop);
});

