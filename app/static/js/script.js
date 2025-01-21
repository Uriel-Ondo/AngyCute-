
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", (event) => {
        const email = document.getElementById("email").value;
        const password = document.getElementById("mot_de_passe").value;

        if (!email.includes("@")) {
            alert("Veuillez entrer une adresse email valide.");
            event.preventDefault(); // Empêche l'envoi du formulaire
        }

        if (password.length < 6) {
            alert("Le mot de passe doit contenir au moins 6 caractères.");
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");

    form.addEventListener("submit", (event) => {
        const nom = document.getElementById("nom").value.trim();
        const prenom = document.getElementById("prenom").value.trim();
        const email = document.getElementById("email").value.trim();
        const telephone = document.getElementById("telephone").value.trim();
        const adresse = document.getElementById("adresse").value.trim();
        const motDePasse = document.getElementById("mot_de_passe").value;

        // Vérifications basiques
        if (nom === "" || prenom === "" || email === "" || telephone === "" || adresse === "") {
            alert("Veuillez remplir tous les champs.");
            event.preventDefault();
            return;
        }

        if (!email.includes("@") || !email.includes(".")) {
            alert("Veuillez entrer une adresse email valide.");
            event.preventDefault();
            return;
        }

        if (telephone.length < 8 || isNaN(telephone)) {
            alert("Veuillez entrer un numéro de téléphone valide.");
            event.preventDefault();
            return;
        }

        if (motDePasse.length < 6) {
            alert("Le mot de passe doit contenir au moins 6 caractères.");
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const adminForm = document.getElementById("adminForm");

    if (adminForm) {
        adminForm.addEventListener("submit", (event) => {
            const nom = document.getElementById("nom").value.trim();
            const prix = document.getElementById("prix").value.trim();
            const description = document.getElementById("description").value.trim();
            const image = document.getElementById("image").files[0];

            if (!nom || !prix || !description || !image) {
                alert("Tous les champs doivent être remplis.");
                event.preventDefault();
            }

            if (prix <= 0) {
                alert("Le prix doit être un nombre positif.");
                event.preventDefault();
            }
        });
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const commandeForm = document.getElementById("commandeForm");

    if (commandeForm) {
        commandeForm.addEventListener("submit", (event) => {
            const total = parseFloat("{{ total_general }}");

            if (total <= 0) {
                alert("Votre panier est vide. Veuillez ajouter des produits avant de commander.");
                event.preventDefault();
            }
        });
    }
});

//menu deroulant
document.addEventListener("DOMContentLoaded", function() {
    var dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function(dropdown) {
        dropdown.addEventListener('mouseover', function() {
            dropdown.querySelector('.dropdown-menu').style.display = 'block';
        });

        dropdown.addEventListener('mouseout', function() {
            dropdown.querySelector('.dropdown-menu').style.display = 'none';
        });
    });
});
