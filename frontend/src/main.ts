import "./style.css";

async function fetchData() {
  const response = await fetch(
    "http://localhost:8000/api/v1/search?query=hello"
  );
  const data = await response.json();
  console.log(data);
}

document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
  <main>
  <h1 class="title">Jugge och Alex</h1>
  <img src="/morran_tobias.jpg" class="logo" alt="Jugge och Alex" />
  </main>
`;

// just making sure the backend works. Check browser console for the data
fetchData();
