// ---------------------------
// TEAM SEARCH
// ---------------------------
const teamSearch = document.getElementById("teamSearch");

if (teamSearch) {

    teamSearch.addEventListener("keyup", function () {

        let searchValue = this.value.toLowerCase();

        let teams = document.querySelectorAll(".team-link");

        teams.forEach(team => {

            let teamName = team.dataset.team;

            if (teamName.includes(searchValue)) {
                team.style.display = "block";
            }
            else {
                team.style.display = "none";
            }

        });

    });

}


window.addEventListener("load", () => {

    setTimeout(() => {

        const loader = document.getElementById("loader");

        loader.style.opacity = "0";

        setTimeout(() => {
            loader.remove();
        }, 500);

    }, 750); // 0.75 seconds

});