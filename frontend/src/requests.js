import router from '@/router/index.js';

export default {
    async post(endpoint, data, redirect){
        return new Promise((resolve, reject) => {
            fetch(endpoint, { method: "POST", body: data}).then((response) => {
                if (response.status == 200){
                    const contentType = response.headers.get("Content-Type")
                    switch (contentType) {
                        case 'application/json':
                            response.json().then(content => resolve(content))
                            break;
                        case 'plain/text':
                            response.text().then(content => resolve(content))
                            break
                        default:
                            resolve(response)
                    }
                } else if (response.status == 440 || response.status == 401){
                    if (redirect == false){
                        reject(response.statusText)
                    }else{
                        router.push('/login')
                        reject('redirected')
                    }
                }else{
                    reject(response.statusText)
                }
            }).catch((error) => {
                reject(error)
            })
        }) 
    },
    async get(endpoint, searchParams, redirect){
        return new Promise((resolve, reject) => {
            const uri = endpoint + (searchParams ? '?'+searchParams.toString() : '') 
            fetch(uri, {method: "GET"}).then((response) => {
                if (response.status == 200){
                    const contentType = response.headers.get("Content-Type")
                    switch (contentType) {
                        case 'application/json':
                            response.json().then(content => resolve(content))
                            break;
                        case 'plain/text':
                            response.text().then(content => resolve(content))
                            break
                        default:
                            resolve(response)
                    }
                } else if (response.status == 440 || response.status == 401){
                    if (redirect == false){
                        reject(response.statusText)
                    }else{
                        router.push('/login')
                    }
                }else{
                    reject(response.statusText)
                }
            }).catch((error) => {
                reject(error)
            })
        })
    }
}
