function alterarFarois(idtabela, numColuna) {
  let tabela = document.getElementById(idtabela);
  let farol = "";
  for (let i = 1; i < tabela.rows.length; i++) {
    farol = tabela.rows[i].cells[numColuna].innerHTML;
    if (farol == "VERMELHO") {
      tabela.rows[i].cells[numColuna].outerHTML =
        "<td><span class='farol vermelho'></span></td>";
    } else if (farol == "AMARELO") {
      tabela.rows[i].cells[numColuna].outerHTML =
        "<td><span class='farol amarelo'></span></td>";
    } else if (farol == "VERDE") {
      tabela.rows[i].cells[numColuna].outerHTML =
        "<td><span class='farol verde'></span></td>";
    } else {
      tabela.rows[i].cells[numColuna].outerHTML =
        "<td><span class='farol'></span></td>";
    }
  }
}
window.onload = () => {
  alterarFarois("emExecucao", 3);
  alterarFarois("emDiagnostico", 4);
};
