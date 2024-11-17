import "./style.css";

async function fetchData(query: string = "skridskor") {
  const response = await fetch(
    `http://localhost:8000/api/v2/search/?query=${query}&limit=10`
  );
  const data = await response.json();
  console.log(data);

  // Rendera produkterna inuti productGrid-diven
  const productGridHTML = data.products
    .map((product: any) => product_cart(product))
    .join("");

  document.querySelector<HTMLDivElement>("#app")!.innerHTML = `
    <main>
      <div class="productGrid">
        ${productGridHTML}
      </div><!--/productGrid-->
    </main>
  `;
}

function product_cart(product: any) {
  return `
    <div class="productCard">
      <img src="${product.image}">
      <h2>${product.brand} ${product.name}</h2>
      <p>Fr. ${product.price} kr på ${product.provider}</p>
      <div>
        <button>Till butik</button>
      </div>
    </div>
  `;
}

// Anropa fetchData för att hämta och visa produkterna
fetchData("skridskor");
