class CupcakeManager{
    constructor(listSelector){
        this.listSelector = listSelector;
    }

    async fetchAllCupcakes(){
        const resp = await axios.get('api/cupcakes')
        const cupcakes = resp.data.cupcakes;
        $(this.listSelector).empty();
        cupcakes.forEach(cupcake => this.addCupcakeToList(cupcake));
    }

    async createCupcake(cupcakeData){
        const resp = await axios.post('api/cupcakes', cupcakeData);
        this.addCupcakeToList(resp.data.cupcake);
    }

    addCupcakeToList(cupcake) {
        $(this.listSelector).append(
            `<li>
                <img src="${cupcake.image}" alt="${cupcake.flavor}" style="width: 100px; height: 100px;">
                ${cupcake.flavor}, ${cupcake.size}, Rating: ${cupcake.rating}
                - <button class="delete-cupcake" data-id="${cupcake.id}">X</button>
            </li>`
        );
    }

    async deleteCupcake(cupcakeId) {
        await axios.delete(`api/cupcakes/${cupcakeId}`);
        $(`button[data-id=${cupcakeId}]`).parent().remove();
    }

    async searchCupcakes(searchTerm) {
        const response = await axios.get(`api/cupcakes/search?term=${searchTerm}`);
        const cupcakes = response.data.cupcakes;
        $(this.listSelector).empty();
        cupcakes.forEach(cupcake => this.addCupcakeToList(cupcake));
    }
}

const cupcakeManager = new CupcakeManager('#cupcake_list');

$(document).ready(function(){
    cupcakeManager.fetchAllCupcakes();

    $('#add-cupcake-form').on('submit', function(e){
        console.log("sdklfjsdklfjl")
        e.preventDefault();
        const cupcakeData = {
            flavor: $('#flavor').val(),
            size: $('#size').val(),
            rating: $('#rating').val(),
            image: $('#image').val()
        };
        cupcakeManager.createCupcake(cupcakeData);
    });

    $(document).on('click', '.delete-cupcake', function(){
        const cupcakeid= $(this).data('id');
        cupcakeManager.deleteCupcake(cupcakeid);
    });

    $('#search-cupcake-form').on('submit', function(e){
        e.preventDefault();
        const searchterm =$('input[name="searchTerm"]').val();
        cupcakeManager.searchCupcakes(searchterm);
    });
});