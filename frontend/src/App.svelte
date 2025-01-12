<script>
  import {api} from './util/api.js';
  // Define a function to handle the button click
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  async function fetchData() {
    try {
      const data = await api(backendUrl+'/testAdd', {
        method: 'GET'
      });

      
      console.log(data); // Do something with the data (e.g., update the UI)
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Error fetching data! Check the console for more details.');
    }
  }
</script>


<button on:click={fetchData}>Call REST Endpoint</button>


<style>
</style>
