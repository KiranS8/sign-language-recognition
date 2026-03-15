function previewImage(){

    const file = document.getElementById("imageInput").files[0];
    const preview = document.getElementById("preview");

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
}

async function predict(){

    const loader = document.getElementById("loader");

    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    if(!file){
        alert("Upload an image first");
        return;
    }

    loader.style.display="block";

    const formData = new FormData();
    formData.append("file",file);

    try{

        const response = await fetch(
            "https://cher-presymphysial-pamella.ngrok-free.dev/predict",
            {
                method:"POST",
                body:formData
            }
        );

        const data = await response.json();

        loader.style.display="none";

        document.getElementById("letter").innerText =
        data.prediction;

        const confidence = (data.confidence*100).toFixed(2);

        document.getElementById("confidenceText").innerText =
        confidence+"%";

        document.getElementById("barFill").style.width =
        confidence+"%";

    }

    catch(error){

        loader.style.display="none";
        alert("API connection error");

    }
}