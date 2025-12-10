document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const generateBtn = document.getElementById('generateBtn');
    const loader = document.getElementById('loader');
    const initialState = document.getElementById('initialState');
    const resultContent = document.getElementById('resultContent');
    const descriptionOutput = document.getElementById('descriptionOutput');
    const keywordsOutput = document.getElementById('keywordsOutput');

    // UI Loading State
    generateBtn.disabled = true;
    generateBtn.innerText = 'Generating...';
    initialState.style.display = 'none';
    resultContent.classList.remove('visible');
    loader.classList.add('active');

    // Collect Data
    const formData = {
        product_name: document.getElementById('productName').value,
        features: document.getElementById('features').value.split(',').map(f => f.trim()).filter(f => f),
        target_audience: document.getElementById('audience').value,
        tone: document.getElementById('tone').value
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        // Populate Results
        descriptionOutput.innerText = data.description;

        keywordsOutput.innerHTML = ''; // Clear previous
        data.keywords.forEach(keyword => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.innerText = keyword;
            keywordsOutput.appendChild(span);
        });

        // Show Results
        loader.classList.remove('active');
        resultContent.classList.add('visible');

    } catch (error) {
        console.error("Error:", error);
        loader.classList.remove('active');
        descriptionOutput.innerText = "An error occurred while generating content. Please ensure the backend server is running.";
        keywordsOutput.innerHTML = '';
        resultContent.classList.add('visible');
    } finally {
        generateBtn.disabled = false;
        generateBtn.innerText = 'Generate Content';
    }
});
