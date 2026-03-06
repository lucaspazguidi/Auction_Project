async function get_item_info(){
    // Get item_id and convert into integer value
    const item_select = document.getElementById("item")
    const item_id = parseInt(item_select.value)
    
    // Create a response object
    const resp = await fetch(`/api/item/${item_id}`)
    
    if(!resp.ok){
        // If the request fails, hide and clear
        document.getElementById("description").textContent = '';
        document.getElementById("item_image").src = '';
        document.getElementById("item_image").style.display = 'none'; // Hide
        return
    }
    
    // Await json response
    const item = await resp.json()

    // Apply the changes dynamically
    const description = document.getElementById("description")
    const image = document.getElementById("item_image")

    description.textContent = item.desc
    image.src = item.image 
    
    image.style.display = 'block'; 

}

document.getElementById("item").addEventListener("change", get_item_info)