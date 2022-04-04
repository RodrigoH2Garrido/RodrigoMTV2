function initMap(){
    var service_url = 'http://localhost:5001/service/getLocations'
    //var service_url = 'http://192.168.0.18:5001/service/getLocations'
    var centro = {}
    var datitos = []
    Promise.all([ // esto es para abrir el mapa.
        getPositions1(service_url).then(function(data){
            addMarkersToList(data,datitos,false)
        }).catch(function(err){
            console.log('error')
        })
    ]).then(()=>{ // esto deberia quedar a la espera de que el mapa cambie para no hacer 2 queries al mismo tiempo
        if(length(datitos)==0){ // en caso de que no se encuentren puntos -> servicios caidos
            centro = {lat:0, lng:0} // setea la vista del mapa en el centro {0,0}
            const map = new google.maps.Map(document.getElementById("map"),{
                zoom:4,
                center:{lat:0,lng:0}
            })
            let aux = document.getElementById("boton-address").addEventListener("click", () => {
                address(map)
            });
            //console.log('zoom inicial : ',map.getZoom())        
        }
        else{// si existen puntos
            let aux = document.getElementById("boton-address").addEventListener("click", ()=>{
                address(map)
            } );

            centro = setNewCenter(datitos) // se calcula el centro entre estos puntos
            console.log('datitos 1 :',datitos)
            const map = new google.maps.Map(document.getElementById("map"), {
                zoom: 4,
                center: centro,
            });
            setMapOnAll(map,datitos)
            var boundListener = google.maps.event.addListener((map),'idle',function(event){ // esto permite identificar cuando el mapa esta quieto
                // o mejor dicho cuando se dejo de interactuar con el mapa.
                let bounds = map.getBounds()
                let southWest = bounds.getSouthWest()
                let northEast = bounds.getNorthEast()
                let zum = map.getZoom()
                console.log('zum: ',zum)
                console.log('fromlat: ',southWest.lat())
                console.log('tolat: ',northEast.lat());
                console.log('fromlng: ',southWest.lng())
                console.log('tong: ',northEast.lng());
                var service_url2 = 'http://localhost:5001/service/getLocations/zoom3/'+zum+'/'+southWest.lat()+'/'+northEast.lat()+'/'+southWest.lng()+'/'+northEast.lng()

                clearMarkers(datitos)
                datitos=deleteMarkers(map,datitos)

                Promise.all([
                    getPositions1(service_url2).then(function(data){
                        addMarkersToList(data,datitos,false)
                        //console.log(datitos)
                    }).catch(function(err){
                        console.log('Error service_url2')
                        //console.log(service_url2)
                    }).then(()=>{
                        setMapOnAll(map,datitos)
                    })
                ])
           })

        }
    })

    // esto esta tomando la direccion que se le pasa al form se la manda al servicio extra, este servicio extrea info de la direccion
    // tambien se le pasa al servicio la lista con los puntos actuales para que se realize el clustering y la idea es que 
    // el servicio devuelvea el punto del address + los k puntos mas cercanos a este, luego se recalcula el centro del mapa para que
    // en base a los puntos obtenidos
    async function address(map){
        var address = document.getElementById("address-input").value
        var k = parseInt(document.getElementById('k-input').value)
        console.log(k)
        var zoom = map.getZoom()
        var bounds = map.getBounds()
        var southWest = bounds.getSouthWest()
        var northEast = bounds.getNorthEast()
        // var url = 'http://192.168.49.2:30100/service/address1'
        var url = 'http://localhost:5001/service/address1'
        var resultado = await getPositions1(url,{
            address:address,
            zoom:zoom,
            fromlat:southWest.lat(),
            tolat:northEast.lat(),
            fromlng:southWest.lng(),
            tolng:northEast.lng(),
            neighbors: k
        }).then( (data) =>{
            console.log('data2: ',data)
            clearMarkers(datitos)
            datitos = deleteMarkers(map,datitos)

            addMarkersToList(data,datitos,true)

            setMapOnAll(map,datitos)
            
        } ).catch((err)=>{
            console.log('error: ',err)
        })
    }

}

function length(obj){
        return Object.keys(obj).length;
}

function getPositions1(url,data){
    return new Promise(function(resolve, reject){ // hace que retorne una promesa que se completa cuando el ajax tiene exito o falla.
        $.ajax({
            url: url,
            data: data || {},
            success: function(data) {
                resolve(data) // Resolve promise and go to then()
            },
            error: function(err) {
                reject(err) // Reject the promise and go to catch()
            }
        });
    })       
}


function addMarkersToList(data,lista,azul){
    let point_str
    let iconito
    for(let i = 0; i<length(data); i++){
        if(data[i]['points']){ // si viene el dato lo agrega si no deja como string vacio
            point_str = 'Points: '+data[i]['points']
        }
        else{
            point_str=''
        }
        
        if(i === length(data)-1 && azul === true){
            iconito = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
        }else{
            iconito ='http://maps.google.com/mapfiles/ms/icons/red-dot.png'
        }
        
        const marker = new google.maps.Marker({
            position: { lat: parseFloat(data[i]['lat']), lng: parseFloat(data[i]['lng']) },
            title: 'Place: '+data[i]['place']+'\n'+ point_str,
            icon:iconito
        })

        lista.push(marker)
    }
}

function setNewCenter(lista){
    var latSum = 0;
    var lngSum = 0;
    
    for( i=0;i<lista.length;i++){
        latSum = latSum + lista[i].getPosition().lat()
        lngSum = lngSum + lista[i].getPosition().lng()
    }

    latSum = latSum/length(lista)
    lngSum = lngSum/length(lista)
    
    return centro ={lat: latSum , lng:lngSum}
}

function setMapOnAll(map,lista){
    for (i = 0; i<lista.length; i++){
        lista[i].setMap(map)
    }
}

function clearMarkers(lista){
    setMapOnAll(null,lista)
    return lista
}
function deleteMarkers(lista){
    setMapOnAll(null,lista)
    return []
}
function prueba (){
    var lat_ = document.getElementById("latitude-input")
    var lng_ = document.getElementById("longitude-input")
    geocoder = new google.maps.Geocoder()
    //console.log(geocoder)
    var point = {lat:lat_,lng:lng_}
    //console.log('valores: ',point)
}

