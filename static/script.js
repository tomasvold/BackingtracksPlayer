// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const playPauseButton = document.getElementById('play-pause-button');
    const stopButton = document.getElementById('stop-button');
    const playlist = document.getElementById('playlist');
    const availableTracksList = document.getElementById('available-tracks');

    let dragSrcEl = null;
    let currentlyPlaying = null;
    let selectedTrack = null;

    // Function to update the playlist on the UI
    function updatePlaylist(files) {
        playlist.innerHTML = '';
        files.forEach(file => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="drag-handle" draggable="true">☰</span>
                <span>${file}</span>
                <span class="remove-button">✖</span>
            `;
            li.dataset.filename = file;
            playlist.appendChild(li);
        });

        addPlaylistEventListeners();
    }

    // Function to update the available tracks on the UI
    function updateAvailableTracks(files) {
        availableTracksList.innerHTML = '';
        files.forEach(file => {
            const li = document.createElement('li');
            li.textContent = file;
            li.dataset.filename = file;
            availableTracksList.appendChild(li);
        });

        addAvailableTracksEventListeners();
    }

    function addPlaylistEventListeners() {
        const listItems = document.querySelectorAll('#playlist li');

        listItems.forEach(item => {
            item.addEventListener('dragstart', handleDragStart);
            item.addEventListener('dragover', handleDragOver);
            item.addEventListener('drop', handleDrop);
            item.addEventListener('dragend', handleDragEnd);
            item.addEventListener('click', handleTrackSelection);
            const removeButton = item.querySelector('.remove-button');
            removeButton.addEventListener('click', handleRemoveFile);
        });
    }

    function addAvailableTracksEventListeners() {
        const listItems = document.querySelectorAll('#available-tracks li');
        listItems.forEach(item => {
            item.addEventListener('click', handleAddTrack);
        });
    }

    function handleTrackSelection(e) {
        if (e.target.className === 'remove-button' || e.target.classList.contains('drag-handle')) {
            return;
        }

        const previousSelection = document.querySelector('.playing-track');
        if (previousSelection) {
            previousSelection.classList.remove('playing-track');
        }

        selectedTrack = e.currentTarget.dataset.filename;
        e.currentTarget.classList.add('playing-track');
    }

    async function handleRemoveFile(e) {
        e.stopPropagation();
        const filename = e.target.dataset.filename;
        if (confirm(`Are you sure you want to remove '${filename}' from the playlist?`)) {
            const response = await fetch(`/api/remove_file`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ filename })
            });

            if (response.ok) {
                loadAllTracks();
            } else {
                alert('Failed to remove file from playlist.');
            }
        }
    }

    async function handleAddTrack(e) {
        const filename = e.target.dataset.filename;
        const response = await fetch(`/api/add_track`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename })
        });
        
        if (response.ok) {
            loadAllTracks();
        } else {
            alert('Failed to add track to playlist.');
        }
    }

    function handleDragStart(e) {
        dragSrcEl = e.target.closest('li');
        dragSrcEl.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', e.target.closest('li').innerHTML);
    }

    function handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        const targetEl = e.target.closest('li');
        if (targetEl && targetEl !== dragSrcEl && targetEl.parentNode === playlist) {
            const rect = targetEl.getBoundingClientRect();
            const midpoint = rect.y + rect.height / 2;
            if (e.clientY > midpoint) {
                playlist.insertBefore(dragSrcEl, targetEl.nextSibling);
            } else {
                playlist.insertBefore(dragSrcEl, targetEl);
            }
        }
    }

    function handleDrop(e) {
        e.stopPropagation();
        const targetEl = e.target.closest('li');
        if (dragSrcEl && targetEl && dragSrcEl !== targetEl) {
            // The item has already been moved in handleDragOver
        }
    }

    async function handleDragEnd(e) {
        dragSrcEl.classList.remove('dragging');
        const listItems = document.querySelectorAll('#playlist li');
        const newOrder = Array.from(listItems).map(item => item.dataset.filename);
        await savePlaylistOrder(newOrder);
    }
    
    async function savePlaylistOrder(newOrder) {
        const response = await fetch(`/api/reorder_playlist`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_order: newOrder })
        });
        
        if (response.ok) {
            console.log('Playlist order saved successfully.');
        } else {
            console.error('Failed to save playlist order.');
        }
    }

    playPauseButton.addEventListener('click', async () => {
        if (!selectedTrack) {
            console.log('No track selected. Please select a track from the playlist.');
            return;
        }

        const response = await fetch('/api/play_pause', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename: selectedTrack })
        });
        const data = await response.json();
        playPauseButton.textContent = data.state === 'playing' ? '⏸️' : '▶️';
        console.log('Playback state:', data.state);

        const listItems = document.querySelectorAll('#playlist li');
        listItems.forEach(item => {
            if (item.dataset.filename === selectedTrack) {
                currentlyPlaying = item;
            }
        });
    });

    stopButton.addEventListener('click', async () => {
        const response = await fetch('/api/stop', { method: 'POST' });
        const data = await response.json();
        console.log('Playback state:', data.state);
        playPauseButton.textContent = '▶️';
        
        if (currentlyPlaying) {
            currentlyPlaying.classList.remove('playing-track');
        }
        currentlyPlaying = null;
        selectedTrack = null;
    });

    async function loadAllTracks() {
        try {
            const playlistResponse = await fetch('/api/playlist');
            const playlistData = await playlistResponse.json();
            updatePlaylist(playlistData.files);

            const availableTracksResponse = await fetch('/api/available_tracks');
            const availableTracksData = await availableTracksResponse.json();
            updateAvailableTracks(availableTracksData.files);
        } catch (error) {
            console.error('Error loading tracks:', error);
        }
    }
    
    loadAllTracks();
});