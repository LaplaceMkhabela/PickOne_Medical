async function sendId(id) {
    url = '/doctor/view'
    let resp_promise = await fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ 'id': id }) })

    let resp_data = await resp_promise.json()

    if (resp_data['code'] == '500') {
        Swal.fire(
            {
                title: 'Error',
                text: resp_data['msg'],
                icon: 'error',
                showCancelButton: false,
                confirmButtonText: "Ok"
            }
        ).then(
            (result)=>{
                if(result.isConfirmed){
                    window.location.reload()
                }
            }
        )
    }
    else if(resp_data['code'] == '200'){
        window.location.assign(resp_data['link'])
    }
    else{
        Swal.fire(
            {
                title: 'Error',
                text: 'Something went wrong',
                icon: 'error',
                showCancelButton: false,
                confirmButtonText: "Ok"
            }
        ).then(
            (result)=>{
                if(result.isConfirmed){
                    window.location.reload()
                }
            }
        )
    }
}