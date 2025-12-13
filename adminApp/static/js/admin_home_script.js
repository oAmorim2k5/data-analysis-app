document.addEventListener('DOMContentLoaded', () => {
    
    // Seleciona elementos necessários
    const sidebar = document.querySelector('.sidebar');
    const clientButtons = document.querySelectorAll('.client-button');
    const dropdownMenus = document.querySelectorAll('.dropdown-menu'); // Seleciona todos os menus

    // Função auxiliar para fechar todos os menus
    const closeAllDropdowns = () => {
        dropdownMenus.forEach(menu => {
            menu.classList.remove('open');
        });
    };

    // --- 1. Lógica de Abertura/Fechamento ao CLICAR ---
    
    clientButtons.forEach(button => {
        button.addEventListener('click', () => {
            
            const clientId = button.getAttribute('data-client');
            const dropdown = document.getElementById(`menu-${clientId}`);
            
            // Fecha todos os outros dropdowns
            dropdownMenus.forEach(menu => {
                if (menu.id !== `menu-${clientId}`) {
                    menu.classList.remove('open');
                }
            });

            // Alterna o dropdown clicado
            dropdown.classList.toggle('open');
        });
    });

    // --- 2. Lógica de Fechamento ao TIRA O MOUSE (mouseleave) ---

    if (sidebar) { 
        sidebar.addEventListener('mouseleave', () => {
            setTimeout(closeAllDropdowns, 1); 
        });
    } else {
        console.error("Erro: Elemento '.sidebar' não encontrado no DOM. Verifique a classe no HTML.");
    }
});