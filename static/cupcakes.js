const BASE_URL = "http://127.0.0.1:5000/api";

function renderCupcakesPage(cupcake) {
    return `
    <div data-cupcake-id=${cupcake.id}>
    <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="btn btn-danger btn-sm delete-button">X<button>
    </li>
    <img class="Cupcake-img" src="${cupcake.image}" alt="Cupcake">
    </div>   `;

};

async function showCupcakes() {
    const resp = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of resp.data.cupcakes) {
        let newCupcake = $(renderCupcakesPage(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
};

$("#new-cupcake-form").on("submit", async function (e){
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let size = $("#form-size").val();
    let rating = $("#form-rating").val();
    let image = $("#form-image").val();

    if (image = null) {
        $("#form-image").val() = "https://tinyurl.com/demo-cupcake"
    }

    const newCupcakeResp = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, rating, size, image
    });

    let newCupcake = $(renderCupcakesPage(newCupcakeResp.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$("#cupcakes-list").on("click", ".delete-button", async function(e) {
    e.preventDefault();

    let $cupcake = $(e.target).closest("div");
    let cupcakeID = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeID}`);
    $cupcake.remove();
});

$(showCupcakes);