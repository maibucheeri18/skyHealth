//chooseSession JS
document.addEventListener('DOMContentLoaded', function(){
    const sessionButton = document.getElementById('CS-continue-button');
    const sessionSelect = document.getElementById('session-select');
    const sessionError = document.getElementById('session-error-message');

    if (sessionButton && sessionSelect && sessionError) {
        sessionButton.addEventListener('click', function() {
            const selectedSession = sessionSelect.value;

            if (!selectedSession) {
                sessionError.style.display = 'block';
            } else {
                sessionError.style.display = 'none';
                window.location.href = '/healthCheck/chooseTeam';
            }
        });
    }

    // chooseTeam JS
    const teamButton = document.getElementById('CT-continue-button');
    const teamSelect = document.getElementById('team-select');
    const teamError = document.getElementById('team-error-message');

    if (teamButton && teamSelect && teamError) {
        teamButton.addEventListener('click', function() {
            const selectedTeam = teamSelect.value;

            if (!selectedTeam) {
                teamError.style.display = 'block';
            } else {
                teamError.style.display = 'none';
                window.location.href = '/healthCheck/startPage';
            }
        });
    }

    if (sessionButton) {
        sessionButton.addEventListener('click', function(){
            window.location.href = '/healthCheck/chooseTeam/';
        });
    }

    if (teamButton) {
        teamButton.addEventListener('click', function(){
            window.location.href = '/healthCheck/startPage/';
        });
    }

    const startButton = document.getElementById('start-button');

    if (startButton) {
        startButton.addEventListener('click', function(){
            window.location.href = '/healthCheck/healthCheckForm/';
        });
    }
});
