async function analyzeTopic() {
    const topic = document.getElementById("topic").value.trim();

    if (topic === "") {
        alert("Por favor, ingresa un tema.");
        return;
    }

    // Desactiva el botón y mostrar indicador de búsqueda
    const analyzeButton = document.getElementById("analyze-button");
    analyzeButton.disabled = true;
    const originalButtonText = analyzeButton.innerText;
    analyzeButton.innerText = "Buscando...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({topic})
        });

        if (!response.ok) {
            throw new Error("Error en la solicitud.");
        }

        const result = await response.json();
        renderResults(result);
    } catch (error) {
        console.error(error);
        alert("Ocurrió un error al procesar la solicitud.");
    } finally {
        // Reactiva el botón y restaurar el texto original
        analyzeButton.disabled = false;
        analyzeButton.innerText = originalButtonText;
    }
}

function renderResults(data) {
    const output = document.getElementById("results");
    output.innerHTML = "";

    if (data.tweets && data.tweets.length > 0) {
        // Crea sección para los tweets
        const tweetsSection = document.createElement("div");
        tweetsSection.classList.add("mb-4");

        const tweetsHeader = document.createElement("h2");
        tweetsHeader.innerText = "Tweets Obtenidos:";
        tweetsSection.appendChild(tweetsHeader);

        data.tweets.forEach((tweet, index) => {
            const tweetCard = document.createElement("div");
            tweetCard.classList.add("card", "tweet-card");

            const cardBody = document.createElement("div");
            cardBody.classList.add("card-body");

            const tweetTitle = document.createElement("h5");
            tweetTitle.classList.add("card-title");
            tweetTitle.innerText = `Tweet ${index + 1}:`;

            const tweetText = document.createElement("p");
            tweetText.classList.add("card-text");
            tweetText.innerText = tweet;

            cardBody.appendChild(tweetTitle);
            cardBody.appendChild(tweetText);
            tweetCard.appendChild(cardBody);
            tweetsSection.appendChild(tweetCard);
        });

        output.appendChild(tweetsSection);
    } else {
        const noTweets = document.createElement("p");
        noTweets.innerText = "No se encontraron tweets para el tema proporcionado.";
        output.appendChild(noTweets);
    }

    if (data.summary) {
        // Crea sección para el resumen
        const summarySection = document.createElement("div");
        summarySection.classList.add("summary-section");

        const summaryHeader = document.createElement("h2");
        summaryHeader.innerText = "Resumen:";
        summarySection.appendChild(summaryHeader);

        const summaryText = document.createElement("p");
        summaryText.innerText = data.summary;
        summarySection.appendChild(summaryText);

        output.appendChild(summarySection);
    }
}