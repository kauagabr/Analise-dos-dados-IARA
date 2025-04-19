import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import 'bootstrap/dist/css/bootstrap.min.css';

Chart.register(...registerables);

function App() {
  const [datas, setDatas] = useState([]);
  const [dataSelecionada, setDataSelecionada] = useState('');
  const [dados, setDados] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/datas")
      .then(res => {
        setDatas(res.data);
        if (res.data.length > 0) {
          setDataSelecionada(res.data[0]); // primeira data por padrão
        }
      });
  }, []);

  useEffect(() => {
    if (dataSelecionada) {
      const formatada = dataSelecionada.replaceAll('/', '-');
      axios.get(`http://localhost:8000/api/analise-completa/${formatada}`)
        .then(res => setDados(res.data));
    }
  }, [dataSelecionada]);

  const cores = {
    real: 'blue',
    previsao: 'orange',
    mais: 'green',
    menos: 'red',
    atencao: 'yellow',
    alerta: 'red'
  };

  const datasets = dados ? [
    {
      label: 'Atenção',
      data: dados.atencao,
      borderColor: cores.atencao,
      fill: false,
      borderWidth: 2,
      borderDash: [5, 5]
    },
    {
      label: 'Alerta',
      data: dados.alerta,
      borderColor: cores.alerta,
      fill: false,
      borderWidth: 2,
      borderDash: [10, 5]
    },
    {
      label: 'Cota Real',
      data: dados.cotas_reais,
      borderColor: cores.real,
      backgroundColor: 'rgba(0,0,255,0.2)',
      fill: true,
      borderWidth: 2,
      tension: 0.2
    },
    {
      label: 'Previsão',
      data: dados.previsao,
      borderColor: cores.previsao,
      borderWidth: 2,
      tension: 0.2,
      pointStyle: 'rect'
    },
    {
      label: 'Previsão + Erro',
      data: dados.previsao_mais,
      borderColor: cores.mais,
      borderWidth: 2,
      borderDash: [5, 5],
      tension: 0.2
    },
    {
      label: 'Previsão - Erro',
      data: dados.previsao_menos,
      borderColor: cores.menos,
      borderWidth: 2,
      borderDash: [5, 5],
      tension: 0.2
    }
  ] : [];

  return (
    <div className="container py-4">
      <h2 className="mb-4 text-center">IARA - Análise de Cotas do Rio</h2>

      <div className="mb-4">
        <label className="form-label">Selecione a data:</label>
        <select className="form-select" value={dataSelecionada} onChange={e => setDataSelecionada(e.target.value)}>
          {datas.map((data, i) => (
            <option key={i} value={data}>{data}</option>
          ))}
        </select>
      </div>

      {dados && (
        <>
          <Line
            data={{
              labels: dados.dias,
              datasets: datasets
            }}
            options={{
              responsive: true,
              plugins: {
                legend: { position: 'top' },
                title: {
                  display: true,
                  text: 'Cota Real e Previsão com a Margem de Erro',
                  font: { size: 18 }
                }
              }
            }}
          />
          {/*
          <h4 className="mt-5 mb-3">Parâmetros Hidrometeorológicos</h4>
          <table className="table table-bordered table-hover">
            <thead className="table-dark">
              <tr>
                <th>Parâmetro</th>
                <th>Valor</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(dados.parametros).map(([param, valor], i) => (
                <tr key={i}>
                  <td>{param}</td>
                  <td>{valor}</td>
                </tr>
              ))}
            </tbody>
          </table>*/}
        </>
      )}
    </div>
  );
}

export default App;
