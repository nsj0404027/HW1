document.getElementById('recommendForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const song = document.getElementById('song').value;
    const artist = document.getElementById('artist').value;
    
    const loader = document.getElementById('loader');
    const resultsContainer = document.getElementById('results');
    
    // Reset state and show loader
    resultsContainer.innerHTML = '';
    resultsContainer.classList.add('hidden');
    loader.classList.remove('hidden');

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ song, artist })
        });
        
        const data = await response.json();
        
        loader.classList.add('hidden');
        resultsContainer.classList.remove('hidden');

        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach(rec => {
                const card = document.createElement('div');
                card.className = 'result-card';
                card.innerHTML = `
                    <div class="song-info">
                        <h3>${rec.title}</h3>
                        <p>${rec.artist}</p>
                    </div>
                    <a href="${rec.link}" target="_blank" class="listen-btn">Listen on YT</a>
                `;
                resultsContainer.appendChild(card);
            });
        }
    } catch (error) {
        loader.classList.add('hidden');
        resultsContainer.classList.remove('hidden');
        resultsContainer.innerHTML = '<p style="color: #FF3366; text-align: center;">Something went wrong. Please try running the backend server!</p>';
    }
});
