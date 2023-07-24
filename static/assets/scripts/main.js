
  // Fechar dropdown quando o mouse sair do elemento
  $('.dropdown').mouseleave(function() {
    $(this).removeClass('show');
    $(this).find('.dropdown-menu').removeClass('show');
  });

  function moveExcessItems() {
    // todo: ao redimensionar a janela, os itens que foram movidos para o dropdown não voltam para a lista
    // todo: novo bug que não tinha no ultimo commit: ao redimensionar a janela os itens NÃO SAO MOVIDOS not at all, e o "mais" some
    const columnWidth = $('.col-10').width() / 1.2;
    const listItems = $('#categoryList li');
    const dropdown = $('#moreDropdown');
    const dropdownList = $('#moreItems');

    // Inverter a ordem dos itens da lista
    const reversedListItems = listItems.get().reverse();
    const reversedList = $(reversedListItems);

    let totalWidth = 0;
    let hiddenItems = [];

    // Calcula a largura total dos itens da lista invertida, começando a partir do índice 1
    for (let index = 1; index < reversedList.length; index++) {
        totalWidth += $(reversedList[index]).outerWidth(true);
    }

    // Verifica se a largura total dos itens MENOS UM é maior que a largura da coluna
    if (totalWidth > columnWidth) {
        // Calcula a largura do dropdown
        const dropdownWidth = dropdown.outerWidth(true);
        // Calcula a largura dos itens que serão movidos para o dropdown
        let excessWidth = totalWidth - columnWidth + dropdownWidth;
        // Move os itens para o dropdown
        for (let index = 1; index < reversedList.length; index++) {
            excessWidth -= $(reversedList[index]).outerWidth(true);
            if (excessWidth >= 0) {
                reversedList[index].classList.remove('list-inline-item');
                hiddenItems.push(reversedList[index]);
            }
        }
        $(hiddenItems.reverse()).appendTo(dropdownList);
    }

    if (dropdownList.children().length === 0) {
        dropdown.hide();
    } else {
        dropdown.show();
    }
    }


  // Chama a função quando a página carrega e também após redimensionar a janela
  $(window).on('load resize', moveExcessItems);