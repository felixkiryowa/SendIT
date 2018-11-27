var url = 'https://francissendit.herokuapp.com/api/v2/parcels/1';

fetch(url).then(response => response.json).then(data => console.log(data))