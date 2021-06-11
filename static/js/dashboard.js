function alterarFarois(idtabela) {
  let tabela = document.getElementById(idtabela);
  let farol = "";
  for (let i = 1; i < tabela.rows.length; i++) {
    farol = tabela.rows[i].cells[4].innerHTML;
    if (farol == "VERMELHO") {
      tabela.rows[i].cells[4].outerHTML =
        "<td><span class='farol vermelho'></span></td>";
    } else if (farol == "AMARELO") {
      tabela.rows[i].cells[4].outerHTML =
        "<td><span class='farol amarelo'></span></td>";
    } else if (farol == "VERDE") {
      tabela.rows[i].cells[4].outerHTML =
        "<td><span class='farol verde'></span></td>";
    } else {
      tabela.rows[i].cells[4].outerHTML =
        "<td><span class='farol'></span></td>";
    }
  }
}
window.onload = () => {
  alterarFarois("emExecucao");
  alterarFarois("emDiagnostico");
};
